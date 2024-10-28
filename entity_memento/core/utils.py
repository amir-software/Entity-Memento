import inspect
import ast


def get_client_ip(request):
    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            if ',' in x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = x_forwarded_for
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    except:
        return "UNKNOWN"


def inspect_request():
    for frame_record in inspect.stack():
        if frame_record[3]=='get_response':
            request = frame_record[0].f_locals['request']

            return request
    return None


def get_filter_params(params, extra_to_remove=[]):
    filter_params = {}
    fields_to_remove = ['page', 'page_size', 'access_token'] + extra_to_remove
    for prm in params:
        if prm not in fields_to_remove:
            if '[' in params.get(prm):
                filter_params[prm] = ast.literal_eval(params.get(prm))
            else:
                filter_params[prm] = params.get(prm)
    return filter_params