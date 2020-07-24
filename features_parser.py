import win32com.client
from win32com.client import constants
from pprint import pprint
import sys
import os.path
from collections import Counter

def features_parser(path, is_bearing=False, invApp = None):
    if not invApp:
        invApp = win32com.client.Dispatch("Inventor.Application")
        invApp.Visible = False
    doc = invApp.Documents.Open(path, False)
    return [
    {
        "name": occ.name,
        "is_bearing": is_bearing,
        "content": dict(Counter([f.type for f in occ.Definition.Features]))
    }
    for occ in doc.ComponentDefinition.Occurrences]