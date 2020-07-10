# coding: utf-8
import re, sys
from itertools import islice
from pprint import pprint

# функция, вызываемая снаружи
def main(filename):
    return string_replacer(parse_stp(_open_file(filename)))

# построчно выдаёт содержимое файла
def _open_file(filename):
    with open(filename, "r") as f:
        for line in f:
            yield line

# разбирает переданное ему содержимое файла формата step
def parse_stp(data):
    # Пропускаем заголовок
    # Возможно, потом из него что-нибудь будем извлекать, но не сейчас
    for linecount, line in enumerate(data):
        if line == "DATA;\n":
            break
    # начинаем разбирать секцию данных
    res = {}
    current_el = -1
    no_op_element = False
    for linecount, line in enumerate(data):
        line = line.rstrip('\n')
        #print(linecount)
        if line == "ENDSEC;":
            return res
        if current_el == -1: # если он не равен -1, то мы продолжаем парсить элемент с прошлой строки
            b = line.find('(')
            e = line.find('=')
            current_el = int(line[1:e])
            no_op_element = line[e+1:b]==''
            temp_line = line
        else:
            temp_line += line
            if no_op_element:
                temp_line += '\n'
        if line[-1] == ';':
            b = temp_line.find('(')
            e = temp_line.find('=')
            if not no_op_element:
                res[current_el] = [temp_line[e+1:b], _parse(temp_line[b+1:-2])]
            else:
                res[current_el] = [temp_line[e+1:b], _parse_multiline_element(temp_line[b+1:-3])]
            current_el = -1

# разбирает аргументы команды
# принимает аргументы без скобок
def _parse(line):
    res = []
    start = 0
    b_count = 0
    i = 0
    for i in range(len(line)):
        if b_count == 0 and line[i] in ',\n' and start <= i:
            res.append(line[start:i])
            start = i+1
        elif line[i] == '(':
            b_count += 1
        elif line[i] == ')':
            b_count -= 1
            if b_count == 0:
                try:
                    res.append(_parse(line[start+1:i]))
                    start = i+2
                except Exception:
                    print(line)
                    print(i)
                    raise Exception 
        else:
            continue
    if b_count < 0:
        print(line)
        raise Exception
    left_chars = line[start:i+1]
    if line[start:i+1] != '':
        res.append(left_chars)
    return res

def _parse_multiline_element(element):
    lines = element.split('\n')[:-1]
    res = []
    for line in lines:
        b = line.find('(')
        res.append([line[:b], _parse(line[b+1:-1])])
    return res

# приводит строки в utf-8
def string_replacer(parsed_data):
    res = {x:[] for x in parsed_data}
    for key in parsed_data:
        res[key] = _recursive_string_replacer(parsed_data[key])
    return res

def _recursive_string_replacer(lst):
    res = []
    for element in lst:
        if type(element) == str:
            if element.find("\\X2") != -1: 
                splitted = element.split("\\X2\\")
                element = splitted[0]
                for substr in splitted[1:]:
                    x0 = substr.find("\\X0\\")
                    element += _convert_string(substr[:x0]) + substr[x0+len("\\X0\\"):]
            res.append(element)
        elif type(element) == list:
            res.append(_recursive_string_replacer(element))
    return res


def _convert_string(string):
    output = ""
    i = 0
    while i < len(string):
        output += chr(int(string[i:i+4], 16))
        i += 4
    return output

# заменяет упоминания элементов в разобранных данных на ссылки
def reference_replacer(parsed_data):
    res = {x:[parsed_data[x][0], []] for x in parsed_data}
    for key in parsed_data:
        try:
            res[key][1] += _list_reference_replacer(parsed_data[key][1], res)
        except Exception:
            print(key)
            print(parsed_data[key])
    return res

# рекурсивно заменяет упоминания элементов в данном списке на ссылки
# lst — список, в котором заменять
# dct — словарь, на который надо ссылаться
def _list_reference_replacer(lst, dct):
    res = []
    for element in lst:
        if type(element) == str and element != '' and element[0] == '#':
            ref_num = int(element[1:])
            res.append(dct[ref_num])
        elif type(element) == list:
            res.append(_list_reference_replacer(element, dct))
        else:
            res.append(element)
    return res



#res = main("test.stp")
#ref_res = reference_replacer(res)
#pprint(ref_res, depth=6)
if __name__ == "__main__":
    pprint(main(sys.argv[1]))