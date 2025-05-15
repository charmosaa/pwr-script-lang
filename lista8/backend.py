import sys
import datetime
from collections import namedtuple
import validator as vd

# namedtuple to represent each HTTP request for better readability
HttpRequest = namedtuple('HttpRequest', [
    'timestamp', 'uid', 'orig_host', 'orig_port', 
    'resp_host', 'resp_port', 'method', 'host', 'uri', 'status_code'
])

def read_log(file):
    http_requests = []
    with open(file, "r", encoding="utf-8") as f:
        content = f.readlines()
        for line in content:
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
        status_code = vd.parse_code(parts[14]) 

        return HttpRequest(ts, uid, orig_h, orig_p, resp_h, resp_p, method, host, uri, status_code)
    
    except (IndexError, ValueError) as e:
        print(f"Error reading the line : {line} - {e}", file=sys.stderr)
        return None 
    
def get_entries_by_date(logs, start_date, end_date):
    return [log for log in logs if log.timestamp >= start_date and log.timestamp <= end_date]


if __name__ == "__main__":
    logs = read_log("data\http_first_100k.log")

    filter_logs = get_entries_by_date(logs, datetime.datetime(2012, 3, 16, 13, 40), datetime.datetime(2012, 3, 16, 13, 50) )
    print(len(filter_logs))
    print(filter_logs[:5])