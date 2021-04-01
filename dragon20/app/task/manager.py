import os
import sys
import time
import mysql.connector
import uuid


DBHOST = "{{db_host}}"
DBUSERNAME = "apparmor"
DBPASSWORD = "{{db_passwd}}"
DOCKERPASSWORD = "{{db_hubpasswd}}"

DOCKERUSERNAME = "dragonsectorclient"

TASK_NUM = int(sys.argv[1])

RUN_LIMIT = 60

creds = (DOCKERUSERNAME+':'+DOCKERPASSWORD).encode("base64").strip()
config=open('ds-apparmor-task/config.json.template').read()
config = config.replace("$$CREDENTAILS$$",creds)
f = open('ds-apparmor-task/config.json','w')
f.write(config)
f.close()

os.system("cd ds-apparmor-task; docker build . -t ds-apparmor-task")
os.system("apparmor_parser -r -W apparmor-policy")


myid=uuid.uuid4()

mydb = mysql.connector.connect(
  host=DBHOST,
  user=DBUSERNAME,
  passwd=DBPASSWORD,
  database="apparmor"
)

allowed_chars="1234567890qwertyuiopasdfghjklzxcvbnm/"
def fix_name(name):
    for ch in name:
        if ch not in allowed_chars:
            return "hello-world"
    return name

def get_images(limit):
    update = mydb.cursor()
    update.execute("UPDATE images SET owner='"+str(myid)+"', status = 1 WHERE status = 0 order by id limit "+str(limit))
    mydb.commit()
    fetch = mydb.cursor()
    fetch.execute("SELECT name FROM images WHERE status=1 AND owner='"+str(myid)+"'")
    myresult = fetch.fetchall()
    return [item[0] for item in myresult]

def finish_images():
    update = mydb.cursor()
    update.execute("UPDATE images SET status = 2 WHERE status = 1 AND owner='"+str(myid)+"'")
    mydb.commit()

while 1:
    time.sleep(3)
    images = get_images(TASK_NUM)
    for i in range(len(images)):
        print 'running '+images[i]
        image = fix_name(images[i])
        cmd = 'docker run --privileged --cpus=".5" -m "512m" -e "RUN_ME='+image+'" --rm --name ds-apparmor-runner-'+str(i)+' -d ds-apparmor-task'
        os.system(cmd)
    time.sleep(RUN_LIMIT)
    for i in range(len(images)):
        cmd = 'docker kill ds-apparmor-runner-'+str(i);
        os.system(cmd)
    finish_images()




