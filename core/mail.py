from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


def send_mail(to, template, context):
    html_content = render_to_string(f'core/email/{template}.html', context)
    text_content = render_to_string(f'core/email/{template}.txt', context)

    msg = EmailMultiAlternatives(context['subject'], text_content, settings.DEFAULT_FROM_EMAIL, [to])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def send_otp_code(request, email, code):
    context = {
        'subject': _('Store firouzjah send otp'),
        'uri': request.build_absolute_uri(reverse('core:send-otp')),
        'code': code
    }

    send_mail(email, 'send_otp', context)
