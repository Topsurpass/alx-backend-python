from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory
from django.contrib.auth.models import User

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    """Signal to create a notification when a new message is sent"""
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )


@receiver(pre_save, sender=Message)
def log_edited_msg(sender, instance, **kwargs):
    """Signal to log the edited message"""	
    if instance.pk:
        try:
            original_message = Message.objects.get(pk=instance.pk)
            if original_message.content != instance.content:
                MessageHistory.objects.create(
                    message=original_message,
                    old_content=original_message.content,
                    edited_by=instance.sender
                )
                instance.edited = True
        except Message.DoesNotExist:
            pass
        
@receiver(post_delete, sender=User)
def cleanup_user_related_data(sender, instance, **kwargs):
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(user=instance).delete()
    MessageHistory.objects.filter(edited_by=instance).delete()