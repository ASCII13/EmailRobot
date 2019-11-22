
import getpass
import os.path
import smtplib
import time
import ssl

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header


# 附件存放目录
ATTACHMENT_PATH = ''

# 附件列表
attachment_list = []

# smtp服务
SMTP_SERVER = ''
SMTP_PORT = xxx

# 邮箱账户
ACCOUNT = input('请输入邮箱账户：')
PASSWORD = getpass.getpass('请输入邮箱密码：')

# 发件人/收件人/抄送
FROM = ACCOUNT
TO = ['']
CC = ['']

# 邮件内容路径 html
ABC = ''


# 邮件标题
SUBJECT = ''


def setup_msg(sender, receiver, carbon_copy, subject, attactment_name):

    msg = MIMEMultipart()

    msg['From'] = sender
    msg['To'] = ','.join(receiver)
    msg['Cc'] = ','.join(carbon_copy)
    msg['Subject'] = Header(subject, 'utf-8')

    msg.attach(MIMEText(get_email_content(ABC), 'html', 'utf-8'))

    try:
        with open(attactment_name, 'rb') as f:
            mime = MIMEApplication(f.read())
            mime.add_header('Content-Disposition', 'attachment', filename=attactment_name)

            msg.attach(mime)

        return msg
    except IOError as e:
        print('附件读取失败，原因：' + e)


# 获取待发送附件
def get_attachment():

    att_list = os.listdir(ATTACHMENT_PATH)

    print('---------------- 待发送附件如下：')

    for att_name in att_list:
        if att_name.startswith('.'):
            continue
        else:
            attachment_list.append(att_name)
            print(att_name)


def send_email(attachment):
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context) as smtp:
        smtp.login(ACCOUNT, PASSWORD)
        msg = setup_msg(FROM, TO, CC, SUBJECT, attachment)

        print('邮件发送中')

        smtp.sendmail(FROM, TO, msg.as_string())

        print('邮件发送完成')


def get_email_content(path):
    try:
        with open(UNION, 'rb') as content:
            return content.read()
    except IOError as e:
        print('获取邮件内容失败，原因：' + e)


def delay_send(second):
    count = 0
    while count < second:
        timeLeft = second - count
        print('-------- %d 秒后发送下一封邮件' %timeLeft)
        time.sleep(1)
        count += 1


if __name__ == '__main__':
    os.chdir(ATTACHMENT_PATH)

    get_attachment()

    for i in range(len(attachment_list)):
        try:
            send_email(attachment_list[i])
            print('---------------- 第%d封邮件发送成功，剩余%d封' % (i + 1, len(attachment_list) - i - 1))
        except smtplib.SMTPException as e:
            print('---------------- 第%d封邮件发送失败，原因：%s' % (i + 1, e))
