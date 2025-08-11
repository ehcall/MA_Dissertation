import re
import csv
from semantic_dictionary import terms as sem_dict


def import_csv(filename):
    semantic_list = []
    with open(filename, encoding='utf-8') as fileread:
        semantic_csv = csv.reader(fileread)
        for line in semantic_csv:
            term = line[0]
            if re.match('\ufeff',term):
                term = re.sub('\ufeff','',term)
            semantic_list.append([term, line[1], line[2], line[3], line[4]])
    return semantic_list

def clean_term(term):
    cleaned = re.sub(r'[a-z]{1,3}', '', term)
    cleaned = re.sub('---', '-', cleaned)
    cleaned = re.sub('--', '-', cleaned)
    cleaned = re.sub('\+\+\+', '+', cleaned)
    cleaned = re.sub('\+\+', '+', cleaned)
    return cleaned
def condense_list(semantic_list):
    level_0 = {} #term incl. modifiers; for providing labels
    level_1 = {} #main category (A)
    level_2 = {} #sub category (A.1)
    level_3 = {} #sub sub category (A.1.1)
    level_4 = {} #sub sub sub category (A.1.1.1)

    for line in semantic_list:
        term = line[0]
        term_list = []
        if re.search('/',term):
            split_term = re.split('/',term)
            term_list.extend(split_term)
            #for now, I'm basically double-counting a term that gets 2+ cats
            cleaned_terms = []
            for ct in term_list:
                cleaned_terms.append(clean_term(ct))
            combined_name = ''
            for ct2 in cleaned_terms:
                if ct2 not in sem_dict:
                    combined_name += 'Unknown/'
                else:
                    combined_name += (sem_dict[ct2]['label'] + ' / ')
            combined_name = combined_name[:-3]
            level_0[term] = {
                'label': combined_name,
                '1_af': int(line[1]),
                '1_rf': float(line[2]),
                '2_af': int(line[3]),
                '2_rf': float(line[4])
            }
        else:
            term_list.append(term)
            cleaned_term = clean_term(term)
            if cleaned_term in sem_dict:
                level_0[term] = {
                    'label': sem_dict[cleaned_term]['label'],
                    '1_af': int(line[1]),
                    '1_rf': float(line[2]),
                    '2_af': int(line[3]),
                    '2_rf': float(line[4])
                }
        for term_check in term_list:
                cleaned_term = clean_term(term_check)
                if cleaned_term == 'D' or cleaned_term == 'PUNCT':
                    continue
                level_1_term = sem_dict[cleaned_term]['Lv1']
                if level_1_term not in level_1:
                    level_1[level_1_term] = {
                        'label': sem_dict[level_1_term]['label'],
                        '1_af': int(line[1]),
                        '1_rf': float(line[2]),
                        '2_af': int(line[3]),
                        '2_rf': float(line[4])
                    }
                else:
                    level_1[level_1_term]['1_af'] += int(line[1])
                    level_1[level_1_term]['1_rf'] += float(line[2])
                    level_1[level_1_term]['2_af'] += int(line[3])
                    level_1[level_1_term]['2_rf'] += float(line[4])


                level_2_term = sem_dict[cleaned_term]['Lv2']
                if level_2_term not in level_2:
                    level_2[level_2_term] = {
                        'label': sem_dict[level_2_term]['label'],
                        '1_af': int(line[1]),
                            '1_rf': float(line[2]),
                            '2_af': int(line[3]),
                            '2_rf': float(line[4])
                        }
                else:
                    level_2[level_2_term]['1_af'] += int(line[1])
                    level_2[level_2_term]['1_rf'] += float(line[2])
                    level_2[level_2_term]['2_af'] += int(line[3])
                    level_2[level_2_term]['2_rf'] += float(line[4])

                level_3_term = sem_dict[cleaned_term]['Lv3']
                if level_3_term != '-':
                    if level_3_term not in level_3:
                        level_3[level_3_term] = {
                            'label': sem_dict[level_3_term]['label'],
                            '1_af': int(line[1]),
                            '1_rf': float(line[2]),
                            '2_af': int(line[3]),
                            '2_rf': float(line[4])
                        }
                    else:
                        level_3[level_3_term]['1_af'] += int(line[1])
                        level_3[level_3_term]['1_rf'] += float(line[2])
                        level_3[level_3_term]['2_af'] += int(line[3])
                        level_3[level_3_term]['2_rf'] += float(line[4])

                level_4_term = sem_dict[cleaned_term]['Lv4']
                if level_4_term != '-':
                    if level_4_term not in level_4:
                        level_4[level_4_term] = {
                            'label': sem_dict[level_4_term]['label'],
                            '1_af': int(line[1]),
                            '1_rf': float(line[2]),
                            '2_af': int(line[3]),
                            '2_rf': float(line[4])
                        }
                    else:
                        level_4[level_4_term]['1_af'] += int(line[1])
                        level_4[level_4_term]['1_rf'] += float(line[2])
                        level_4[level_4_term]['2_af'] += int(line[3])
                        level_4[level_4_term]['2_rf'] += float(line[4])

    return level_0, level_1, level_2, level_3, level_4

def print_to_file(termlist, level_name, filename):
    full_filename = 'Semantic_Files/Condensed_' + level_name + '_' + filename
    with open(full_filename, 'w',newline='', encoding='utf-8') as to_write:
        sem_writer = csv.writer(to_write)
        for term in termlist:
            #print(term, termlist[term])
            sem_writer.writerow([term, termlist[term]['label'], termlist[term]['1_af'], termlist[term]['1_rf'],
                                termlist[term]['2_af'], termlist[term]['2_rf']])

def main():

    semantic_file = 'Semantic_Files/AllFemale_AllMale_Semantic.csv'
    new_filename = 'AllFemale_AllMale_Semantic.csv'

    semantic_file = 'Semantic_Files/CFMFemale_CFMMale_Semantic.csv'
    new_filename = 'CFMFemale_CFMMale_Semantic.csv'
    file_list = import_csv(semantic_file)
    term_lists = condense_list(file_list)

    i = 0
    for tlist in term_lists:
        level_name = 'Level' + str(i)
        print_to_file(tlist, level_name, new_filename)
        i+=1




    return

main()