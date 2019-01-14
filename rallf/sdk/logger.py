from rallf.sdk.network import Network


class Logger(Network):
    """
        Log severity codes according with RFC 3164
        @see https://www.ietf.org/rfc/rfc3164.txt
    """

    def __init__(self, input, output, context):
        super().__init__(input, output, context)

    def log(self, msg, severity=7, channel="", data=None):
        return self.event(
            "log",
            {
                "message": str(msg),
                "channel": channel,
                "severity": severity,
                "data": data
            }
        )

    def debug(self, msg, channel="", data=None):
        """Debug: debug-level messages"""
        return self.log(msg, 7, channel, data)

    def info(self, msg, channel="", data=None):
        """Informational: informational messages"""
        return self.log(msg, 6, channel, data)

    def notice(self, msg, channel="", data=None):
        """Notice: normal but significant condition"""
        return self.log(msg, 5, channel, data)

    def warning(self, msg, channel="", data=None):
        """Warning: warning conditions"""
        return self.log(msg, 4, channel, data)

    def error(self, msg, channel="", data=None):
        """Error: error conditions"""
        return self.log(msg, 3, channel, data)

    def critical(self, msg, channel="", data=None):
        """Critical: critical conditions"""
        return self.log(msg, 2, channel, data)

    def alert(self, msg, channel="", data=None):
        """Alert: action must be taken immediately"""
        return self.log(msg, 1, channel, data)

    def emergency(self, msg, channel="", data=None):
        """Emergency: system is unusable"""
        return self.log(msg, 0, channel, data)
