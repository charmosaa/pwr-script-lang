import sys
import validator as vd

def get_entries_by_addr(log, address):
    if vd.is_valid_ip(address):
        return [entry for entry in log if entry.host == address or entry.resp_host == address]
    
    print("Address not valid", file=sys.stderr)
    return []

def get_entries_by_code(log, code):
    if not vd.is_valid_http_code(code):
        print(f"Invalid HTTP code: {code}. Must be a 3-digit number.")
        return []
    return [entry for entry in log if entry.status_code == code]


def get_failed_reads(log, combine = False):
    four_xx = []
    five_xx = []

    for entry in log:
        code = entry.status_code
        if(code):
            if(int(code/100) == 4):
                four_xx.append(entry)
            elif(int(code/100) == 5):
                five_xx.append(entry)
    
    if(combine):
        return four_xx+five_xx
    return four_xx, five_xx

def get_entries_by_extension(log, extension):
    extension_with_dot = '.' + extension
    return [entry for entry in log if entry.uri.endswith(extension_with_dot)]