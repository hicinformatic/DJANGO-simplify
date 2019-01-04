from django.db.models.signals import post_save
from django.dispatch import receiver
    
from .apps import SimplifyConfig as conf
from .models import (Method)

logger = conf.logger

@receiver(post_save, sender=Method)
def MethodWriteCertificate(sender, instance, created, **kwargs):
    logger(7, 'test')
    if instance.tls and instance.certificate is not None:
        instance.write_certificate():

#if conf.scheduler.enable:
#    from .models import (Script, Task)
#    @receiver(post_save, sender=Task)
#    def TaskStarting(sender, instance, created, **kwargs):
#        if instance.status == conf.choices.status_order:
#            instance.prepare()
#            instance.can_run() 
#        elif instance.status == conf.choices.status_ready:
#            instance.start_task()
#
#    @receiver(post_save, sender=Script)
#    def ScriptStarting(sender, instance, created, **kwargs):
#        instance.script_write(instance.script_path())