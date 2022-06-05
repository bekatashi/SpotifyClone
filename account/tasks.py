from django.core.mail import send_mail
from account.send_email import send_confirmation_email, send_reset_password
from SpotifyClone.celery import app
# from celery import Celery

# app = Celery('tasks', broker='pyamqp://guest@localhost//')
@app.task
def send_notification(user, singer):
    to_email = user.email
    send_mail(f'Hello u have followed{singer}', 'hope u will enjoy ur time listening to his music.', 'market.place@gmail.com', [to_email], fail_silently=False)


@app.task
def send_activation_code(user):
    send_confirmation_email(user)


def send_reset_pass(user):
    send_reset_password(user)
