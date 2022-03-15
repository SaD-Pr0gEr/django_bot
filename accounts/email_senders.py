import os

from django.core.mail import send_mail
from dotenv import load_dotenv

load_dotenv()


def confirm_email(user_email, confirm_url, domain):
    subject = "HI there!"
    send_mail(
        subject,
        f"Привет! Подтвердите почту на сайте {domain} по ссылке \n {confirm_url} \n Если это не вы то просто "
        f"игноррируйте",
        os.getenv("EMAIL_USER"),
        [user_email],
        auth_user=os.getenv("EMAIL_USER"),
        auth_password=os.getenv("EMAIL_PASSWORD")
    )
