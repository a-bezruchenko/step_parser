# coding: utf-8
# по разобранному файлу сборки строит дерево сборок/подсборок/моделей
from step_parser import main as parse_step
from pprint import pprint
import sys

def main(filename):
    parsed = parse_step(filename)
    pprint(build_tree(parsed))

# возвращаемый формат:
# (assembly_relationships, names), где
# assembly_relationships: [[1768, 1769], ...]
# второй элемент в каждом отношении является подсборкой
# names: {1768:"Сборка2", ...}
def build_tree(parsed_data):
    # вид parsed_data:
    # {10: ["operation", ["arg1", "2", [...], ...]], ...}

    # найти все NEXT_ASSEMBLY_USAGE_OCCURRENCE
    # они идут подряд близко к началу
    key = 10
    assembly_relationships = []
    while parsed_data[key][0] != 'NEXT_ASSEMBLY_USAGE_OCCURRENCE':
        key += 1

    while parsed_data[key][0] == 'NEXT_ASSEMBLY_USAGE_OCCURRENCE':
        assembly_relationships.append(key)
        key += 1

    # вид assembly_relationships: [25,26,27]
    # заменяем каждый элемент assembly_relationships на связываемые элементом тела
    def replace_with_related(key):
        j = 0
        while parsed_data[key][1][j][0] != '#':
            j += 1
        res = [parsed_data[key][1][j], parsed_data[key][1][j+1]]
        for i in range(len(res)):
            res[i] = int(res[i][1:])
        return res

    assembly_relationships = list(map(replace_with_related, assembly_relationships))

    # вид assembly_relationships: [[1768, 1769], [1768, 1770], [1768, 1770]]
    # выделим в отдельный список имена элементов
    names = {}
    for lst in assembly_relationships:
        for el in lst:
            if el not in names:
                names[el] = parsed_data[el][1][0]
    return assembly_relationships, names

if __name__ == "__main__":
    pprint(main(sys.argv[1]))