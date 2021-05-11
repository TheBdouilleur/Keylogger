#!/usr/bin/env python
# -*- coding: utf-8 -*-
from essential_generators import DocumentGenerator
import pyminifier
import os

def obfuscate(file_name):
    #1. PyMinifier
    os.popen(f"pyminifier --obfuscate --use-tabs {file_name}")   
    #2. Add random sentence
    gen = DocumentGenerator()
    text = "#" + gen.sentence() 
    with open(file_name, "a") as file:
        file.write(text)

def exeify(file_name):
    pass

def upxify(file_name):
    pass

obfuscate("keyl.py")
exeify("keyl.py")
upxify("keyl.exe")
