from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_new_user_email(
    subject, txt_template, to, context=None, html_template=None, fail_silently=True
):
    """
    Multipart message helper with template rendering.
    """

    context = context or {}
    context.update(
        {
            "title": subject,
        }
    )

    txt_body = render_to_string(txt_template, context)

    message = EmailMultiAlternatives(subject=subject, body=txt_body, to=[to, ])

    if html_template:
        body = render_to_string(html_template, context)
        message.attach_alternative(body, "text/html")
    message.send(fail_silently=fail_silently)