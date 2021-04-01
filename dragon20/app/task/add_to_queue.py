import sys
import mysql.connector
import random
import string
from hashcash import check
import SocketServer

def get_input(sock, prompt):
	sock.sendall(prompt)
	return readline(sock).strip()


def readline(sock):
  data = ''
  while not data.endswith("\n"):
    x = sock.recv(1)
    if len(x) < 1:
      break
    data += x
  return data



DBHOST = "{{db_host}}"
DBUSERNAME = "apparmor"
DBPASSWORD = "{{db_passwd}}"

DOCKERUSERNAME = "dragonsectorclient"

HARDNESS = 26

def main(r):
  resource = "".join(random.choice(string.ascii_lowercase) for i in range(8))

  r.sendall("Please use the following command to solve the Proof of Work: hashcash -mb{} {}\n".format(HARDNESS, resource))
  stamp = get_input(r, "PoW: ")

  if not stamp.startswith("1:"):
		r.sendall("Only hashcash v1 supported\n")
		return


  if not check(stamp, resource=resource, bits=HARDNESS):
		r.sendall("Invalid PoW\n")
		return

  image = get_input(r, "Image name to run (shared with '"+DOCKERUSERNAME+"' on registry.gitlab.com)\n")


  mydb = mysql.connector.connect(
    host=DBHOST,
    user=DBUSERNAME,
    passwd=DBPASSWORD,
    database="apparmor"
  )

  allowed_chars="1234567890qwertyuiopasdfghjklzxcvbnm/"
  def check_name(name):
      for ch in name:
          if ch not in allowed_chars:
              return ""
      return name


  if check_name(image) == "":
      r.sendall("Image name contains not allowed characters\n")
      return

  add = mydb.cursor()
  add.execute('insert into images VALUES (NULL,0,"'+image+'","");')
  mydb.commit()
  r.sendall("Image added to the queue\n")

class TaskHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        main(self.request)
        

if __name__ == '__main__':
    SocketServer.ThreadingTCPServer.allow_reuse_address = True
    server = SocketServer.ThreadingTCPServer(('0.0.0.0', 1337), TaskHandler)
    server.serve_forever()

