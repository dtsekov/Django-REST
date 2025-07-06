from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Envía un email al usuario cuando se crea el token de reseteo.
    """
    user = reset_password_token.user
    # Construye la URL que consumirá tu frontend en Vue
    reset_url = "{}?token={}".format(
        instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
        reset_password_token.key
    )

    context = {
        'email': user.email,
        'reset_password_url': reset_url,
        'current_user': user,
    }

    # Renderiza plantillas: texto plano y HTML
    subject = "[Mentoría] Restablecer tu contraseña"
    text_body = render_to_string('password_reset/email.txt', context)
    html_body = render_to_string('password_reset/email.html', context)

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=None,  # usa DEFAULT_FROM_EMAIL
        to=[user.email],
    )
    msg.attach_alternative(html_body, "text/html")
    msg.send()