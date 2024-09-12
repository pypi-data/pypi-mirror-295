from actions_lib.utils.contact_tool import redis_add_contact, redis_show_contact

def add_contact(name, address, step, **kwargs):
    redis_client = kwargs.get('redis_client')
    executor =  kwargs.get('executor')
    code, res = redis_add_contact(redis_client, executor, name, address)
    return {
        'result': { 'code': code, 'content': res },
        'action': None, 
        'next_action': None 
    }

def show_contact_by_name(name, step, **kwargs):
    redis_client = kwargs.get('redis_client')
    executor =  kwargs.get('executor')
    code, res = redis_show_contact(redis_client, executor, name)
    return {
        'result': { 'code': code, 'content': res },
        'action': None, 
        'next_action': None 
    } 

def show_all_contact(step, **kwargs):
    redis_client = kwargs.get('redis_client')
    executor =  kwargs.get('executor')
    code, res = redis_show_contact(redis_client, executor, None)
    return {
        'result': { 'code': code, 'content': res },
        'action': None, 
        'next_action': None 
    }  