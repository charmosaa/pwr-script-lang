from collections import Counter
import read_log as rl

def entry_to_dict(entry):
    return entry._asdict()

def log_to_dict(log):
    log_dict = {}

    for entry in log:
        entry_dict = entry_to_dict(entry)
        
        # for first appearence of uid create an empty list
        if entry_dict['uid'] not in log_dict:
            log_dict[entry_dict['uid']] = []
        
        # append the uid key with the entry dictionary
        log_dict[entry_dict['uid']].append(entry_dict)

    return log_dict

def analyze_entry(entries):
    hosts = {}      # dictionary of hosts data
    methods = Counter()     # counter for each method
    ok_codes = 0             # counter for 2xx codes   

    for entry in entries:
        host = entry['resp_host']
        method = entry['method']

        # host data
        if host not in hosts:
            hosts[host] = {
                'requests': 1,
                'first_request': entry['timestamp'],
                'last_request': entry['timestamp']
            }
        else:
            hosts[host]['requests'] += 1
            hosts[host]['first_request'] = min(hosts[host]['first_request'], entry['timestamp'])
            hosts[host]['last_request'] = max(hosts[host]['last_request'], entry['timestamp'])
        
        # methods data
        if method:
            methods[method] += 1
        
        # status codes
        if entry['status_code'] and int(entry['status_code'])/100 == 2:
            ok_codes += 1
        
    return hosts, methods, ok_codes

def print_dict_entry_dates(log_dict):
    for uid, entries in log_dict.items():
        hosts, methods, ok_codes = analyze_entry(entries)

        if len(entries) > 2:
            # printing block
            print('-'*50)
            print(f"SESSION: {uid}")
            print_methods_distribution(methods)
            print(f'HOSTS: {hosts}')
            print(f'{ok_codes*100/len(entries) :.2f}% of OK staus codes')

def print_methods_distribution(methods):
    total_methods = sum(methods.values())

    if total_methods > 0:
        print("Method distribution:")
        for method, count in methods.items():
            percent = (count / total_methods) * 100
            print(f"  {method}: {percent:.2f}%")
    else:
        print("No methods in this session")

if __name__ == "__main__":
    log = rl.read_log()
    logs_dict = log_to_dict(log)
    print_dict_entry_dates(logs_dict)
