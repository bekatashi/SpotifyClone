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
def send_activation_code(to_email, code):
    # send_confirmation_email(email,code,user)
    full_link = f'http://localhost:8000/api/v1/accounts/activate/{code}'
    send_mail('Hello! please enter ur account', f'Please open the following link {full_link}, to activate it', 'forexample@gmail.com', [to_email, ], fail_silently=False)

@app.task
def send_reset_pass(code, email):
    send_reset_password(code, email)
