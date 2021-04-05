import importlib
import inspect
import json


local_group = {
    'parts':{
        'seq':{
            'source_file':'basics',
            'source_class':'Sequencer',
            'start_state':{
                'data':{
                    'freq':[1,2,3,4,5,6,7,8,9,10,11,12]
                },
                'count':0
            }
        },
        'beep':{
            'source_file':'basics',
            'source_class':'Beeper',
            'start_state':''
        }
    },

    'connections':{
        'data':[
            [['seq','freq'], ['beep','freq']]
        ]
    }
}





# get file from JSON
#file_name = "data.json"
#with open(file_name) as file_handle:
#    local_group = json.load(file_handle)

# Store basics intermediate info
module_name_lst = []
class_dict = {}
part_dict = {}

# get the names of all the files needed to import
for key, item in local_group['parts'].items():
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

# construct objs
for key, item in local_group['parts'].items():
    part_dict[key] = class_dict[item['source_class']](item['start_state'])

# Run objs
while True:
    for part_name, part in part_dict.items():
        part.step()