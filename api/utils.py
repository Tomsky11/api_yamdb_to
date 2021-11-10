from api_yamdb.settings import NOREPLY_YAMDB_EMAIL
from django.core import mail
from django.contrib.auth import get_user_model

User = get_user_model()


def generate_mail(to_email, code):
    subject = 'Код подтверждения'
    text_content = f'''
        Код подтверждения для работы с API YaMDB.
        Внимание, храните его в тайне {code}
    '''
    mail.send_mail(
        subject, text_content,
        NOREPLY_YAMDB_EMAIL, [to_email],
        fail_silently=False
    )
