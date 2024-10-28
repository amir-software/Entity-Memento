from ..models import Product
from .memento_utils import memento_change_add_state_data_generator, memento_delete_state_data_generator

from django.dispatch import receiver
from django.apps import apps
from django.dispatch import Signal
from django.db.models.signals import pre_delete, pre_save


insert_memento_state_signal = Signal()


@receiver(signal=insert_memento_state_signal)
def insert_state(model_name, data, **kwargs):

    model = apps.get_model('gin', model_name=model_name)
    model.objects.using('admin').create(**data)


@receiver(signal=[pre_save], sender=Product)
def product_changes_receiver(sender, instance, **kwargs):
    ignore_keys = ['_state',]
    state_data = memento_change_add_state_data_generator(sender, instance, ignore_keys=ignore_keys)
    if state_data:
        insert_memento_state_signal.send(sender="product_changes_receiver", model_name='ProductMemento', data=state_data)


@receiver(signal=[pre_delete], sender=Product)
def product_delete_receiver(sender, instance, **kwargs):
    state_data = memento_delete_state_data_generator(instance)
    insert_memento_state_signal.send(sender='product_delete_receiver', model_name='ProductMemento', data=state_data)