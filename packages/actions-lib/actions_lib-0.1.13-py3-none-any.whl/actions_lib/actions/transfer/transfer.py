from typing import Tuple

from web3 import Web3
from eth_utils.abi import function_abi_to_4byte_selector, collapse_if_tuple

from actions_lib.actions.type import Action, ActionData
from actions_lib.utils.contact_tool import get_contact_address

token_mapping = {
    "ethereum": {
        "usdc": "0xA0b86991C6218b36c1d19D4a2e9EB0cE3606EB48",  # USDC on Ethereum
        "usdt": "0xdAC17F958D2ee523a2206206994597C13D831ec7",  # USDT on Ethereum
    },
    "bsc": {
        "usdc": "0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d",  # USDC on BSC
        "usdt": "0x55d398326f99059ff775485246999027b3197955",  # USDT on BSC
    },
    "base": {
        "usdc": "0x45b58118a5374dccf7fd6f3f66c66278ab7473d9",  # USDC on Base
    },
}


allowance_abi = """
[
  {
    "constant": true,
    "inputs": [
      {
        "name": "_owner",
        "type": "address"
      },
      {
        "name": "_spender",
        "type": "address"
      }
    ],
    "name": "allowance",
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  }
]
"""

control_contract_abi = [
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "from",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "to",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "value",
        "type": "uint256"
      }
    ],
    "name": "controlTransferFrom",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "owner_",
        "type": "address"
      }
    ],
    "name": "setOwner",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "token_",
        "type": "address"
      }
    ],
    "name": "setToken",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [],
    "stateMutability": "nonpayable",
    "type": "constructor"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "token_",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "value",
        "type": "uint256"
      }
    ],
    "name": "withdraw",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "stateMutability": "payable",
    "type": "receive"
  },
  {
    "inputs": [],
    "name": "TRANSFER",
    "outputs": [
      {
        "internalType": "bytes4",
        "name": "",
        "type": "bytes4"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "TRANSFERFROM",
    "outputs": [
      {
        "internalType": "bytes4",
        "name": "",
        "type": "bytes4"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  }
]

chain_id_mapping = {
  'base': '0x14a34',
  'ethereum': '0xaa36a7',
  'eth': '0xaa36a7',
  'bsc': '0x38'
}

erc20_approve_abi = """
[{
  "constant": false,
  "inputs": [
    {
      "name": "_spender",
      "type": "address"
    },
    {
      "name": "_value",
      "type": "uint256"
    }
  ],
  "name": "approve",
  "outputs": [
    {
      "name": "",
      "type": "bool"
    }
  ],
  "payable": false,
  "stateMutability": "nonpayable",
  "type": "function"
}]
"""

def transfer(receiver, amount, step, run_mode = 'auto', chain = "base", token = "usdc", **kwargs):
    """
      kwargs need to include providers from different chains
      for example: 
      providers: {
        "base": "https://base.g.alchemy.com/v2/7mj7kTlPr2M1AiMu42Z3Tbwwg8DyOHPk", 
        "ethereum": "https://ethereum.g.alchemy.com/v2/7mj7kTlPr2M1AiMu42Z3Tbwwg8DyOHPk" 
      }
    """
    print(f"receiver: {receiver}, amount: {amount}, run_mode: {run_mode}, chain: {chain}, token: {token}, kwargs: {kwargs}, step: {step}")
    token_raw = token
    info = None
    executor = kwargs.get("executor")
    redis_client = kwargs.get("redis_client")
    control_address = kwargs.get('control_address')
    control_contract = kwargs.get('contract')
    private_key = kwargs.get('private_key')
    spender_address =  kwargs.get('spender_address')
    blockchain_explore = kwargs.get('blockchain_explore')
    providers = kwargs.get("providers")
    provider = Web3.HTTPProvider(providers[chain.lower()])
    provider.middlewares.clear()
    w3 = Web3(provider)
    if run_mode == 'auto':
      """ check executor approved allowance """
      token = w3.to_checksum_address(token_mapping[chain.lower()][token.lower()]) 
      token_contract = w3.eth.contract(address=token, abi=allowance_abi)
      allowance = token_contract.functions.allowance(Web3.to_checksum_address(executor), spender_address).call()
      allowance_normalized = Web3.from_wei(allowance, 'mwei')
      print(f"allowance_normalized: {float(allowance_normalized)}")
      if float(allowance_normalized) < float(amount):
          # active_chain_key = f"user:{executor}:active_chain"
          # active_chain = redis_client.get(active_chain_key)
          # if not active_chain:
          #   active_chain = "base"
          # if active_chain.lower() != chain.lower():
          #   action_params = {
          #     "func": "wallet_switchEthereumChain",
          #     "chainId": chain_id_mapping[chain.lower()]
          #   }
          #   action_data = ActionData(func='', group='', params=action_params)
          #   action = Action(msg=None, type='setting', data=action_data.__dict__)
          #   next_params = {
          #     'receiver': receiver,
          #     'amount': amount,
          #     'chain': chain,
          #     'token': token_raw,
          #     'run_mode': run_mode
          #   }
          #   next_action_data = ActionData(func='transfer', group='transfer', params=next_params)
          #   next_action = Action(msg=None, type='backend', data=next_action_data.__dict__)

          #   return {
          #     'result': { 'code': 403, 'content': 'Incorrect network, switching to the correct network for you.' },
          #     'action': action.__dict__,
          #     'next_action': next_action.__dict__
          #   }
          # else:
          action_params = {
            "func": "approve",
            "chainId": chain_id_mapping[chain.lower()],
            'contract': token,
            'to': spender_address,
            'amount': float(amount),
            'abi': erc20_approve_abi
          }
          action_data = ActionData(func='', group='', params=action_params)
          action = Action(msg=None, type='wallet', data=action_data.__dict__)

          code, res = get_contact_address(redis_client, executor, receiver, w3)
          if code != 200:
              info = {"content": f"Cannot find {receiver} on contact", "code": 420}
              return {
                'result': info,
                'action': None, 
                'next_action': None 
              }
          value = float(amount)
          receiver = res
          to = w3.to_checksum_address(receiver)
          next_params = {
            'receiver': to,
            'amount': amount,
            'chain': chain,
            'token': token_raw,
            'run_mode': run_mode
          }
          next_action_data = ActionData(func='transfer', group='transfer', params=next_params)
          next_action = Action(msg=None, type='backend', data=next_action_data.__dict__)
          return {
            'result': { "code": 401, "content": "Insufficient allowance, proceeding with approval." },
            'action': action.__dict__,
            'next_action': next_action.__dict__
          }
      code, res = get_contact_address(redis_client, executor, receiver, w3)
      if code != 200:
          info = {"content": f"Cannot find {receiver} on contact", "code": 420}
          return {
            'result': info,
            'action': None, 
            'next_action': None 
          }
      value = float(amount)
      amount_to_transfer = w3.to_wei(value, 'mwei')  # USDT uses 6 decimals
      receiver = res
      to = w3.to_checksum_address(receiver)
      executor = w3.to_checksum_address(executor)

      print(f"to: {to}, executor: {executor}")
      tx_hash = None
      try:
          nonce = w3.eth.get_transaction_count(control_address)
          current_gas_price = w3.eth.gas_price
          replacement_gas_price = current_gas_price
          tx = control_contract.functions.transferFromERC20(
              token, executor, to, amount_to_transfer).build_transaction({
                'from': control_address,
                'nonce': nonce,
                'gas': 200000,  # Adjust gas limit
                'gasPrice': replacement_gas_price,  # Adjust gas price
              })
          pk = private_key
          signed_tx = w3.eth.account.sign_transaction(tx, pk)
          send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
          tx_hash = send_tx.hex()
          tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)
          status = 200
          message = "success"
          if tx_receipt['status'] == 0:
              status = 500
              message = "failed"
          info = {
            "content":
            generate_markdown_content(tx_receipt['status'], tx_hash, blockchain_explore),
            "status":
            tx_receipt['status'],
            "code":
            status
          }
          return { 
            'result': info, 
            'action': None, 
            'next_action': None 
          }
      except Exception as e:
          name, params = decode_custom_error(control_contract_abi, w3, str(e))
          if not name:
              # Note: If unknown error expose, check:
              # 1. if abi.json is the latest
              # 2. what error is exposed, how it happens
              message = f"Transfer usdt failed with unknown error: {e}"
          else:
              message = f"Transfer usdt error, error name: {name}, parameters: {params}"
          info = {"content": message, "status": 0, "code": 500}
          return {
            'result': info,
            'action': None, 
            'next_action': None
          }
    else:
      """ check executor current active chain """
      active_chain_key = f"user:{executor}:active_chain"
      active_chain = redis_client.get(active_chain_key)
      if not active_chain:
        active_chain = "base"
      if active_chain.lower() != chain.lower():
          params = {
            "func": "wallet_switchEthereumChain",
            "chainId": "ETH"
          }
          action_data = ActionData(func='', group='', params=params)
          action = Action(msg=None, type='setting', data=action_data.__dict__)

          code, res = get_contact_address(redis_client, executor, receiver, w3)
          if code != 200:
              info = {"content": f"Cannot find {receiver} on contact", "code": 420}
              return {
                'result': info,
                'action': None, 'next_action': None
              }
          value = float(amount)
          receiver = res
          to = w3.to_checksum_address(receiver)
          params = {
            'receiver': to,
            'amount': amount,
            'chain': chain,
            'token': token_raw,
            'run_mode': run_mode
          }
          next_action_data = ActionData(func='transfer', group='transfer', params=params)
          next_action = Action(msg=None, type='backend', data=next_action_data.__dict__)

          return {
            'result': { 'code': 403, 'content': 'Incorrect network, switching to the correct network for you.' },
            'action': action.__dict__,
            'next_action': next_action.__dict__
          }
      else:
          code, res = get_contact_address(redis_client, executor, receiver, w3)
          if code != 200:
              info = {"content": f"Cannot find {receiver} on contact", "code": 420}
              return {
                'result': info,
                'action': None,
                'next_action': None
              }
          value = float(amount)
          amount_to_transfer = w3.to_wei(value, 'mwei')  # USDT uses 6 decimals
          receiver = res
          to = w3.to_checksum_address(receiver)
          params = {
            'receiver': to,
            'amount': amount,
            'chain': chain,
            'token': token_raw,
            'run_mode': run_mode
          }
          action_data = ActionData(func='transfer', group='transfer', params=params)
          action = Action(msg=None, type='backend', data=action_data.__dict__)
          return {
            'result': None,
            'action': action.__dict__,
            'next_action': None
          }

def generate_markdown_content(status, hash_value, blockchain_explore):
    if status == 1:
        return f"Transfer successful. You can check the transaction on [blockchain explorer]({blockchain_explore}{hash_value})"
    else:
        return f"Transfer failed. You can check the transaction on [blockchain explorer]({blockchain_explore}{hash_value})"

def decode_custom_error(contract_abi, w3, error) -> Tuple[str, str]:
    # Parse error content, the error content must look like:
    # "Call method: submitServiceProof,xxxxx,error:('xxxxxx','xxxxxxx')"
    tmp_array = error.split(":")
    if len(tmp_array) != 3:
        return None, None
    param_str = tmp_array[2]
    param_str = param_str.replace("(","")
    param_str = param_str.replace(")","")
    param_str = param_str.replace(",","")
    param_str = param_str.replace("'","")
    errors = param_str.split()

    for error in [abi for abi in contract_abi if abi["type"] == "error"]:
        # Get error signature components
        name = error["name"]
        data_types = [collapse_if_tuple(abi_input) for abi_input in error.get("inputs", [])]
        error_signature_hex = function_abi_to_4byte_selector(error).hex()
        # Find match signature from error
        for error in errors:
            if error_signature_hex.casefold() == error[2:10].casefold():
                params = ','.join([str(x) for x in w3.codec.decode(data_types,bytes.fromhex(error[10:]))])
                #decoded = "%s(%s)" % (name , str(params))
                return name, params
    return None, None #try other contracts until result is not None since error may be raised from another called contract
