import smtplib
from email import utils
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import openpyxl
import json
import os


class AhmEmail():
    '''
    通过AhmEmail类发送email
    '''

    def __init__(self, username: str = '2569674866@qq.com', login_token: str = "zqoppgniszwqeaej", smtp_host: str = 'smtp.qq.com') -> None:
        '''
        初始化AhmEmail类
        username: 用户名
        login_token: 登录token
        smtp_host: smtp服务器地址
        '''
        self.username = username
        self.login_token = login_token
        self.smtp_host = smtp_host
        self.server = None

    def __enter__(self):
        '''用于with语句的上下文管理器'''
        self.server = smtplib.SMTP_SSL(self.smtp_host, 465)
        try:
            self.server.login(self.username, self.login_token)
        except smtplib.SMTPAuthenticationError:
            print("认证失败，请检查用户名和密码")
            raise
        except smtplib.SMTPException as e:
            print(f"无法连接到SMTP服务器: {e}")
            raise
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        '''确保在退出时关闭服务器连接'''
        if self.server:
            self.server.quit()

    def send_text_email(self, recipient: str, subject: str, body: str, json_data: dict = None, attachment_filename: str = 'attachment.xlsx') -> None:
        '''
        发送邮件，选择性添加表格附件,表格数据必须为扁平结构\n
        recipient: 收件人邮箱地址\n
        subject: 邮件主题\n
        body: 邮件内容\n
        json_data: 可选，传入的JSON数据用于生成Excel表格附件\n
        attachment_filename: 可选，生成的表格文件名
        '''
        try:
            # 创建一个带附件的邮件对象
            msg = MIMEMultipart()
            msg['From'] = utils.formataddr(('Sender Name', self.username))
            msg['To'] = utils.formataddr(('Recipient Name', recipient))
            msg['Subject'] = subject

            # 添加邮件正文
            msg.attach(MIMEText(body, 'plain', 'utf-8'))

            # 如果传入了JSON数据，生成Excel附件
            if json_data:
                # 创建一个新的Excel工作簿
                wb = openpyxl.Workbook()
                ws = wb.active

                # 写入数据头（列名）
                headers = list(json_data.keys())
                ws.append(headers)

                # 逐行写入数据
                rows = zip(*json_data.values())
                for row in rows:
                    ws.append(row)

                # 保存为Excel文件
                wb.save(attachment_filename)

                # 读取文件并添加为附件
                with open(attachment_filename, 'rb') as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition', f'attachment; filename="{os.path.basename(attachment_filename)}"')
                    msg.attach(part)

            # 发送邮件
            self.server.sendmail(self.username, [recipient], msg.as_string())
            print(f"邮件已发送至 {recipient}")
        except smtplib.SMTPRecipientsRefused:
            print(f"收件人 {recipient} 被拒绝")
        except smtplib.SMTPException as e:
            print(f"发送邮件时发生错误: {e}")
        finally:
            # 删除生成的附件文件
            if json_data and os.path.exists(attachment_filename):
                os.remove(attachment_filename)


if __name__ == '__main__':
    data_dict = {
        'name': ['Alice', 'Bob', 'Charlie'],
        'age': [25, 30, 35],
        'city': ['New York', 'Los Angeles', 'Chicago']
    }
    with AhmEmail() as email:
        email.send_text_email('2569674866@qq.com', '测试邮件',
                              '这是一封测试邮件', json_data=data_dict)
