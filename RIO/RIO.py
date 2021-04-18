import build_construction
import pprint
construction = build_construction.build("./tests/tetris_music.json")
pprint.pprint(construction)

while True:
    for part_name, part in construction.items():
        part['class_obj'].step()
        for connection in part['connections']:
            try:
                construction[connection[1]['part']]['class_obj'].input(connection[0]['port'], construction[connection[0]['part']]['class_obj'].output(connection[1]['port']))
            except:
                pass
                #print('port connection failed')


