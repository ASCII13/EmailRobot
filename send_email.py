
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
TO = []
CC = []

# 邮件正文模版
TEMPLATE = ''


def generate_msg(subject, body, attachment_name):
    """
    构建邮件
    :param subject: 标题
    :param body: 正文
    :param attachment_name: 附件
    :return:
    """
    msg = MIMEMultipart()

    msg['From'] = FROM
    msg['To'] = ','.join(TO)
    msg['Cc'] = ','.join(CC)
    msg['Subject'] = Header(subject, 'utf-8')

    msg.attach(MIMEText(body, 'html', 'utf-8'))

    try:
        with open(attachment_name, 'rb') as f:
            mime = MIMEApplication(f.read())
            mime.add_header('Content-Disposition', 'attachment', filename=attachment_name)

            msg.attach(mime)
        return msg
    except IOError as e:
        print('附件读取失败，原因：' + e)


def send_email():
    """
    分渠道发送
    你可以在这里构建自己的发送逻辑
    :return:
    """
    banks = list_dir(ATTACHMENT_PATH)
    # example
    if 'a' in banks:
        send('这是邮件标题', TEMAPLTE, 'a', '这是附件名称')
        print('a已发送')
        delay_send(6)
    else:
        print('未匹配到相关目录，请检查')
        sys.exit(0)
    print('邮件已全部发送')


def send(subject, email_content_path, bank_name, attachment):
    """
    发送邮件
    :param subject: 邮件标题
    :param email_content_path: 邮件正文路径
    :param bank_name: 银行名称
    :param attachment: 附件
    :return:
    """
    os.chdir(ATTACHMENT_PATH + bank_name)
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context) as smtp:
            smtp.login(ACCOUNT, PASSWORD)

            msg = generate_msg(subject, get_email_content(email_content_path), attachment)

            print('邮件发送中')

            smtp.sendmail(FROM, TO + CC, msg.as_string())

            print('邮件发送完成')
    except smtplib.SMTPException as e:
        print(bank_name + '邮件发送失败，原因：' + e)


def get_email_content(content_path):
    """
    读取邮件正文
    :param content_path: 正文模版路径
    :return:
    """
    try:
        with open(content_path, 'rb') as content:
            return content.read()
    except IOError as e:
        print('邮件正文读取失败，原因：' + e)


def delay_send(second):
    count = 0
    while count < second:
        time_left = second - count
        print('-------- %d 秒后发送下一封邮件' % time_left)
        time.sleep(1)
        count += 1


def list_dir(path):
    """
    过滤特殊文件
    :param path: 附件路径
    :return: 
    """
    name_list = os.listdir(path)
    for item in name_list:
        if item.startswith('.'):
            name_list.remove(item)
    name_list.sort()
    return name_list


if __name__ == '__main__':
    send_email()
