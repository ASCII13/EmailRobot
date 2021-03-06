<h1 align="center">EmailRobot</h1>
<p align="center">
    <a href="https://github.com/ASCII13/EmailRobot/stargazers"><img alt="stars" src="https://img.shields.io/github/stars/ASCII13/EmailRobot"></a>
    <a href="https://github.com/ASCII13/EmailRobot/network"><img alt="forks" src="https://img.shields.io/github/forks/ASCII13/EmailRobot"></a>
    <a href="https://github.com/ASCII13/EmailRobot/issues"><img alt="issues" src="https://img.shields.io/github/issues/ASCII13/EmailRobot"></a>
</p>

## 描述
一个自动发送邮件的 python 脚本，已进行脱敏处理，根据自身情况重新配置相关参数，即可使用

## 背景
由于业务需要，对接了5个银行的智能POS，每次发版都需要将不同的渠道包通过邮件提交给各银行审核，部分银行对于单封邮件附件大小还有限制，
导致每次发版写邮件耗费较长时间，EmailRobot由此诞生。

## 功能
* 在运行脚本的时候读取邮箱账户和密码，避免信息泄漏，提升安全性
* 根据附件数量智能发送邮件
* 邮件正文由HTML文件单独管理

## 代码导读
1. `send_email.py` 脚本文件
    - `ATTACHMENT_PATH` 附件存放路径
    - `SMTP_SERVER` SMTP服务地址
    - `SMTP_PORT` SMTP服务端口
    - `ACCOUNT` 邮箱账户
    - `PASSWORD` 邮箱密码/授权码
    - `FROM` 发件人
    - `TO` 收件人列表
    - `CC` 抄送列表
    - `CONTENT_xx` 邮件正文存放路径
 
2. `content.html` 邮件正文管理文件，邮件内容相关可以在这里编辑
