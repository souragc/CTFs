---
title: Diary - Balsn 2020
date: 2020-11-17 18:00:00
author: 3agl3
author_url: https://twitter.com/3agl31
categories:
  - Pwn
tags:
  - Heap
  - Balsn
---

**tl;dr**

+ Overflow from `stdin` stucture till `main_arena`.
+ Create fake `fastbin` chunks to get overlapping chunk and leak.
+ Overwrite `__malloc_hook` using fastbin attack.

We were able to solve only one pwn challenge this time. According to the author the method explained in this post is an unintentded solution.

## Analysis

Binary was a standard menu driven heap program with usual mitigations.

```sh
gdb-peda$ checksec
CANARY    : ENABLED
FORTIFY   : disabled
NX        : ENABLED
PIE       : ENABLED
RELRO     : FULL
```

## Reversing

First the program asks for a `name` of size 32 bytes which is stored on bss.  
After this we are given 5 options:  
+ `Show name`: Prints the name.
+ `Write Diary`: Creates a chunk using `calloc` (max size is 0x80). Size is stored as the first 4 bytes and the pointer is stored in a global array (Max 14 allocations).
+ `Read Diary`: Prints the content of a chunk.
+ `Edit Diary`: Edit the content of a chunk. Can be only done once.
+ `Tear out page`: Frees a chunk and set a bit to `1`. This bit will be used to prevent `UAF`.

Since `calloc` is used, any chunk that goes to tcache cannot be reused.

## Bugs

+ Since the `name` is non null terminated and since it is stored just above the pointer table, we can get heap leak by calling `Show name` after creating atleast 1 chunk.
+ In `Edit Diary`, the index can be negative.

## Exploitation

Since heap leak is easy, let's do that.
```python
sendlineafter("name : ",'a'*0x1f)
add(0x80,"aaaa")
view_name()
```
Next we need a libc leak. The issue here is that the program uses `calloc` which nulls out the content of a chunk before giving it to the user. This does not happen if the `mmap bit` of the chunk is set. Let's find a way to do that. For this, we will be using the second bug. We had several targets on bss at negative offset. Two of them were `stdin` and `stdout` pointers. We can't use `stdout` since program uses `puts` and `printf` which will use `vtable`. So we are going to use `stdin`.  
If we check using a debugger, we can see that `main_arena` lies after `stdin` meaning we can create fake chunks. Remember that we only have 1 edit. So we will have to set everything together.  
We create a chunk with data that looks like a header of a chunk.

```python
payload = "\x00"*4 + p64(0)*2 + p64(0x51)
add(0x80,payload)
```
Now in the edit operation, we put the pointer to this fake chunk inside fastbin. Next time when we ask for a chunk of size 0x41, calloc returns our fake chunk. Using this, we can overwrite the size of next chunk while also setting the `mmap bit`. Now we just need to add another chunk and view it to get leak.

## Getting shell

To overwrite `__malloc_hook`, we need a fastbin which is poiting to this. Since we don't have libc leak at the time of doing the `edit`, we have to create a fastbin that points to `__malloc_hook`. Actually no. Remember that our tcache of size 0x70 is currently empty. Meaning if we have a fastbin pointing to `__malloc_hook` and then allocates a chunk, the remaining chunks will be moved to tcache. Let's try to fill tcache of size 0x70. Consider this case.

![](./fastbin.png)

Here we have a chain of fake chunks which ultimately points to `__malloc_hook`. If we put chunk `1` in the fastbin and allocates a chunk, calloc sees that tcache is empty and start moving the chunks. When it reaches chunk `8`, tcache is full and the remaining is kept in fastbin and chunk `1` is returned to the user. Next time when we allocates, we will get `__malloc_hook` and we can overwrite it with `one_gadget`. Next call to malloc will give us a shell.

## Conclusion

Even though this was not the intended solution, it was a really good heap challenge. Thanks to Balsn for such a ctf.  
You can find the full exploit [here](https://github.com/souragc/Exploits/blob/main/Balsn/Diary.py)
