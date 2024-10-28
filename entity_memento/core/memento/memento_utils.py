from ..utils import inspect_request, get_client_ip


def memento_change_add_state_data_generator(sender, instance, ignore_keys):
    request = inspect_request()
    
    if sender.objects.filter(id=instance.id).exists():
        modification_type = "CHANGE"
        current_obj = sender.objects.get(id=instance.id)

        object_data = {}
        for key, value in current_obj.__dict__.items():
            if key in ignore_keys:
                continue
            if instance.__dict__.get(key) != value:
                object_data[key] = {'old' : value, 'new' : instance.__dict__.get(key)}
    else:
        modification_type = "ADD"
        object_data = instance.__dict__.copy()
        if '_state' in object_data:
            del object_data['_state']

    if object_data:
        state_data = {
            'modifier_user' : request.user.username if request and request.user else "UNKNOWN",
            'modifier_ip' : get_client_ip(request) or "UNKNOWN",
            'modification_type' : modification_type,
            'object_id' : instance.id or "UNKNOWN",
            'object_data' : object_data
        }

        return state_data
    
    return None


def memento_delete_state_data_generator(instance):
    request = inspect_request()
    
    modification_type = "DELETE"
    object_data = instance.__dict__

    if '_state' in object_data:
        del object_data['_state']

    state_data = {
        'modifier_user' : request.user.username or "UNKNOWN",
        'modifier_ip' : get_client_ip(request) or "UNKNOWN",
        'modification_type' : modification_type,
        'object_id' : instance.id,
        'object_data' : object_data
    }

    return state_data