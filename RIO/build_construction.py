import importlib
import inspect
import json
import os

def build(filename):
    # get file from JSON
    file_name = os.path.abspath(filename)
    with open(file_name) as file_handle:
        construction = json.load(file_handle)

    # Store basics intermediate info
    module_name_lst = []
    class_dict = {}
    part_dict = {}

    # get the names of all the files needed to import
    for key, item in construction['parts'].items():
        module_name_lst += ['Modules.'+item['source_file']]

    # import files
    for module_name in module_name_lst:
        try:
            module = importlib.import_module(module_name)
            for obj_name, obj in inspect.getmembers(module):
                if inspect.isclass(obj):
                    class_dict[obj_name] = obj
        except:
            print("Module '" + module_name + "' not found or broken")

    # construct parts
    for key, item in construction['parts'].items():
        part_dict[key] = {
            'class_obj':class_dict[item['source_class']](item['start_state']),
            'connections':[]
        }
        for connection_pair in construction['connections']:
            if key in connection_pair[0].values():
                part_dict[key]['connections'] += [connection_pair]
            elif key in connection_pair[1].values():
                part_dict[key]['connections'] += [connection_pair[::-1]]
            else:
                pass
    
    return part_dict
    
'''
# Run parts
while True:
    for part_name, part in part_dict.items():
        part['class_obj'].step()

        for connection_name, content in part['connections'].items():
            pass

'''