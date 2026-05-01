from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import os
from myapp.models import User

@shared_task
def send_email_task(email_id, email, subject, body, sender_name):
    try:
        receiver_name = email.split("@")[0]

        html_content = render_to_string(
            "index.html",
            {
                "receiver_name": receiver_name,
                "sender_name": sender_name,
                "subject": subject,
                "body": body,
            }
        )

        text_content = strip_tags(html_content)

        email_msg = EmailMultiAlternatives(
            subject,
            text_content,
            os.getenv("EMAIL_HOST_USER"),
            [email]
        )

        email_msg.attach_alternative(html_content, "text/html")

        email_msg.send()

        user = User.objects.get(id=email_id)
        user.is_sent = True
        user.save()

        return f"Email sent to {email}"

    except Exception as e:
        return f"Error sending email to {email}: {str(e)}"