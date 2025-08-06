import os
from bs4 import BeautifulSoup
import csv
import re
from datetime import datetime

people_dict = dict()
calling_dict = dict()
citation_dict = dict()
def add_to_dict(quotation, qdata, speaker, manual, text):

    gender = quotation['gender']
    citation = quotation['citation']


    if gender == 'M - Male':
        if speaker not in qdata[manual]['men']:
            qdata[manual]['men'][speaker] = [[citation, text, quotation['partial_quote']]]
        else:
            qdata[manual]['men'][speaker].append([citation, text, quotation['partial_quote']])
    elif gender == 'F - Female':
        if speaker not in qdata[manual]['women']:
            qdata[manual]['women'][speaker] = [[citation, text, quotation['partial_quote']]]
        else:
            qdata[manual]['women'][speaker].append([citation, text, quotation['partial_quote']])
    elif gender == 'O - Mixed':
        if speaker == 'Ruth Renlund':
            qdata[manual]['women'][speaker] = [[citation, text, quotation['partial_quote']]]
        else:
            qdata[manual]['men'][speaker] = [[citation, text, quotation['partial_quote']]]

    else:
        if speaker not in qdata[manual]['supp']:
            qdata[manual]['supp'][speaker] = [[citation, text, quotation['partial_quote']]]
        else:
            qdata[manual]['supp'][speaker].append([citation, text, quotation['partial_quote']])
    return

