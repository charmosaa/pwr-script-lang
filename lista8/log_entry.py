class LogEntry:
    def __init__(self, http_request):
        (self.timestamp, self.uid, self.orig_host, self.orig_port,
         self.resp_host, self.resp_port, self.method, self.host,
         self.uri, self.status_code) = http_request

    def __str__ (self):
        timestamp_str = self.timestamp.strftime('%Y-%m-%d %H:%M:%S.%f') if self.timestamp else "N/A"
        raw_string = f"{timestamp_str} {self.uid} {self.orig_host} {self.orig_port} {self.resp_host} {self.resp_port} {self.method} {self.host} {self.uri} {self.status_code}"
        return raw_string[:40] + "..."