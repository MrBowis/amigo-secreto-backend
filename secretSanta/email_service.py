from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string


def send_secret_santa_assignment_email(participant_name, participant_email, receiver_name, event_name, event_id):
    """
    Send email to participant with their secret santa assignment
    """
    subject = f'Tu Amigo Secreto en "{event_name}"'
    
    message = f"""
Hola {participant_name},

¡Se ha realizado el sorteo de Amigo Secreto para "{event_name}"!

Tu amigo secreto es: {receiver_name}

Recuerda que esto es un secreto, no le digas a nadie a quién le tocaste.

Para ver más detalles y la lista de deseos de {receiver_name}, visita:
http://localhost:3000/my-draws?email={participant_email}

¡Que disfrutes preparando tu regalo!

---
Amigo Secreto App
    """
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [participant_email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email to {participant_email}: {str(e)}")
        return False


def send_draw_completed_email(creator_email, event_name, participants_count):
    """
    Send notification to event creator that draw is complete
    """
    subject = f'Sorteo completado: "{event_name}"'
    
    message = f"""
Hola,

El sorteo de "{event_name}" se ha completado exitosamente.

Se enviaron correos a {participants_count} participantes con sus asignaciones.

¡Que disfruten su Amigo Secreto!

---
Amigo Secreto App
    """
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [creator_email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email to creator: {str(e)}")
        return False
