
import getpass
import os.path
import smtplib
import time
import ssl
import sys

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header


# 附件存放目录
ATTACHMENT_PATH = ''

# smtp服务
SMTP_SERVER = ''
SMTP_PORT =

# 邮箱账户
ACCOUNT = input('请输入邮箱账号：')
PASSWORD = getpass.getpass('请输入邮箱密码：')

# 发件人/收件人/抄送
FROM = ACCOUNT
TO = ['']
CC = ['']

# 邮件内容存放目录
CONTENT_01 = ''
CONTENT_02 = ''
CONTENT_03 = ''
CONTENT_04 = ''
CONTENT_05 = ''


# 构建邮件
def setup_msg(subject, email_content, attachment_name):

    msg = MIMEMultipart()

    msg['From'] = FROM
    msg['To'] = ','.join(TO)
    msg['Cc'] = ','.join(CC)
    msg['Subject'] = Header(subject, 'utf-8')

    msg.attach(MIMEText(email_content, 'html', 'utf-8'))

    try:
        with open(attachment_name, 'rb') as f:
            mime = MIMEApplication(f.read())
            mime.add_header('Content-Disposition', 'attachment', filename=attachment_name)

            msg.attach(mime)
        return msg
    except IOError as e:
        print('附件读取失败，原因：' + e)


# 分渠道发送邮件
def send_email():
    banks = list_dir(ATTACHMENT_PATH)
    for bank_name in banks:
        if bank_name == 'test01':
            send('test01', CONTENT_01, bank_name, '附件名')
            print('test01已发送')
            delay_send(10)
        elif bank_name == 'test02':
            zips = list_dir(ATTACHMENT_PATH + bank_name)
            for index, item in enumerate(zips):
                send('test02%d' % index+1, CONTENT_02, bank_name, item)
                print('test02第%d封邮件发送成功，剩余%d封' % (index + 1, len(zips) - index - 1))
                delay_send(10)
        elif bank_name == 'test03':
            send('test03', CONTENT_03, bank_name, '附件名')
            print('test03已发送')
            delay_send(10)
        elif bank_name == 'test04':
            send('test04', CONTENT_04, bank_name, '附件名')
            print('test04已发送')
            delay_send(10)
        elif bank_name == 'test05':
            send('test05', CONTENT_05, bank_name, '附件名')
            print('test05已发送')
        else:
            print('附件不符合规定，请检查')
            sys.exit(0)
    print('邮件已全部发送')


def send(subject, email_content_path, bank_name, attachment):
    os.chdir(ATTACHMENT_PATH + bank_name)
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context) as smtp:
            smtp.login(ACCOUNT, PASSWORD)

            msg = setup_msg(subject, get_email_content(email_content_path), attachment)

            print('邮件发送中')

            smtp.sendmail(FROM, TO + CC, msg.as_string())

            print('邮件发送完成')
    except smtplib.SMTPException as e:
        print('邮件发送失败，愿意：' + e)


def get_email_content(content_path):
    try:
        with open(content_path, 'rb') as content:
            return content.read()
    except IOError as e:
        print('获取邮件内容失败，原因：' + e)


def delay_send(second):
    count = 0
    while count < second:
        time_left = second - count
        print('-------- %d 秒后发送下一封邮件' % time_left)
        time.sleep(1)
        count += 1


# 过滤特殊文件 并 排序
def list_dir(path):
    name_list = os.listdir(path)
    for item in name_list:
        if item.startswith('.'):
            name_list.remove(item)
    name_list.sort()
    return name_list


if __name__ == '__main__':
    send_email()
