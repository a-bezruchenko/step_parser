import win32com.client
from win32com.client import constants

# path = "C:/Users/User/Desktop/универ/практика/модели/подшипник сборка/—борка2.iam"
# path = "C:/Users/User/Desktop/универ/практика/код/step_parser/BS 292_ ƒеталь 1 - 7000 - 10 x 26 x 8.ipt"

def parse_iam(path):
    invApp = win32com.client.Dispatch("Inventor.Application")
    invApp.Visible = False
    doc = invApp.Documents.Open(path, False)
    main_name = "test"
    res = {main_name: _rec_parse_subassembly(doc.ComponentDefinition.Occurrences)}
    return res

def _rec_parse_subassembly(subassembly):
    ASSEMBLY_TYPE = 12291
    COMPONENT_TYPE = 12290
    res = []
    for el in subassembly:
        if el.DefinitionDocumentType == COMPONENT_TYPE:
            res.append({el.Name: [{f.Name: f} for f in el.Definition.Features]})
        else:
            res.append({el.Name: _rec_parse_subassembly(el.SubOccurrences)})
    return res

def parse_ipt(path):
    invApp = win32com.client.Dispatch("Inventor.Application")
    invApp.Visible = False
    doc = invApp.Documents.Open(path, False)
    name = "test"
    res = []
    comp = doc.ComponentDefinition
    for feature in comp.Features:
        res.append({feature.Name: feature})
    return {name: res}