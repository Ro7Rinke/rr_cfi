from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import ValidationError

from .utils import generateInstallmentsByEntry
from .models import Entry

@receiver(post_save, sender=Entry)
def afterSaveEntry(sender, instance, created, **kwargs):
    if(created):
        status, error = generateInstallmentsByEntry(instance)
        if not status:
            raise ValidationError(error)
        
        print('Entry created')
    else:
        print('Entry updated')