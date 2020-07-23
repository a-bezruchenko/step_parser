from collections import Counter
from inv_parser import getLastFrom, parse_iam, parse_ipt
import os.path
import sys
from pprint import pprint

def get_surface_list(tree, is_bearing):
    res = []
    for element in tree['content']:
        if element['type'] == "part":
            res.append({
                "name": element['name'],
                "is_bearing": is_bearing,
                "content": dict(Counter(element['content'][0]['content']))
                })
        else:
            res += get_surface_list(element, is_bearing)
    return res

PRINT_WIDTH = 120

if __name__ == "__main__":
    if len(sys.argv) > 2:
        if sys.argv[1][0] == '-':
            start_index = 2
            if sys.argv[1][1:].lower() in ["1","true","y"]:
                is_bearing = True
            elif sys.argv[1][1:].lower() in ["0","false","n"]:
                is_bearing = False
            else:
                print('"is_bearing" parameter not specified, assumed to be false')
                is_bearing = False
        else:
            start_index = 1
            print('"is_bearing" parameter not specified, assumed to be false')
            is_bearing = False
        for path in sys.argv[start_index:]:
            if not os.path.isfile(path):
                print("No such file: ", path)
            else:
                print("parsing " + path)
                extention = getLastFrom(path, '.')
                if extention == "iam":
                    pprint(get_surface_list(parse_iam(path), is_bearing), width=PRINT_WIDTH, compact=True)
                elif extention == "ipt":
                    pprint(get_surface_list(parse_ipt(path), is_bearing), width=PRINT_WIDTH, compact=True)
                else:
                    print("Unknown extention: ", extention)
                print('\n')
        print("Press any button to continue...")
        input()