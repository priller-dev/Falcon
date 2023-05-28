"""this file for sending emails and something related with emails"""
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from root.settings import EMAIL_HOST_USER


def send_verification_link(subject: str, username: str, to_email: str, link: str) -> None:
    """this function sends email verification as html to particular user"""
    context = {
        'name': username,
        'link': link
    }

    html_content = render_to_string('authentication/email_page.html', context)

    msg = EmailMessage(subject, body=html_content, from_email=EMAIL_HOST_USER, to=[to_email])
    msg.content_subtype = 'html'
    msg.send()
