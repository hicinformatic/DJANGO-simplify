from django.db.models.signals import post_save
from django.dispatch import receiver
    
from .apps import SimplifyConfig as conf
from .models import Task

@receiver(post_save, sender=Task)
def TaskStarting(sender, instance, created, **kwargs):
    if created:
        instance.prepare()
        instance.can_run()
    else:
        if instance.status == conf.choices.status_ready:
            instance.start_task()