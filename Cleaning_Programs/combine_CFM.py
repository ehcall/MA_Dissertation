import os
import re


def get_file_text(filename):
    with open(filename, encoding="utf-8") as xml_file:
        file_text = xml_file.readlines()
    return file_text

def write_to_manual(new_location, manual_text):
    with open(new_location, 'w', encoding='utf-8') as xml_file:
        xml_file.write("<text>\n")
        for chapter in manual_text:
            xml_file.write("<chapter type=\"lesson\">\n")
            #print(chapter)
            xml_file.writelines(chapter)
            xml_file.write("\n</chapter>\n")
        xml_file.write("\n</text>\n")


files_dir = "C:\\Users\elena\PycharmProjects\MA_Thesis\CFM_Split_Files"

for standard_work in os.listdir(files_dir):
    standard_work_dir = files_dir + "\\" + standard_work

    full_manual_text = []
    for text_file in os.listdir(standard_work_dir):
        if not re.match("BM", text_file):
            #print(text_file)
            text_file_loc = standard_work_dir + "\\" + text_file
            file_text = get_file_text(text_file_loc)
            full_manual_text.append(file_text)
    #print(full_manual_text)

    new_manual_text_loc = "C:\\Users\elena\PycharmProjects\MA_Thesis\Full_Manuals\\" + standard_work + ".xml"
    write_to_manual(new_manual_text_loc, full_manual_text)