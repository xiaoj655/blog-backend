import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

def send_verify_mail(receive_email: str, verify_href: str):
  username = 'admin@bitdancing.com'
  password = 'bkk3DZ8bBLaDHbX'
  replyto = 'kk@bitdancing.com'
  receivers = [receive_email]

  msg = MIMEMultipart('alternative')
  msg['Subject'] = Header('验证您的邮箱')
  msg['From'] = formataddr(['validator', username])
  msg['Reply-to'] = replyto
  verify_href = "https://blog.bitdancing.com/verify/" + str(verify_href)
  print(verify_href)
  texthtml = MIMEText(f'<h1>Hello , <a href={verify_href}>click to confirm your email </a></h1>',
                      _subtype='html', _charset='utf-8')
  msg.attach(texthtml)

  try:
    client = smtplib.SMTP('smtpdm.aliyun.com', 80)
    client.set_debuglevel(0)
    client.login(username, password)
    client.sendmail(username, receivers, msg.as_string())
    client.quit()
    print('email send successfully')
    return True
  except Exception as e:
    print(e)
    return False