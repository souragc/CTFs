---
title: Diary - Balsn 2020
date: 2020-11-16 14:20:00
author: Cyb0rG
author_url: https://twitter.com/_Cyb0rG
categories:
  - Pwn
tags:
  - Heap
  - Linux
  - Balsn
---

**tl;dr**

+ Edit `stdin` file structure by supplying negetive index to the edit function.
+ Create fake fastbins in main arena to get overlapping chunks for leaking libc by overwriting `mmap bit`.
+ Write to `__malloc_hook` with fastbin attack.

<!--more-->

**Challenge Points:** 850
**Solves:** 18
**Solved By:** [3agl3](https://twitter.com/3agl31) , [Cyb0rG](https://twitter.com/_Cyb0rG)

We had a great time this weekend playing this year's edition of Balsn CTF. The quality of challenges was nothing less as should be expected from Balsn. I spent most of my time working on just two challenges. This post will discuss the solution of the challenge we solved during the CTF.

## Challenge description

The challenge was running on `glibc 2.29`. The binary is a standard CTF-style x86-64 bit executable.

## Initial analysis

```sh
gdb-peda$ checksec
CANARY    : ENABLED
FORTIFY   : disabled
NX        : ENABLED
PIE       : ENABLED
RELRO     : FULL
```

## Reversing

+ The program takes in 32 bytes of name initially.
+ The `add` option takes user size (less than 0x80) , `calloc`s a chunk of that size , takes in data for the chunk , and finally stores the chunk on a global table.
+ On deleting a chunk , the table is not nulled but a bit is set which checks for any use after free attacks.
+ The edit option lets us edit a chunk at an index only once.

## Bugs

+ We can supply negetive index to the `edit` function.
+ Heap can be easily leaked by `view name` option since name is not appended by null.

## Exploit development

We have good targets in the bss segment at negetive offsets to our table. Two of them being `stdin` and `stdout` file buffers. During the CTF , we were working with `stdin` itself since corrupting `stdout` and writing past it required overwriting the `vtables` which is not ideal since functions like `printf` , `puts` are being used. So we went for `stdin` since only `read` function is being used and mind you , `read` does not use stdin file structure. So, we're good to go.

## Writing past stdin

We were in for a surprise to realize that `main arena` lies just below the `stdin` file structure. Now, since we have heap leak, we can create fake fastbins in the fastbin entries of the main arena structure. This way, we can suitably set overlapping chunks to write to the `size` field of an `unsorted bin` chunk (size 0x80). We flip the mmaped bit of the free chunk to fool calloc to return uninitialized memory thus getting libc leak.

## The final stage

One thing that we have to take care of is that , even if we set fake fastbins and their fd's pointing to `__malloc_hook`, `calloc` can send them to tcache if the count of tcache is less than 7. Hence , we first have to free a tcache bin , so that while calling `calloc` , we eventually won't dump the fastbins into tcache.

Once everything is set , we get allocation on `__malloc_hook` , overwrite it with `one_gadget` and pop a shell.

## Conclusion

The idea of creating fake fastbins on main arena was quite novel. Kudos to team balsn for great challenges and a great CTF overall.
Credits to [3agl3](https://twitter.com/3agl31) for the major idea and [exploit](https://gist.github.com/PwnVerse/ec0ffe91313e39f9ca51d4272b54da77).





        

