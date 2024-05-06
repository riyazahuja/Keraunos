import subprocess
from datetime import datetime
import json
# import time

# Interval in seconds - how often you want to send the file
interval = 0.5

# Bash script path
bash_script = "./bluetooth_sender.sh"

json_fd = 'test.json'
data = {'time' : datetime.now().isoformat()}

with open(json_fd, 'w') as f:
    json.dump(data,f)

while True:
    # Execute the bash script
    st = datetime.now()
    subprocess.run(bash_script, shell=True)
    f=datetime.now()-st
    print(f)


    # Wait for the specified interval
    # time.sleep(interval)