def grab_from_corpus():
    qdata = dict()

    quote_texts = "C:\\Users\elena\PycharmProjects\MA_Thesis\Full_Manuals\Sources_XML"
    for manual in os.listdir(quote_texts):
        analyzing_manual = quote_texts + "\\" + manual

        with open(analyzing_manual, 'r', encoding='utf-8') as f:
            file = f.read()
        soup = BeautifulSoup(file, 'xml')
        quotations = soup.find_all(['quotation'])
        qdata[manual] = {
            'men': dict(),
            'women': dict(),
            'supp': dict()
        }
        dupe_quotes = []
        for quotation in quotations:
            text = quotation.text.strip()
            if quotation['partial_quote'] != 'True':
                speaker = quotation['speaker']
                split_speaker = quotation['speaker'].split(', ')
                if len(split_speaker) > 1 and speaker != 'Joseph Smith, Sr.':
                    for person in split_speaker:
                        if person != 'Teaching — No Greater Call' and person != 'History of the Church':
                            add_to_dict(quotation, qdata, person, manual, text)
                else:
                    add_to_dict(quotation, qdata, speaker, manual, text)
            else:
                dupe_quotes.append(quotation)

        full_text = []
        prev_citation = ''
        dupe_speaker = ''
        dupe_manual = ''
        i = 0
        for dq in dupe_quotes:
            # print(dq['citation'])
            if prev_citation == dq['citation']:
                full_text.append(dq.text.strip())
            else:
                if i != 0:
                    # print("\t",full_text, dupe_speaker, prev_citation)
                    add_to_dict(prev_quotation, qdata, dupe_speaker, manual, ' '.join(full_text))
                else:
                    i += 1
                prev_citation = dq['citation']
                dupe_speaker = dq['speaker']
                dupe_manual = manual
                prev_quotation = dq
                full_text = []
                full_text.append(dq.text.strip())
                # print(dq['citation'])
        # print("\t", full_text, dupe_speaker, prev_citation)
        add_to_dict(prev_quotation, qdata, dupe_speaker, manual, ' | '.join(full_text))

    qdata_rows = []

    for manual in qdata:
        # print(manual)
        for gender in qdata[manual]:
            #  print("\t",gender)
            for speaker in sorted(qdata[manual][gender]):
                # print("\t\t",speaker)
                # quote_count = 0
                for speaker_quote in qdata[manual][gender][speaker]:
                    # quote_count += 1
                    # print("\t\t\tQuote ",quote_count,": ")

                    speaker_citation = speaker_quote[0]
                    speaker_citation = re.sub('See also ', '', speaker_citation)
                    speaker_citation = re.sub('[sS]ee ', '', speaker_citation)
                    if re.match(speaker, speaker_citation):
                        speaker_citation = re.sub(speaker, '', speaker_citation)
                    speaker_citation = re.sub('^[:,] ', '', speaker_citation)
                    speaker_citation = re.sub(' or Liahona', '', speaker_citation)

                    speaker_text = speaker_quote[1]
                    # print(speaker, "\n\t", speaker_citation, "\n\t\t", speaker_text)
                    new_row = [manual, gender, speaker, speaker_citation, speaker_text, speaker_quote[2]]
                    qdata_rows.append(new_row)

    with open('/Cleaning_Programs/quote_data.csv', 'w',
              encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Manual', 'Gender', 'Speaker', 'Citation', 'Text', 'Partial'])
        csvwriter.writerows(qdata_rows)
    return

def calling_sorting(calling):
    calling_category = ''
    ces = ['BYU President','BYU-I President', 'Commissioner of Church Education', 'SVU President']
    if re.match('FP',calling) or re.match('President', calling):
        calling_category = 'First Presidency'
    elif re.match('PB', calling):
        calling_category = 'Presiding Bishopric'
    elif re.match('PR', calling):
        calling_category = 'Primary'
    elif re.match('Q12', calling):
        calling_category = 'Quorum of the Twelve'
    elif re.match('RS', calling):
        calling_category = 'Relief Society'
    elif re.match('Seventy', calling) or re.match('Assistant',calling):
        calling_category = 'Seventy'
    elif re.match('SS', calling):
        calling_category = 'Sunday School'
    elif re.match('YM', calling):
        calling_category = 'Young Men'
    elif re.match('YW', calling):
        calling_category = 'Young Women'
    elif calling in ces:
        calling_category = 'CES'
    else:
        calling_category = 'Other'
    return calling_category

def adjust_date(old_date):
    if old_date == 'NA':
        old_date = '2025-07-24'
    if len(old_date.split('-')) == 2:
        old_date = old_date + "-01"
    elif len(old_date.split('-')) == 1:
        old_date = old_date + "-01-01"
    new_date = datetime.strptime(old_date, '%Y-%m-%d').date()
    return new_date
def import_speaker_data():
    #would this have been easier if I assigned IDs to begin with? almost certainly. not changing it now though!
    with open('/Cleaning_Programs\speaker_data.xml', 'r', encoding='utf-8') as f:
        file = f.read()
    people_soup = BeautifulSoup(file, 'xml')
    people = people_soup.find_all('person')

    for person in people:
        person_name = person.find('name').text.strip()
        person_id = person.find('person-id').text.strip()
        gender = person.find('gender').text.strip()
        religion = person.find('religion').text.strip()

        birthdate = person.find('birthdate').text.strip()
        if birthdate == '':
            birthdate = 'UNKNOWN'
        if birthdate != 'UNKNOWN':
            birthdate = adjust_date(birthdate)
        deathdate = person.find('deathdate').text.strip()
        if deathdate == '':
            deathdate = 'UNKNOWN'
        if deathdate != 'UNKNOWN':
            deathdate = adjust_date(deathdate)
        callings = person.find_all('calling')
        if person_id not in people_dict:
            people_dict[person_name] = {
                'id':person_id,
                'gender':gender,
                'religion':religion,
                'birth':birthdate,
                'death':deathdate,
                'callings':{}
            }
        for calling in callings:
            calling_title = calling.find('calling-title').text.strip()
            organization = calling_sorting(calling_title)
            if calling_title not in calling_dict:
                calling_dict[calling_title] = {
                    'org': organization,
                    'people': []
                }
            calling_dict[calling_title]['people'].append(person_id)
            calling_start = adjust_date(calling.find('calling-start').text.strip())
            calling_end = adjust_date(calling.find('calling-end').text.strip())
            calling_role = calling_title.split(' - ')
            if calling_title not in people_dict[person_name]['callings']:
                people_dict[person_name]['callings'][calling_title] = []


            if len(calling_role) == 2:
                people_dict[person_name]['callings'][calling_title].append({
                    'start': calling_start,
                    'end': calling_end,
                    'org':organization,
                    'role':calling_role[1]
                })

            else:
                people_dict[person_name]['callings'][calling_title].append({
                    'start': calling_start,
                    'end': calling_end,
                    'org':organization
                })
    return people_dict,calling_dict

def get_citation_data(citation, speaker, gender, quote_id):
    #print(citation)

    citation_year_search = re.search('[0-9]{4}', citation)
    if citation_year_search != None:
        citation_year = citation_year_search.group()
    else:
        citation_year = 'NONE'
    # print(citation_year)
    citation_month_search = re.search('Jan|Feb|Mar[\.c]|Apr|May [0-9]|Jun|Jul|Aug|Sep|Oct|Nov|Dec', citation)
    if citation_month_search != None:
        citation_month = citation_month_search.group().strip()
        if citation_month == 'Jan':
            citation_month = '01'
        elif re.match('May',citation_month) or citation_month == 'Apr':
            if not re.search('Ensign',citation) and not re.search('Conference Report', citation):
                if re.match('May',citation_month):
                    citation_month = '05'
                else:
                    citation_month = '04'
            else:
                citation_month = '04'
        elif citation_month == 'Nov' or citation_month == 'Oct':
            if not re.search('Ensign', citation) and not re.search('Conference Report', citation):
                if citation_month == 'Nov':
                    citation_month = '11'
                else:
                    citation_month = '10'
            else:
                citation_month = '10'
        elif citation_month == 'Feb':
            citation_month = '02'
        elif re.match('Mar',citation_month):
            citation_month = '03'
        elif citation_month == 'Jun':
            citation_month = '06'
        elif citation_month == 'Jul':
            citation_month = '07'
        elif citation_month == 'Aug':
            citation_month = '08'
        elif citation_month == 'Sep':
            citation_month = '09'
        elif citation_month == 'Dec':
            citation_month = '12'
    else:
        citation_month = 'NONE'
    #print(citation_year, citation_month, " - ",citation)
    citation_date = 'UNKNOWN'
    if citation_year != 'NONE':
        citation_date = citation_year
        if citation_month != 'NONE':
            citation_date = citation_date + "-" + citation_month
    return citation_date

def get_calling(citation_date,speaker, publication_date):
    speaker_callings = people_dict[speaker]['callings']
    if len(speaker_callings) == 0:
        if people_dict[speaker]['religion'] != 'LDS':
            return 'Not LDS','Not LDS'
        else:
            return "NA","NA"
    else:
        for sc in speaker_callings:
           # print(citation_date, speaker)
            #print(speaker_callings[sc])
            for calling_option in speaker_callings[sc]:
                if calling_option['end'] == people_dict[speaker]['death'] and people_dict[speaker]['death'].year < int(publication_date):
                    last_calling = "DECEASED AT PUB - " + calling_option['org']
                    return sc, last_calling
                if calling_option['start'] < citation_date < calling_option['end']:
                    if people_dict[speaker]['death'].year < int(publication_date):
                        last_calling = "DECEASED AT PUB - " + calling_option['org']
                        return sc, last_calling
                    return sc, calling_option['org']


    for sc in speaker_callings:
        return sc, speaker_callings[sc][0]['org']

    return

def get_pub_calling(publication_year,speaker):
    speaker_callings = people_dict[speaker]['callings']
    if len(speaker_callings) == 0:
        if people_dict[speaker]['religion'] != 'LDS':
            return 'Not LDS','Not LDS'
        else:
            if speaker == 'The Quorum of the Twelve':
                return 'Quorum of the Twelve'
            return "NA","NA"
    else:
        for sc in speaker_callings:
           # print(citation_date, speaker)
            #print(speaker_callings[sc])
            for calling_option in speaker_callings[sc]:
                if calling_option['end'] == people_dict[speaker]['death'] and people_dict[speaker]['death'].year < int(publication_year):
                    last_calling = "DECEASED AT PUB - " + calling_option['org']
                    return sc, last_calling
                if calling_option['end'] == people_dict[speaker]['death']:
                    return sc, calling_option['org']
                if calling_option['start'].year < int(publication_year) < calling_option['end'].year:
                    return sc, calling_option['org']


    for sc in speaker_callings:
        if people_dict[speaker]['death'].year < int(publication_year):
            last_calling = "DECEASED AT PUB - " + calling_option['org']
            return sc, last_calling
        return sc, speaker_callings[sc][0]['org']

    return
def link_speakers():
    q_data = []
    with open('quote_data.csv', encoding='utf-8') as csv_read:
        csvreader = csv.reader(csv_read)
        for row in csvreader:
            if len(row) > 0 and row[0] != 'Manual':
               q_data.append(row)
                #print(row)
    basic_data_cite = {}
    basic_data_pub = {}
    quote_id = 0
    partial_quote = []
    prev_data = []
    full_quotes = []
    for qd in q_data:
        manual = qd[0]
        pub_date = re.search('[0-9]{4}',manual).group()
        gender = qd[1]
        speaker = qd[2]
        citation = qd[3]
        citation_date = get_citation_data(citation, speaker, gender, quote_id)
        #print(pub_date, citation_date)
        quote = qd[4]
        partial = qd[5]
        if partial == 'False':
            if len(partial_quote) != 0:
                prev_data.extend([' '.join(partial_quote), 'Connected'])
                full_quotes.append(prev_data)
                partial_quote = []
                prev_data = []
            full_quotes.append([manual, gender, speaker, citation, pub_date, citation_date, quote, partial])
            partial_quote = []
            prev_data = []
        elif len(prev_data) > 0 and citation != prev_data[3]:
            prev_data.extend([' '.join(partial_quote), 'Connected'])
            full_quotes.append(prev_data)
            partial_quote = []
            prev_data = []
            partial_quote.append(quote)
            prev_data = [manual, gender, speaker, citation, pub_date, citation_date]

        else:
            partial_quote.append(quote)
            prev_data = [manual, gender, speaker, citation, pub_date, citation_date]
            #print("here")

    just_quote_text = []
    for full_quote in full_quotes:
        manual = full_quote[0]
        gender = full_quote[1]
        speaker = full_quote[2]
        citation = full_quote[3]
        pub_date = full_quote[4]
        citation_date = full_quote[5]
        quote = full_quote[6]
        partial = full_quote[7]
        just_quote_text.append([quote, manual, gender, speaker])
        if gender == 'supp':
            calling_at_cite = 'NA'
            org_at_cite = 'NA'
            org_at_pub = 'NA'
        elif speaker == 'The First Presidency':
            calling_at_cite = 'First Presidency'
            org_at_cite = 'First Presidency'
            org_at_pub = 'First Presidency'

        else:
            if citation_date != 'UNKNOWN':
                citation_date = adjust_date(citation_date)
                calling_org_citation = get_calling(citation_date, speaker, pub_date)
                calling_org_pub = get_pub_calling(pub_date, speaker)
                org_at_pub = calling_org_pub[1]
                #print(calling_org)
                calling_at_cite = calling_org_citation[0]
                org_at_cite = calling_org_citation[1]
                #print(manual, org_at_cite, speaker, citation_date)
            else:
                new_pub_date = adjust_date(pub_date)
                calling_org_citation = get_calling(new_pub_date, speaker, pub_date)
                calling_at_cite = calling_org_citation[0]
                org_at_cite = calling_org_citation[1]
                calling_org_pub = get_pub_calling(pub_date, speaker)
                org_at_pub = calling_org_pub[1]


        if manual not in basic_data_cite:
            basic_data_cite[manual] = {}
        if gender not in basic_data_cite[manual]:
            basic_data_cite[manual][gender] = {}
        if org_at_cite not in basic_data_cite[manual][gender]:

            basic_data_cite[manual][gender][org_at_cite] = {}
        if speaker not in basic_data_cite[manual][gender][org_at_cite]:
            basic_data_cite[manual][gender][org_at_cite][speaker] = 0
        basic_data_cite[manual][gender][org_at_cite][speaker] += 1

        if manual not in basic_data_pub:
            basic_data_pub[manual] = {}
        if gender not in basic_data_pub[manual]:
            basic_data_pub[manual][gender] = {}
        if org_at_pub not in basic_data_pub[manual][gender]:
            basic_data_pub[manual][gender][org_at_pub] = {}
        if speaker not in basic_data_pub[manual][gender][org_at_pub]:
            basic_data_pub[manual][gender][org_at_pub][speaker] = 0
        basic_data_pub[manual][gender][org_at_pub][speaker] += 1

    #print(basic_data)
    basic_data_list_pub = []
    for manual in basic_data_pub:
        for gender in basic_data_pub[manual]:
            for org in basic_data_pub[manual][gender]:
                org_people = []
                total_quote_count = 0
                for person in basic_data_pub[manual][gender][org]:
                    #print(person)
                    org_people.append([person, basic_data_pub[manual][gender][org][person]])
                    total_quote_count+= basic_data_pub[manual][gender][org][person]
                basic_data_list_pub.append([manual, gender, org, org_people, len(org_people), total_quote_count])

    basic_data_list_cite = []
    for manual in basic_data_cite:
        for gender in basic_data_cite[manual]:
            for org in basic_data_cite[manual][gender]:
                org_people = []
                total_quote_count = 0
                for person in basic_data_cite[manual][gender][org]:
                    # print(person)
                    org_people.append([person, basic_data_cite[manual][gender][org][person]])
                    total_quote_count += basic_data_cite[manual][gender][org][person]
                basic_data_list_cite.append([manual, gender, org, org_people, len(org_people), total_quote_count])

    with open('speaker_quote_data_pub.csv', 'w', newline='', encoding='utf-8') as csv_writer:
        csvwriter = csv.writer(csv_writer)
        csvwriter.writerows(basic_data_list_pub)

    with open('speaker_quote_data_cite.csv', 'w', newline='', encoding='utf-8') as csv_writer:
        csvwriter = csv.writer(csv_writer)
        csvwriter.writerows(basic_data_list_cite)

    internal_quotes = []

    for line in just_quote_text:
        if re.search('«',line[0]):
            internal_quotes.append(line)

    with open('internal_quotes.csv', 'w', newline='', encoding='utf-8') as csv_writer:
        csvwriter = csv.writer(csv_writer)
        csvwriter.writerows(internal_quotes)
    print(len(just_quote_text), len(internal_quotes))
    return

def get_percent(figure_1, figure_2):
    total_overall = figure_1 + figure_2
    fig_1_percent = round((figure_1 / total_overall * 100), 2)
    fig_2_percent = round((figure_2 / total_overall * 100), 2)
    return (fig_1_percent,fig_2_percent)

def get_stats():
    pub_calling_data = []
    cite_calling_data = []
    with open('speaker_quote_data_pub.csv', encoding='utf-8') as csv_reader:
        csvreader = csv.reader(csv_reader)
        for row in csvreader:
            pub_calling_data.append(row)
    with open('speaker_quote_data_cite.csv', encoding='utf-8') as csv_reader:
        csvreader = csv.reader(csv_reader)
        for row in csvreader:
            cite_calling_data.append(row)

    manual_data = dict()
    people_data = dict()

    for list_item in pub_calling_data:
        manual = list_item[0]
        gender = list_item[1]
        org_pub = list_item[2]
        speakers = list_item[3].split("], [")
        #print(speakers)
        cat_speaker_count = list_item[4]
        cat_quote_count = list_item[5]

        if manual not in manual_data:
            manual_data[manual] = {
                #this is the total number of quotes by gendered speakers
                'total_counts': {
                    'total_male': 0,
                    'total_female': 0,
                    'total_supp': 0,
                },
                #this is the percentage of gendered speakers (excl. supp)
                'percent_counts': {
                    'percent_male':float(),
                    'percent_female':float(),
                },
                #this is sets of unique speakers by gender
                'unique_gender':{
                    'unique_males':set(),
                    'unique_females':set(),
                    'unique_supp':set(),
                },

            }

        #I don't think knowing the calling is actually all that important right now??
        for speaker in speakers:
            speaker = re.sub('[\[\]]','',speaker)
            speaker = speaker.split(', ')
            speaker_name = speaker[0]
            speaker_name = re.sub('^[\'\"]','',speaker_name)
            speaker_name = re.sub('[\'\"]$','',speaker_name)
            speaker_number = int(speaker[1])

            if gender == 'men':
                manual_data[manual]['unique_gender']['unique_males'].add(speaker_name)
                manual_data[manual]['total_counts']['total_male'] += speaker_number
            elif gender == 'women':
                manual_data[manual]['unique_gender']['unique_females'].add(speaker_name)
                manual_data[manual]['total_counts']['total_female'] += speaker_number
            elif gender == 'supp':
                manual_data[manual]['unique_gender']['unique_supp'].add(speaker_name)
                manual_data[manual]['total_counts']['total_supp'] += speaker_number

            if not re.search('NT_2019',manual):
                if speaker_name not in people_data:
                    people_data[speaker_name] = {
                        'total_quotes':0,
                        'total_CFM':0,
                        'total_GD':0,
                        'gender':gender,
                        'manuals':{
                            'CFM_BM_2019_T.xml':0,
                            'CFM_DC_2020_T.xml':0,
                            'CFM_OT_2021_T.xml':0,
                            'CFM_NT_2022_T.xml':0,
                            'GD_BM_2003_T.xml':0,
                            'GD_DC_2003_T.xml':0,
                            'GD_NT_1997_T.xml':0,
                            'GD_OT_2001_T.xml':0
                        },
                        'callings':set()
                    }
                people_data[speaker_name]['manuals'][manual] += speaker_number
                if re.match('CFM',manual):
                    people_data[speaker_name]['total_CFM'] += speaker_number
                elif re.match('GD',manual):
                    people_data[speaker_name]['total_GD'] += speaker_number
                people_data[speaker_name]['total_quotes'] += speaker_number
                people_data[speaker_name]['callings'].add(org_pub)

    era_data = {
        'CFM':{
            'manuals':set(),
            'total_counts': {
                'total_male': 0,
                'total_female': 0,
                'total_supp': 0,
            },
            #this is the percentage of gendered speakers (excl. supp)
            'percent_counts': {
                'percent_male':float(),
                'percent_female':float(),
            },
            #this is sets of unique speakers by gender
            'unique_gender':{
                'unique_males':set(),
                'unique_females':set(),
                'unique_supp':set(),
            },
        },
        'GD':{
            'manuals':set(),
            'total_counts': {
                'total_male': 0,
                'total_female': 0,
                'total_supp': 0,
            },
            #this is the percentage of gendered speakers (excl. supp)
            'percent_counts': {
                'percent_male':float(),
                'percent_female':float(),
            },
            #this is sets of unique speakers by gender
            'unique_gender':{
                'unique_males':set(),
                'unique_females':set(),
                'unique_supp':set(),
            },
        }
    }
    for manual in manual_data:
        percents = get_percent(manual_data[manual]['total_counts']['total_female'],manual_data[manual]['total_counts']['total_male'])
        manual_data[manual]['percent_counts']['percent_female'] = percents[0]
        manual_data[manual]['percent_counts']['percent_male'] = percents[1]

        if re.match('CFM', manual):
            era = 'CFM'
        elif re.match('GD', manual):
            era = 'GD'

        if manual not in era_data[era]['manuals'] and not re.search('NT_2019',manual):
            era_data[era]['manuals'].add(manual)
            era_data[era]['total_counts']['total_female'] += manual_data[manual]['total_counts']['total_female']
            era_data[era]['total_counts']['total_male'] += manual_data[manual]['total_counts']['total_male']
            era_data[era]['total_counts']['total_supp'] += manual_data[manual]['total_counts']['total_supp']
            era_data[era]['unique_gender']['unique_males'] |= manual_data[manual]['unique_gender']['unique_males']
            era_data[era]['unique_gender']['unique_females'] |= manual_data[manual]['unique_gender']['unique_females']
            era_data[era]['unique_gender']['unique_supp'] |= manual_data[manual]['unique_gender']['unique_supp']
       # print(manual, manual_data[manual])

        #pretty print
    with open('data_manual.csv', 'w', newline='', encoding='utf-8') as csv_writer:
        csvwriter = csv.writer(csv_writer)
        csvwriter.writerow(['Manual', 'Total Male Quotes','Total Female Quotes','Total Supps','Percent Gendered Quotes Male','Percent Gendered Quotes Female',
                            'Unique Men Count','Unique Women Count','Unique Supps Count','Unique Men Percent','Unique Women Percent','Unique Men','Unique Women', 'Unique Supps'])
        for manual in manual_data:
            percents = get_percent(len(manual_data[manual]['unique_gender']['unique_males']), len(manual_data[manual]['unique_gender']['unique_females']))
            csvwriter.writerow([manual,manual_data[manual]['total_counts']['total_male'],manual_data[manual]['total_counts']['total_female'],
                       manual_data[manual]['total_counts']['total_supp'],manual_data[manual]['percent_counts']['percent_male'],
                       manual_data[manual]['percent_counts']['percent_female'], len(manual_data[manual]['unique_gender']['unique_males']),
                       len(manual_data[manual]['unique_gender']['unique_females']), len(manual_data[manual]['unique_gender']['unique_supp']),
                       percents[0],percents[1],
                       list(manual_data[manual]['unique_gender']['unique_males']), list(manual_data[manual]['unique_gender']['unique_females']),
                       list(manual_data[manual]['unique_gender']['unique_supp'])
                       ])

    for era in era_data:
        percents = get_percent(era_data[era]['total_counts']['total_female'],era_data[era]['total_counts']['total_male'])
        era_data[era]['percent_counts']['percent_female'] = percents[0]
        era_data[era]['percent_counts']['percent_male'] = percents[1]

    #pretty print
    with open('data_era.csv', 'w', newline='', encoding='utf-8') as csv_writer:
        csvwriter = csv.writer(csv_writer)
        csvwriter.writerow(['Manual', 'Total Male','Total Female','Total Supps','Percent Male','Percent Female',
                            'Unique Men Count','Unique Women Count','Unique Supps Count','Unique Men Percent','Unique Women Percent',
                            'Unique Men','Unique Women', 'Unique Supps'])
        for era in era_data:
            percents = get_percent(len(era_data[era]['unique_gender']['unique_males']), len(era_data[era]['unique_gender']['unique_females']))
            csvwriter.writerow([era,era_data[era]['total_counts']['total_male'],era_data[era]['total_counts']['total_female'],
                       era_data[era]['total_counts']['total_supp'],era_data[era]['percent_counts']['percent_male'],
                       era_data[era]['percent_counts']['percent_female'], len(era_data[era]['unique_gender']['unique_males']),
                       len(era_data[era]['unique_gender']['unique_females']), len(era_data[era]['unique_gender']['unique_supp']),
                       percents[0],percents[1],
                       list(era_data[era]['unique_gender']['unique_males']), list(era_data[era]['unique_gender']['unique_females']),
                       list(era_data[era]['unique_gender']['unique_supp'])
                       ])

    #for person in people_data:
    #    print(person, people_data[person])

    with open('data_people.csv', 'w', newline='', encoding='utf-8') as csv_writer:
        csvwriter = csv.writer(csv_writer)
        csvwriter.writerow(
            ['Name', 'Gender','Total Quotes', 'Total CFM','Total GD', 'Callings',
             'CFM_BM_2019', 'CFM_DC_2020', 'CFM_OT_2021', 'CFM_NT_2022',
             'GD_BM_2003', 'GD_DC_2003,', 'GD_NT_1997', 'GD_OT_2001'])

        for person in people_data:
            new_row = []
            new_row.append(person)
            new_row.append(people_data[person]['gender'])
            new_row.append(people_data[person]['total_quotes'])
            new_row.append(people_data[person]['total_CFM'])
            new_row.append(people_data[person]['total_GD'])
            new_row.append(list(people_data[person]['callings']))
            for manual in people_data[person]['manuals']:
                new_row.append(people_data[person]['manuals'][manual])
            csvwriter.writerow(new_row)
    #what stats do I want
    #percentage of women speaking per manual (both quote count and speaker count)
    #percentage per calling...level? per manual?

    return

def get_quote_info():
    q_data = []
    full_quotes = []
    with open('quote_data.csv', encoding='utf-8') as csv_read:
        csvreader = csv.reader(csv_read)
        for row in csvreader:
            if len(row) > 0 and row[0] != 'Manual':
                q_data.append(row)
    partial_quote = []
    prev_data = []
    for quote in q_data:
        manual = quote[0]
        gender = quote[1]
        quote_text = quote[4]
        quote_partial = quote[-1]
        if gender != 'supp':
            if quote_partial == 'False':
                if len(partial_quote) != 0:
                    full_quotes.append([prev_data[0], prev_data[1], ' '.join(partial_quote), 'Connected'])
                    partial_quote = []
                    prev_data = []
                full_quotes.append([manual, gender, quote_text, quote_partial])
                partial_quote = []
                prev_data = []
            else:
                partial_quote.append(quote_text)
                prev_data = [manual, gender]
                #print(manual, gender, quote_text, quote_partial)
    #for full_quote in full_quotes:
    #    print(full_quote)
    print(len(full_quotes))
    return

def main():
    grab_from_corpus()
    #get_quote_info()

    import_speaker_data()
    link_speakers()
    get_stats()


    return

main()