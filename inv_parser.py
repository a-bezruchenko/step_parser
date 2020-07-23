import win32com.client
from win32com.client import constants
from pprint import pprint
import sys
import os.path

def parse_iam(path):
    invApp = win32com.client.Dispatch("Inventor.Application")
    invApp.Visible = False
    doc = invApp.Documents.Open(path, False)
    main_name = doc.PropertySets['Design Tracking Properties']['Part Number'].value
    res = {
        "name": main_name,
        "type": "assembly",
        "content":_rec_parse_subassembly(doc.ComponentDefinition.Occurrences)}
    return res

def _rec_parse_subassembly(subassembly):
    ASSEMBLY_TYPE = 12291
    COMPONENT_TYPE = 12290
    res = []
    for el in subassembly:
        if el.DefinitionDocumentType == COMPONENT_TYPE:
            content = _get_surface(el.Definition.Features)
            res.append({
                "name": el.Name,
                "type": "part",
                "content": content})
        else:
            res.append({
                "name":el.Name, 
                "type": "assembly",
                "content": _rec_parse_subassembly(el.SubOccurrences)})
    return res

def _get_surface(features):
    return [
    {
        "name": b.name,
        "type": "surface",
        "content": [f.SurfaceType for f in b.Faces]}
        for b in features[0].SurfaceBodies]

def parse_ipt(path):
    invApp = win32com.client.Dispatch("Inventor.Application")
    invApp.Visible = False
    doc = invApp.Documents.Open(path, False)
    main_name = doc.PropertySets['Design Tracking Properties']['Part Number'].value
    res = _get_surface(doc.ComponentDefinition.Features)
    return {
        "name": main_name,
        "type": "part",
        "content": res}

def getLastFrom(string: str, symbol: str):
    i = string.rfind(symbol)
    return string[i+1:]

if __name__ == "__main__":
    if len(sys.argv) > 1:
        for path in sys.argv[1:]:
            if not os.path.isfile(path):
                print("No such file: ", path)
            else:
                print("parsing " + path)
                extention = getLastFrom(path, '.')
                if extention == "iam":
                    pprint(parse_iam(path), width=150, compact=True)
                elif extention == "ipt":
                    pprint(parse_ipt(path), width=150, compact=True)
                else:
                    print("Unknown extention: ", extention)
                print('\n')
        print("Press any button to continue...")
        input()