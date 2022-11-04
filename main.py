
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
from typing import AnyStr


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
TEMPLATE = 'template.html'


def generate_mail(subject: str, body: str, attachment_name: str) -> MIMEMultipart:
    """
    构建邮件
    :param subject: 标题
    :param body: 正文
    :param attachment_name: 附件名称
    :return:
    """
    mail = MIMEMultipart()

    mail['From'] = FROM
    mail['To'] = ','.join(TO)
    mail['Cc'] = ','.join(CC)
    mail['Subject'] = Header(subject, 'utf-8')

    mail.attach(MIMEText(body, 'html', 'utf-8'))

    try:
        with open(attachment_name, 'rb') as f:
            mime = MIMEApplication(f.read())
            mime.add_header('Content-Disposition', 'attachment', filename=attachment_name)

            mail.attach(mime)
        return mail
    except IOError as e:
        print(f'附件读取失败：{e}')


def send_email():
    """
    分渠道发送
    你可以在这里构建自己的发送逻辑
    :return:
    """
    banks = get_files_name(ATTACHMENT_PATH)
    # example
    if 'a' in banks:
        send('这是邮件标题', TEMAPLTE, 'a', '这是附件名称')
        print('a已发送')
        delay(6)
    else:
        print('未匹配到相关目录，请检查')
        sys.exit(0)
    print('邮件已全部发送')


def send(subject: str, template_path: str, sub_path: str, attachment_name: str) -> None:
    """
    发送邮件
    :param subject: 邮件标题
    :param template_path: 邮件模版路径
    :param sub_path: 对应银行的目录名称
    :param attachment_name: 附件名称
    :return:
    """
    os.chdir(f'{ATTACHMENT_PATH}{sub_path}')
    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context) as smtp:
            smtp.login(ACCOUNT, PASSWORD)

            mail = generate_mail(subject, get_mail_template(template_path), attachment_name)

            print('邮件正在发送，请稍后...')

            smtp.sendmail(FROM, TO + CC, mail.as_string())

            print(f'{sub_path}邮件发送完成')
    except smtplib.SMTPException as e:
        print(f'{sub_path}邮件发送失败：{e}')

        
def get_mail_template(path: str) -> AnyStr:
    """
    读取邮件模版
    :param path: 模版路径
    :return: 
    """
    try:
        with open(path, 'rb') as content:
            return content.read()
    except IOError as e:
        print(f'邮件模版读取失败：{e}')


def delay(second: int) -> None:
    count = 0
    while count < second:
        time_left = second - count
        print(f'将在 {time_left} 秒后发送下一封邮件')
        time.sleep(1)
        count += 1


def get_files_name(path: str) -> list:
    """
    获取指定目录下包含的文件和目录的名称（过滤.开头的隐藏文件）
    :param path: 目录路径
    :return: 名称列表
    """
    names = os.listdir(path)
    for name in names:
        if name.startswith('.'):
            names.remove(name)
    names.sort()
    return names


if __name__ == '__main__':
    send_email()
