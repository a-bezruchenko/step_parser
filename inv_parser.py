import win32com.client
from win32com.client import constants

# path = "C:/Users/User/Desktop/универ/практика/модели/подшипник сборка/—борка2.iam"

def parse_iam(path):
    invApp = win32com.client.Dispatch("Inventor.Application")
    invApp.Visible = False
    doc = invApp.Documents.Open(path, False)
    comp_list = []
    for comp in doc.ComponentDefinition.Occurrences:
        comp_list.append(comp.Name)
    return comp_list