# [checkmail](https://45q7j852e6.execute-api.ap-southeast-1.amazonaws.com/prod/)

* Checks validity of an email address
  * regex check
  * deliverability check (does domain exist)
  * smtp check (can connect to mailserver & is mailserver accepting mail?) <= this should largely be ignored

## API

GET /<string: email_address>

e.g. [GET /bill@microsoft.com](https://45q7j852e6.execute-api.ap-southeast-1.amazonaws.com/prod/bill@microsoft.com)

```
{
  "address": "bill@microsoft.com", 
  "domain": "microsoft.com", 
  "from_address": "root@localhost", 
  "mx": "microsoft-com.mail.protection.outlook.com.", 
  "username": "bill", 
  "valid": {
    "dns": {
      "mx": "microsoft-com.mail.protection.outlook.com.", 
      "result": true
    }, 
    "overall": false, 
    "smtp": {
      "message": "b'5.7.606 Access denied, banned sending IP [219.75.75.249]. To request removal from this list please visit https://sender.office.com/ and follow the directions. For more information please go to  http://go.microsoft.com/fwlink/?LinkID=526655 (AS16012609) [DM3NAM06FT006.Eop-nam06.prod.protection.outlook.com]'", 
      "result": false
    }, 
    "syntax": {
      "result": true
    }
  }
}
```

## Considerations

### Fixed IP Address

This should probably be run from a system with a fixed IP address. Some mailservers (like Zoho) reject all mail from dynamic IP addresses:

>Mail rejected by <Zoho Mail> for policy reasons. We generally do not accept email from dynamic IP's as they are typically used to deliver unauthenticated SMTP e-mail to an Internet mail server. http://www.spamhaus.org maintains lists of dynamic and residential IP addresses. If you are not an email/network admin please contact your E-mail/Internet Service Provider for help. Email/network admins, please contact <support@zohomail.com> for email delivery information and support

### SMTP Unreliability

checkmail connects to the SMTP server of the recipient to determine the existence and validity of the mailbox. This is often ineffective. Many mailservers ban programs that connect but fail to actually send an email because this behavior is characteristic of spammer validation bots.

The SMTP field in the API result is hence largely unreliable.