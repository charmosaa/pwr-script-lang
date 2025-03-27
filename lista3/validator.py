import re

def is_valid_ip(address):
    ip_pattern = re.compile(r'^(?:\d{1,3}\.){3}\d{1,3}$')
    return bool(ip_pattern.match(address))


def is_valid_http_code(code):
    return bool(re.match(r'^\d{3}$', code))

def parse_code(code):
    if(is_valid_http_code(code)):
        return int(code)
    else:
        return None