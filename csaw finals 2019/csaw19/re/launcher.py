#!/usr/bin/python3
import subprocess
import tempfile
import stat
import os
import base64

binary = "./loader"
def mystery_boi(lib_data):
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpfile, tmpfile_path = tempfile.mkstemp(dir=tmpdir)

        st = os.stat(tmpfile)
        os.chmod(tmpfile, st.st_mode & (~stat.S_IRUSR))

        if lib_data:
            env = {"LD_PRELOAD":tmpfile_path}
            os.write(tmpfile, lib_data)
        else:
            env = {}
        os.close(tmpfile)
        subprocess.run("./mystery_boi", env=env)

buf = base64.b64decode(input())
mystery_boi(buf)
