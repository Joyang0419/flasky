from app import mail
from flask_mail import Message as Mail_message
# 多線程工具
from threading import Thread


def async_send_email(app, message):
    """非同步寄信

    :param app: flask app
    :param message: email內仍
    """
    with app.app_context():
        mail.send(message)


def send_email(receiver_email: str, content: str) -> str:
    """寄送mail。

    :param receiver_email: 接收者
    :param content: 內文
    :return: str
    """
    message = Mail_message(
        subject="Subject主題",  # 主題
        sender='123',  # 寄件人
        recipients=[receiver_email],  # 收件人
        body=content,  # 內文訊息
    )
    # 多執行續
    from flasky import app
    thr = Thread(target=async_send_email, args=[app, message])
    thr.start()
    return '已寄發驗證信'
