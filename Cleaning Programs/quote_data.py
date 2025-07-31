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

    with open('C:\\Users\elena\PycharmProjects\MA_Thesis\Cleaning Programs\quote_data.csv', 'w',
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
    with open('C:\\Users\elena\PycharmProjects\MA_Thesis\Cleaning Programs\speaker_data.xml', 'r', encoding='utf-8') as f:
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
    '''
    citation_split = citation.split('; ')
    for cs in citation_split:
        cs = re.sub('^or ', '', cs)
        cs = re.sub('^also ', '', cs)
        cs = re.sub('^ed\., ', '', cs)
        cs = re.sub('^in ', '', cs)
        cs = re.sub('^comp\., ', '', cs)
        cs = re.sub('^page ', '', cs)

        if (re.search('Ensign,', cs) or re.search('Conference Report',cs)) and (citation_month == '04' or citation_month == '10'):
            if 'LDS Conf' not in citation_dict:
                citation_dict['LDS Conf'] = []
            citation_dict['LDS Conf'].append(quote_id)
       '''
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
                    #last_calling = "DECEASED AT PUB - " + calling_option['org']
                    return sc, calling_option['org']
                if calling_option['start'] < citation_date < calling_option['end']:
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
    basic_data = {}
    quote_id = 0
    for qd in q_data:
        quote_id += 1
        manual = qd[0]
        pub_date = re.search('[0-9]{4}',manual).group()
        gender = qd[1]
        speaker = qd[2]
        citation = qd[3]
        citation_date = get_citation_data(citation, speaker, gender, quote_id)
        #print(pub_date, citation_date)
        quote = qd[4]
        partial = qd[5]
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
            else:
                new_pub_date = adjust_date(pub_date)
                calling_org_citation = get_calling(new_pub_date, speaker, pub_date)
                calling_at_cite = calling_org_citation[0]
                org_at_cite = calling_org_citation[1]
                calling_org_pub = get_pub_calling(pub_date, speaker)
                org_at_pub = calling_org_pub[1]

        if manual not in basic_data:
            basic_data[manual] = {}
        if gender not in basic_data[manual]:
            basic_data[manual][gender] = {}
        if org_at_pub not in basic_data[manual][gender]:
            basic_data[manual][gender][org_at_pub] = {}
        if speaker not in basic_data[manual][gender][org_at_pub]:
            basic_data[manual][gender][org_at_pub][speaker] = 0
        basic_data[manual][gender][org_at_pub][speaker] += 1

    #print(basic_data)
    basic_data_list = []
    for manual in basic_data:
        for gender in basic_data[manual]:
            for org in basic_data[manual][gender]:
                org_people = []
                total_quote_count = 0
                for person in basic_data[manual][gender][org]:
                    #print(person)
                    org_people.append([person, basic_data[manual][gender][org][person]])
                    total_quote_count+= basic_data[manual][gender][org][person]
                basic_data_list.append([manual, gender, org, org_people, len(org_people), total_quote_count])

    with open('speaker_quote_data.csv','w',encoding='utf-8') as csv_writer:
        csvwriter = csv.writer(csv_writer)
        csvwriter.writerows(basic_data_list)

        #if gender != 'supp':
       #     if speaker in people_dict:
       #         #print(qd)
       #         print("\t",speaker, people_dict[speaker]['gender'], people_dict[speaker]['callings'])

        #if speaker in people_dict:
          #  print(speaker, people_dict[speaker])


    return
def main():
    grab_from_corpus()
    import_speaker_data()
    link_speakers()


    return

main()