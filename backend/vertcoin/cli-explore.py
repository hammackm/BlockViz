import os
import subprocess


print(subprocess.check_output([os.path.join(os.getcwd(), 'vertcoin-cli.exe'), 'getrawmempool', 'true']).decode().replace('\r\n', ''))