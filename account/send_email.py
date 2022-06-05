from django.core.mail import send_mail


def send_confirmation_email(user):
    code = user.activation_code
    full_link = f'http://localhost:8000/api/v1/accounts/activate/{code}'
    to_email = user.email
    send_mail('Hello! please enter ur account', f'Please open the following link {full_link}, to activate it', 'forexample@gmail.com', [to_email, ], fail_silently=False)


def send_reset_password(user):
    code = user.activation_code
    to_email = user.email
    send_mail(
        'Changing ur password',
        f'Ur code: {code}',
        'forexample@gmail.com',
        {to_email},
        fail_silently=False,
    )

def send_notification(user, singer):
    to_email = user.email
    send_mail(f'Hello u have followed{singer}', 'hope u will enjoy ur time listening to his music.', 'market.place@gmail.com', [to_email], fail_silently=False)

