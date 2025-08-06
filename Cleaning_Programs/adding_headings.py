import os
import xml.etree.ElementTree as ET
import re

def main():
    to_modify_dir = "C:\\Users\elena\PycharmProjects\MA_Thesis\Full_Manuals\Basic_XML"
    modified_dir = "C:\\Users\elena\PycharmProjects\MA_Thesis\Full_Manuals\Headings_XML"
    for to_modify_manual in os.listdir(to_modify_dir):
       # print(to_modify_manual)
        if re.match("CFM", to_modify_manual):
          #  print(to_modify_manual)
            manual_cleanup = to_modify_dir + "\\" + to_modify_manual
            cleaned_manual = modified_dir + "\\" + to_modify_manual
            tree = ET.parse(manual_cleanup)
            root = tree.getroot()
            section_titles = [' Invite Sharing ', ' Teach the Doctrine ', ' Additional Resource ', ' Additional Resources ',
                              ' Improving Our Teaching ', ' Encourage Learning at Home ']

            for chapter in root:
                chapter_type = chapter.get('type')
                # need to figure out how to insert subsections!
                #print(chapter)
                chapter_headings_count = 0
                for branch in chapter:
                    teach_headings_count = 0
                    if chapter_type == 'lesson' and branch.tag == 'heading':
                        #add section heading titles
                       # print(branch.text)
                        if branch.text in section_titles:
                            branch.set('type','section-title')
                        #add chapter headings details
                        elif chapter_headings_count < 3:
                            chapter_headings_count+=1
                            if chapter_headings_count == 1:
                                branch.set('type', 'date')
                            elif chapter_headings_count == 2:
                                branch.set('type', 'ref')
                            else:
                                branch.set('type', 'title')
                        #add subheadings and details
                        else:
                            branch.tag = 'subheading'
                            if branch.text.isupper():
                                branch.set('type', 'ref')
                            else:
                                branch.set('type','sub-title')

                    elif chapter_type == 'teacher-help':
                        chapter_headings_count+=1
                        if chapter_headings_count > 1 and branch.tag == 'heading':
                            branch.tag = 'subheading'
                       # print(branch)

            tree.write(cleaned_manual)
        elif re.match("GD", to_modify_manual):

            manual_cleanup = to_modify_dir + "\\" + to_modify_manual
            cleaned_manual = modified_dir + "\\" + to_modify_manual
            tree = ET.parse(manual_cleanup)
            tree.write(cleaned_manual)


#main()