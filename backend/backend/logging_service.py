from datetime import datetime

def log(type: str, file: str, text: str):
    '''
    Writes warning messages to the logfile
    '''

    line = f'[{type}]: {datetime.now()} {file} {text}\n'

    with open("log.txt", "w") as log_file:
        log_file.write(line)