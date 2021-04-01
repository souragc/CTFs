from pwn import *
from struct import *
    
#context.log_level = 'debug'
elf = ELF('./rop')
  
# get section address
addr_dynsym     = elf.get_section_by_name('.dynsym').header['sh_addr']
addr_dynstr     = elf.get_section_by_name('.dynstr').header['sh_addr']
addr_relaplt     = elf.get_section_by_name('.rela.plt').header['sh_addr']
addr_plt        = elf.get_section_by_name('.plt').header['sh_addr']
addr_got    = elf.get_section_by_name('.got.plt').header['sh_addr']
addr_bss        = elf.get_section_by_name('.bss').header['sh_addr']
addr_got_read   = elf.got['read']
  
log.info('Section Headers')
log.info('.dynsym  : ' + hex(addr_dynsym))
log.info('.dynstr  : ' + hex(addr_dynstr))
log.info('.rela.plt : ' + hex(addr_relaplt))
log.info('.plt     : ' + hex(addr_plt))
log.info('.got     : ' + hex(addr_got))
log.info('.bss     : ' + hex(addr_bss))
log.info('read@got : ' + hex(addr_got_read))
