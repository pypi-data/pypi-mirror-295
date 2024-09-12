from typing import Tuple
from web3 import Web3

def redis_add_contact(redis_client, user, name, address) -> Tuple[int,str]:
    if not Web3.is_address(address):
        return 410, f"Input address:{address} is not a valid ethereum address"
    key = user + '_' + name
    lower_key = key.lower()
    if_exist = redis_client.hget(f"contact:{lower_key}","address")
    if if_exist:
        return 420, f"Already added {name} to contacts"
    redis_client.hset(f"contact:{lower_key}","address",address)
    return 200, f"Added {name}({address}) to contacts successfully"

def get_contact_address(redis_client, user, contact, w3):
    if not Web3.is_address(contact):
        name = contact
        key = user + '_' + name
        lower_key = key.lower()
        to = redis_client.hget(f"contact:{lower_key}","address")
        if not to:
            return 404, f"Cannot find {name} on contact"
    else:
        to = contact
    address = w3.to_checksum_address(to)
    return 200, address
    
def redis_show_contact(redis_client, user, name):
    res = None
    try:
        prefix = f"contact:{user}"
        name_address_map = get_name_address_mapping(redis_client, prefix)
        if name is not None:
            name_address_map = { name: name_address_map[name] }
        res = generate_markdown(name_address_map)
    except Exception as e:
        res = e
        return 500, res
    return 200, res

def get_name_address_mapping(redis_client, prefix: str):
    name_address_map = {}
    for key in redis_client.scan_iter(match=f"{prefix}*"):
        # key: contact:user_address_name
        name = key.split('_')[-1]
        address = redis_client.hget(key, 'address')
        if address:
            name_address_map[name] = address
    return name_address_map

def generate_markdown(mapping):
    markdown_lines = ["| Name | Address |", "|------|---------|"]
    for name, address in mapping.items():
        markdown_lines.append(f"| {name} | {address} |")
    return "\n".join(markdown_lines)