import os
import re


def main():
    to_modify_dir = "C:\\Users\elena\PycharmProjects\MA_Thesis\Full_Manuals\Headings_XML"
    modified_dir = "C:\\Users\elena\PycharmProjects\MA_Thesis\Full_Manuals\Sections_XML"
    for manual in os.listdir(to_modify_dir):
        if re.match("CFM", manual):
            to_modify_manual = to_modify_dir + "\\" + manual
            modified_manual = modified_dir + "\\" + manual
           # to_modify_manual = "testing.xml"
           # modified_manual = "testing_clean.xml"
            modifying_text = []
           # hold_up = input("wait a sec")
            with open(to_modify_manual, 'r', encoding='utf-8') as modify_file:
                temp_section = []
                temp_subsection = []
                modify_section = False
                for line in modify_file.readlines():
                    #these lines are only here for now because I don't want to deal with italics and bold
                    #so TODO: delete them later
                    line = re.sub(' ?<i> ?', ' ', line)
                    line = re.sub('><b> ?','>',line)
                    line = re.sub(' ?<b> ',' ',line)
                    line = re.sub('<b>', '', line)
                    line = re.sub(' ?</b> ?',' ',line)
                    line = re.sub(' ?</i> ?',' ',line)

                    if re.search("type=\"teacher",line) or re.search("type=\"lesson",line):
                        modify_section = True
                    if re.search("<heading",line) and modify_section is True:
                        if re.search("date",line) or re.search("ref",line) or re.search("\"title", line):
                            if len(temp_section) == 0:
                                temp_section.append("chapter-heading")
                            temp_section.append(line)
                        else:
                           # print(line)
                            if len(temp_subsection) > 0:
                                temp_section.append(temp_subsection)
                                temp_subsection = []
                            if len(temp_section) > 0:
                                #print(temp_section)
                                modifying_text.append(temp_section)
                                temp_section = []
                            temp_section.append(line)
                    elif re.search("<subheading", line):
                        if len(temp_subsection) > 1:
                            temp_section.append(temp_subsection)
                            temp_subsection = []
                        temp_subsection.append(line)
                    else:
                        if re.match("</chapter", line):
                            if len(temp_subsection) > 0:
                                temp_section.append(temp_subsection)
                                temp_subsection = []
                            if len(temp_section) > 0:
                               # print(temp_section)
                                modifying_text.append(temp_section)
                                temp_section = []
                        if len(temp_subsection) > 0:

                            temp_subsection.append(line)
                        elif len(temp_section) > 0:
                            temp_section.append(line)
                            #print(temp_section)
                        else:
                            modifying_text.append(line)

            modified_text = []

            for item in modifying_text:
                if isinstance(item, list):
                    #modified_text.append("<section>")
                    new_type = ""
                    for section_item in item:
                        if isinstance(section_item, list):
                            if new_type != "":
                                new_subsection = "<subsection type=\"" + new_type + "\">\n"
                            else:
                                new_subsection = "<subsection>\n"
                            modified_text.append(new_subsection)
                            for subsection_item in section_item:
                                modified_text.append(subsection_item)
                            modified_text.append("</subsection>\n")
                        else:
                            if re.match("chapter-heading",section_item):
                                modified_text.append("<section type=\"chapter-heading\">\n")
                            elif re.search("section-title", section_item):
                                section_heading = "<section type=\"none\">\n"
                                if re.search("Invite Sharing", section_item):
                                    section_heading = re.sub('none', 'invite',section_heading)
                                    new_type = "invite"
                                elif re.search("Teach the", section_item):
                                    section_heading = re.sub('none', 'teach',section_heading)
                                    new_type = "teach"
                                elif re.search("Encourage Learn", section_item):
                                    section_heading = re.sub('none', 'encourage',section_heading)
                                    new_type = "encourage"
                                elif re.search("Additional Resource", section_item):
                                    section_heading = re.sub('none', 'resource',section_heading)
                                    new_type = "resource"
                                elif re.search("Improving Our", section_item):
                                    section_heading = re.sub('none', 'improve',section_heading)
                                    new_type = "improve"
                                else:
                                    pass
                             #       print(section_item)
                                modified_text.append(section_heading)
                                modified_text.append(section_item)
                            elif re.search("<heading>", section_item):
                                modified_text.append("<section>\n")
                                modified_text.append(section_item)
                            else:
                                modified_text.append(section_item)
                    modified_text.append("</section>\n")
                else:
                    modified_text.append(item)

            with open(modified_manual,'w', encoding='utf-8') as modified_file:
                modified_file.writelines(modified_text)


        elif re.match("GD",manual):
            #TODO
           # print(to_modify_manual)
            pass
            ## deal with "subheadings" and "subsubheadings"

main()