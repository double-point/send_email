# encoding:utf-8
# FileName: send_email
# Author:   wzg
# email:    1010490079@qq.com
# Date:     2019/12/1 下午 06:59
# Description: 邮件发送--带附件+html显示


import smtplib
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def set_content():
    # 邮件正文html模板
    content = """
    <html>
    <h1>html测试:</h1>
    <p>我是邮件正文</p>
    <a href="https://www.hao123.com/">hao123</a>
    <br>
    <a href="https://www.baidu.com/?tn=sitehao123">baidu</a>
    <br>
    <p><img src="cid:image" alt="图片" width="273" height="153"></a></p>
    <br>
    <a >我是知秋小梦的背景照片</a>
    </html>
    """

    return content


if __name__ == '__main__':
    # 发件人邮箱
    username = "xxxxxxx@qq.com"
    # QQ邮箱授权码
    password = "xxxxxxxxx"
    # 可设置多个收件人邮箱
    receivers = ['xxxxxxx@qq.com', 'yyyyyyy@qq.com']
    # 设置抄送人信息，可多个，逗号分隔
    cc = ['zzzzzzzz@qq.com']

    # 设置标题
    subject = "我是邮箱标题"
    # 设置内容
    content = set_content()
    # 创建MIMEMultipart对象，并封装相应的数据
    message = MIMEMultipart()
    # 封装标题
    message['Subject'] = Header(subject, 'gbk')
    # 封装发件人标识
    message['From'] = "每日推送"
    # 封装收件人和抄送人
    message['to'] = Header(",".join(receivers))
    message['Cc'] = Header(",".join(cc))
    # 生成邮件正文
    send_text = MIMEText(content, "html", "utf-8")
    # 封装邮件正文
    message.attach(send_text)

    # 读取图片并创建MIMEImage
    send_file_path = '此处为你的图片的本地地址'
    fp = open(send_file_path, 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    # 定义图片 ID，在 HTML 文本中引用
    msgImage.add_header('Content-ID', '<image>')
    message.attach(msgImage)

    # 读取csv文件作为附件
    send_file_path = "此处为你的附件在本地的路径"
    # 发送附件
    add_file = MIMEText(open(send_file_path, 'rb').read(), 'base64', 'gbk')
    add_file['Content-Type'] = 'application/octet-stream'
    # 设置文件名称
    add_file.add_header('Content-Disposition', 'attachment', filename="{}".format(send_file_path.split("\\")[-1]))
    message.attach(add_file)

    try:
        # 设置smtp的相关参数
        smtp_server = 'smtp.qq.com'
        smtp_port = 25
        smtp = smtplib.SMTP(smtp_server, smtp_port)
        # 登录
        smtp.login(username, password)
        # 发送
        smtp.sendmail(username, receivers + cc, message.as_string())
        smtp.quit()
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print("Error: 无法发送邮件" + e.strerror)