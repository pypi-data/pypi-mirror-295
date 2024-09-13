from django.conf import settings as _settings
from django.core.mail import send_mail as _send_mail
from django.utils.html import strip_tags as _strip_tags

__all__ = [
    "send_mail_template",
    "send_html_mail",
]


def send_mail_template(subject, html_message, plain_message, email):
    _send_mail(
        subject,
        plain_message,
        _settings.DEFAULT_FROM_EMAIL,
        [
            email,
        ],
        html_message=html_message,
    )


def send_html_mail(
    subject: str,
    html_message: str,
    email: str | list[str],
):
    """
    Send an email with HTML content.

    :param subject: The subject of the email.
    :param html_message: The HTML content of the email.
    :param email: The email address of the recipient or a list of email addresses.
    """
    recipient_list = email if isinstance(email, list) else [email]
    message = _strip_tags(html_message)

    _send_mail(
        subject,
        message,
        _settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        html_message=html_message,
    )
