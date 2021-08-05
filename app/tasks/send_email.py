from . import celery
from app import mail
from flask_mail import Message as Mail_message
import time

@celery.task()
def send_email(receiver_email: str, content: str) -> str:
    """寄送mail。

    :param receiver_email: 接收者
    :param content: 內文
    :return: str
    """
    time.sleep(5)
    message = Mail_message(
        subject="Subject主題",  # 主題
        sender='123',  # 寄件人
        recipients=[receiver_email],  # 收件人
        body=content,  # 內文訊息
    )
    mail.send(message)
    return '已寄發驗證信'
