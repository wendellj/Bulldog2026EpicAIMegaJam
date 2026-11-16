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

# =============================================================================
# High-level utility functions (wrap exec_python for common tasks)
# =============================================================================

def import_fbx(source_path: str, dest_path: str, asset_name: str,
               combine_meshes: bool = True, import_textures: bool = False) -> dict:
    """Import an FBX file as a static mesh."""
    source_path = source_path.replace('\\', '/')
    code = f'''
import unreal
task = unreal.AssetImportTask()
task.filename = '{source_path}'
task.destination_path = '{dest_path}'
task.destination_name = '{asset_name}'
task.replace_existing = True
task.automated = True
task.save = True

options = unreal.FbxImportUI()
options.import_mesh = True
options.import_textures = {import_textures}
options.import_materials = False
options.import_as_skeletal = False
options.static_mesh_import_data.combine_meshes = {combine_meshes}
options.static_mesh_import_data.generate_lightmap_u_vs = True
task.options = options

unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
print('IMPORTED:' + str(task.imported_object_paths) if task.imported_object_paths else 'FAILED')
'''
    return exec_python(code)

def import_texture(source_path: str, dest_path: str, asset_name: str = None) -> dict:
    """Import a texture file (jpg, png, tga)."""
    source_path = source_path.replace('\\', '/')
    if asset_name is None:
        import os
        asset_name = os.path.splitext(os.path.basename(source_path))[0]
    code = f'''
import unreal
task = unreal.AssetImportTask()
task.filename = '{source_path}'
task.destination_path = '{dest_path}'
task.destination_name = '{asset_name}'
task.replace_existing = True
task.automated = True
task.save = True
unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
print('IMPORTED:' + str(task.imported_object_paths) if task.imported_object_paths else 'FAILED')
'''
    return exec_python(code)

def create_material_instance(parent_path: str, dest_path: str, asset_name: str) -> dict:
    """Create a material instance from a parent material."""
    code = f'''
import unreal
factory = unreal.MaterialInstanceConstantFactoryNew()
parent = unreal.EditorAssetLibrary.load_asset('{parent_path}')
if parent:
    factory.set_editor_property('initial_parent', parent)
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    mi = asset_tools.create_asset('{asset_name}', '{dest_path}', unreal.MaterialInstanceConstant, factory)
    if mi:
        unreal.EditorAssetLibrary.save_asset('{dest_path}/{asset_name}')
        print('CREATED: {dest_path}/{asset_name}')
    else:
        print('FAILED: Could not create material instance')
else:
    print('FAILED: Parent material not found')
'''
    return exec_python(code)

def set_actor_mesh(actor_label: str, mesh_path: str) -> dict:
    """Set the static mesh on an actor's StaticMeshComponent."""
    code = f'''
import unreal
actors = unreal.EditorLevelLibrary.get_all_level_actors()
target = None
for a in actors:
    if a.get_actor_label() == '{actor_label}':
        target = a
        break

if not target:
    print('FAILED: Actor not found: {actor_label}')
else:
    mesh = unreal.EditorAssetLibrary.load_asset('{mesh_path}')
    if not mesh:
        print('FAILED: Mesh not found: {mesh_path}')
    else:
        comp = target.get_component_by_class(unreal.StaticMeshComponent)
        if comp:
            comp.set_static_mesh(mesh)
            print('SUCCESS: Set mesh on ' + '{actor_label}')
        else:
            print('FAILED: No StaticMeshComponent on actor')
'''
    return exec_python(code)

def set_actor_material(actor_label: str, material_path: str, slot: int = 0) -> dict:
    """Set material on an actor's mesh component."""
    code = f'''
import unreal
actors = unreal.EditorLevelLibrary.get_all_level_actors()
target = None
for a in actors:
    if a.get_actor_label() == '{actor_label}':
        target = a
        break

if not target:
    print('FAILED: Actor not found')
else:
    mat = unreal.EditorAssetLibrary.load_asset('{material_path}')
    comp = target.get_component_by_class(unreal.StaticMeshComponent)
    if comp and mat:
        comp.set_material({slot}, mat)
        print('SUCCESS: Set material on {actor_label}')
    else:
        print('FAILED: Component or material not found')
'''
    return exec_python(code)

def list_assets(path: str = '/Game', asset_type: str = None) -> dict:
    """List assets in a content browser path."""
    type_filter = f"and '{asset_type}' in str(unreal.EditorAssetLibrary.find_asset_data(a).asset_class)" if asset_type else ""
    code = f'''
import unreal
assets = unreal.EditorAssetLibrary.list_assets('{path}', recursive=True)
filtered = [a for a in assets if a {type_filter}]
for a in filtered[:50]:
    print(a)
print(f'Total: {{len(filtered)}} assets')
'''
    return exec_python(code)

def get_mesh_bounds(mesh_path: str) -> dict:
    """Get bounding box dimensions of a static mesh."""
    code = f'''
import unreal
mesh = unreal.EditorAssetLibrary.load_asset('{mesh_path}')
if mesh:
    bounds = mesh.get_bounding_box()
    dims = bounds.max - bounds.min
    print(f'Dimensions: X={{dims.x:.1f}} Y={{dims.y:.1f}} Z={{dims.z:.1f}}')
    print(f'Min: {{bounds.min}}')
    print(f'Max: {{bounds.max}}')
else:
    print('FAILED: Mesh not found')
'''
    return exec_python(code)


if __name__ == '__main__':
    # Test connection
    result = level('get_current_level_path')
    print(f"Current level: {result.get('level_name', 'unknown')}")
