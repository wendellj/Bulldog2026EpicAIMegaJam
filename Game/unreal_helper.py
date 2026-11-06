#!/usr/bin/env python3
"""Helper script for calling UnrealMCPython actions."""
import socket
import json
import sys

def call_unreal(module: str, function: str, args: dict = None) -> dict:
    """Call an UnrealMCPython action via TCP."""
    if args is None:
        args = {}

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(60)
    s.connect(('127.0.0.1', 12029))

    request = {
        'type': 'python_call',
        'module': f'UnrealMCPython.{module}',
        'function': function,
        'args': args
    }
    s.sendall(json.dumps(request).encode())

    response = b''
    while True:
        chunk = s.recv(16384)
        if not chunk:
            break
        response += chunk
    s.close()

    result = json.loads(response.decode())
    if result.get('success'):
        inner = result.get('result', '{}')
        if isinstance(inner, str):
            try:
                return json.loads(inner)
            except:
                return result
        return inner
    return result

def exec_python(code: str) -> dict:
    """Execute arbitrary Python code in Unreal."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(60)
    s.connect(('127.0.0.1', 12029))

    request = {'type': 'python', 'code': code}
    s.sendall(json.dumps(request).encode())

    response = b''
    while True:
        chunk = s.recv(16384)
        if not chunk:
            break
        response += chunk
    s.close()

    return json.loads(response.decode())

# Shorthand functions for common domains
def actor(action: str, **kwargs) -> dict:
    return call_unreal('actor_actions', f'ue_{action}', kwargs)

def asset(action: str, **kwargs) -> dict:
    return call_unreal('asset_actions', f'ue_{action}', kwargs)

def blueprint(action: str, **kwargs) -> dict:
    return call_unreal('blueprint_actions', f'ue_{action}', kwargs)

def level(action: str, **kwargs) -> dict:
    return call_unreal('level_actions', f'ue_{action}', kwargs)

def material(action: str, **kwargs) -> dict:
    return call_unreal('material_actions', f'ue_{action}', kwargs)

def umg(action: str, **kwargs) -> dict:
    return call_unreal('umg_actions', f'ue_{action}', kwargs)

def util(action: str, **kwargs) -> dict:
    return call_unreal('util_actions', f'ue_{action}', kwargs)

if __name__ == '__main__':
    # Test connection
    result = level('get_current_level_path')
    print(f"Current level: {result.get('level_name', 'unknown')}")
