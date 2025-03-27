import sys
import datetime
import filter_logs as fl
import re
from collections import namedtuple

# Defining a namedtuple to represent each HTTP request for beter readability
HttpRequest = namedtuple('HttpRequest', [
    'timestamp', 'uid', 'orig_host', 'orig_port', 
    'resp_host', 'resp_port', 'method', 'host', 'uri', 'status_code'
])

def read_log():
    http_requests = []
    for line in sys.stdin:
        http_requests.append(split_log(line))
    return http_requests


def split_log(line):
    parts = line.strip().split('\t')
    
    try:
        ts = datetime.datetime.fromtimestamp(float(parts[0])) 
        uid = parts[1]
        orig_h = parts[2]
        orig_p = int(parts[3])
        resp_h = parts[4]
        resp_p = int(parts[5])
        method = parts[7]
        host = parts[8]
        uri = parts[9]
        
        match = re.search(r'\s(\d{3})\s', line)  # Looks for a 3-digit number surrounded by spaces
        if match:
            status_code = match.group(1)
        else:
            status_code = ''

        return HttpRequest(ts, uid, orig_h, orig_p, resp_h, resp_p, method, host, uri, status_code)
    
    except (IndexError, ValueError) as e:
        print(f"Error reading the line : {line} - {e}", file=sys.stderr)
        return None 
    

def sort_log(log, index):
    try:
        return sorted(log, key=lambda x: x[index])
    except IndexError:
        print("Index out of bounds", file=sys.stderr)
        return log
    except TypeError:
        print("Non numeric index", file=sys.stderr)
        return log


if __name__ == "__main__":
    logs = read_log()

    for log in fl.get_entries_by_extension(logs, 'html'):
        print(log)
