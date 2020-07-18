import win32com.client
from win32com.client import constants

# path = "C:/Users/User/Desktop/универ/практика/модели/подшипник сборка/—борка2.iam"
# path = "C:/Users/User/Desktop/универ/практика/код/step_parser/BS 292_ ƒеталь 1 - 7000 - 10 x 26 x 8.ipt"

def parse_iam(path):
    invApp = win32com.client.Dispatch("Inventor.Application")
    invApp.Visible = False
    doc = invApp.Documents.Open(path, False)
    res = []
    for comp in doc.ComponentDefinition.Occurrences:
        res.append(comp.Name)
    return res

def parse_ipt(path):
    invApp = win32com.client.Dispatch("Inventor.Application")
    invApp.Visible = False
    doc = invApp.Documents.Open(path, False)
    res = []
    comp = doc.ComponentDefinition
    for feature in comp.Features:
        res.append(feature)
    return res