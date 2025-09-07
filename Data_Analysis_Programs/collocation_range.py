import csv
import re

collocations = []
concordances = []
coll_con_dict = {}
def import_collocations(collocation_file):
    with open(collocation_file, encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        for line in csvreader:
            collocations.append(line[0])

def import_concordances(concordance_file):
    with open(concordance_file, encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        for line in csvreader:
            manual = re.sub('\ufeff','',line[0])
            concordances.append([manual, line[1]])

def combine_coll_concord():
    for collocation in collocations:
        for concordance in concordances:
            if re.search(collocation, concordance[1]):
                if collocation not in coll_con_dict:
                    coll_con_dict[collocation] = set()
                coll_con_dict[collocation].add(concordance[0])

def GD_CFM_count(manual_list):
    gd_count = 0
    cfm_count = 0
    for manual in manual_list:
        if re.match('CFM',manual):
            cfm_count += 1
        elif re.match('GD', manual):
            gd_count += 1
    return gd_count, cfm_count
def print_csv():
    new_filename = 'Collocation_Files/all_male_range.csv'
    with open(new_filename, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        for collocation in coll_con_dict:
            manual_count = GD_CFM_count(coll_con_dict[collocation])
            if len(coll_con_dict[collocation]) > 8:
                print(coll_con_dict[collocation])
            csv_line = [collocation, len(coll_con_dict[collocation]), manual_count[0], manual_count[1]]
            csvwriter.writerow(csv_line)
def main():

    collocation_file = 'Collocation_Files/all_male.csv'
    import_collocations(collocation_file)

    concordance_file = 'Collocation_Files/all_male_concordances.csv'
    import_concordances(concordance_file)

    combine_coll_concord()
    print_csv()


    return

main()