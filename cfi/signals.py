from django.forms import ValidationError
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from .middleware import getCurrentUser
from .utils import generateInstallmentsByEntry
from .models import Entry, Tag

@receiver(post_save, sender=Entry)
def afterSaveEntry(sender, instance, created, **kwargs):
    if(created):
        status, error = generateInstallmentsByEntry(instance)
        if not status:
            instance.delete()
            raise ValidationError(error)
        
        print('Entry created')
    else:
        print('Entry updated')

@receiver(pre_save, sender=Tag)
def check_user_association(sender, instance, **kwargs):
    # Aqui você pode acessar o usuário autenticado de outras maneiras
    # Por exemplo, se estiver no contexto de uma view
    if isinstance(instance, Tag):
        user = instance.id_user

    if user is None:
        raise ValueError("O usuário não pode ser nulo.")

    if not isinstance(user, User):
        raise ValueError("id_user deve ser uma instância de User.")
    
    current_user = getCurrentUser()
    if user.id != current_user.id:
        raise ValueError('Usuário não possúi acesso')