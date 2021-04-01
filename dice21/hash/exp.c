#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/shm.h>
#include <stdint.h>
#include <sys/ioctl.h>

/* constants for the different commands */
#define ADD_KEY 0x1337
#define DELETE_KEY 0x1338
#define UPDATE_VALUE 0x1339
#define DELETE_VALUE 0x133a
#define GET_VALUE 0x133b

/* struct for command parameters.
 * some commands do not use all the fields (for example, del_key only uses key and idx)
*/

typedef struct {
  uint32_t key;
  uint32_t size;
  char* src;
  char *dest;
} req;


/* file descriptor to the opened device (global variable for convenience) */
int hashbrown = -1;

/* open the device (must be called at start) */
void open_hashbrown() {
  hashbrown = open("/dev/hashbrown", O_RDWR);
  if (hashbrown < 0) {
    perror("[-] open hashbrown failed");
    exit(1);
  }
  printf("[+] open fd: %x\n", hashbrown);
}

void add_key(uint32_t key, uint32_t size, char *src){
    req r;
    r.key = key;
    r.size = size;
    r.src = src;
    if(ioctl(hashbrown,ADD_KEY,&r)!=0){
        perror("[-] Add failed");
        exit(1);
    }
}

void delete_key(uint32_t key){
    req r;
    r.key = key;
    if(ioctl(hashbrown,DELETE_KEY,&r)!=0){
        perror("[-] Delete failed");
        exit(1);
    }
}

void update_value(uint32_t key, uint32_t size, char *src){
    req r;
    r.key = key;
    r.size = size;
    r.src = src;
    if(ioctl(hashbrown,UPDATE_VALUE,&r)!=0){
        perror("[-] Update failed");
        exit(1);
    }
}

void delete_value(uint32_t key){
    req r;
    r.key = key;
    if(ioctl(hashbrown,DELETE_VALUE,&r)!=0){
        perror("[-] Delete value failed");
        exit(1);
    }
}

void get_value(uint32_t key, uint32_t size, char *dest){
    req r;
    r.key = key;
    r.size = size;
    r.dest = dest;
    if(ioctl(hashbrown,GET_VALUE,&r)!=0){
        perror("[-] Get value failed");
        exit(1);
    }
}

void main() {
  open_hashbrown();
  char kbuf[10] = "aaaaaaaaaa";
  add_key(1,10,kbuf);
  printf("Add ok :)");
  char kbuf_dest[0x100];
  get_value(1,10,kbuf_dest);
}
