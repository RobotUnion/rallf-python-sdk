from rallf.tools.communicator import Communicator


class Logger(Communicator):
    """
        Log severity codes according with RFC 3164
        @see https://www.ietf.org/rfc/rfc3164.txt
    """

    def __init__(self, input, output):
        super().__init__(input, output)

    def log(self, msg, severity=7, data=None):
        return self.rpccall("log", {"message": str(msg), "severity": severity, "data": data}, wait=False)

    def debug(self, msg, data=None):
        """Debug: debug-level messages"""
        return self.log(msg, 7, data)

    def info(self, msg, data=None):
        """Informational: informational messages"""
        return self.log(msg, 6, data)

    def notice(self, msg, data=None):
        """Notice: normal but significant condition"""
        return self.log(msg, 5, data)

    def warning(self, msg, data=None):
        """Warning: warning conditions"""
        return self.log(msg, 4, data)

    def error(self, msg, data=None):
        """Error: error conditions"""
        return self.log(msg, 3, data)

    def critical(self, msg, data=None):
        """Critical: critical conditions"""
        return self.log(msg, 2, data)

    def alert(self, msg, data=None):
        """Alert: action must be taken immediately"""
        return self.log(msg, 1, data)

    def emergency(self, msg, data=None):
        """Emergency: system is unusable"""
        return self.log(msg, 0, data)
