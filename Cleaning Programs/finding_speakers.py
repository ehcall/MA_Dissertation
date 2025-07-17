import os
import re
import xml.etree.ElementTree as ET

def main():
    to_modify_dir = "C:\\Users\elena\PycharmProjects\MA_Thesis\Full_Manuals\Quotations_XML"
    modified_dir = "C:\\Users\elena\PycharmProjects\MA_Thesis\Full_Manuals\Sources_XML"

    for manual in os.listdir(to_modify_dir):
      #  hold_up = input("wait a sec")
        to_modify_manual = to_modify_dir + "\\" + manual
        modified_manual = modified_dir + "\\" + manual

        tree = ET.parse(to_modify_manual)
        root = tree.getroot()
        for element in root.iter():
            print(element.tag)

#main()