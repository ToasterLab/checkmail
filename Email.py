import re
import socket
import smtplib
import dns.resolver


class Email:
    def __init__(self, address, from_address=f"root@{socket.gethostname()}"):
        self.address = address
        self.from_address = from_address
        self.username = self.get_username()
        self.domain = self.get_domain()
        self.valid = self.check_deliverability()

    def get_username(self):
        username = str(self.address.split('@')[0])
        return username

    def get_domain(self):
        domain = str(self.address.split('@')[1])
        return domain

    def validate_email(self):
        EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        match = re.match(EMAIL_REGEX, self.address)
        return {'result': (match is not None)}

    def check_dns(self):
        try:
            dns_records = dns.resolver.query(self.domain, 'MX')
        except dns.resolver.NXDOMAIN:
            return {'result': False, 'message': 'Invalid domain name'}
        except dns.resolver.NoAnswer:
            return {'result': False, 'message': 'No MX records found'}
        mx_record = str(dns_records[0].exchange)
        self.mx = mx_record
        return {'result': True, 'mx': mx_record}

    def check_smtp(self):
        try:
            server = smtplib.SMTP()
            server.connect(self.mx)
            server.helo(server.local_hostname)
            server.mail(self.from_address)
            code, message = server.rcpt(self.address)
            server.quit()
            if code == 250:
                return {'result': True}
            else:
                return {'result': False, 'message': str(message)}
        except smtplib.SMTPServerDisconnected:
            return {'result': False, 'message': "SMTP server unexpectedly disconnected"}

    def check_deliverability(self):
        validity = {'overall': False}

        syntax_valid = self.validate_email()
        validity['syntax'] = syntax_valid

        if not syntax_valid:
            return validity

        dns_valid = self.check_dns()
        validity['dns'] = dns_valid

        if not dns_valid['result']:
            return validity

        smtp_valid = self.check_smtp()
        validity['smtp'] = smtp_valid

        if smtp_valid['result']:
            validity['overall'] = True

        return validity

    def __str__(self):
        return str(vars(self))
