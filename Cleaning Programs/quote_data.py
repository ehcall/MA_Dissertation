import os
from bs4 import BeautifulSoup
import csv
import re

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
def main():
    qdata = dict()

    quote_texts = "C:\\Users\elena\PycharmProjects\MA_Thesis\Full_Manuals\Sources_XML"
    for manual in os.listdir(quote_texts):
        analyzing_manual = quote_texts + "\\" + manual

        with open(analyzing_manual, 'r', encoding='utf-8') as f:
            file = f.read()
        soup = BeautifulSoup(file, 'xml')
        quotations = soup.find_all(['quotation'])
        qdata[manual] = {
            'men':dict(),
            'women':dict(),
            'supp':dict()
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
        i=0
        for dq in dupe_quotes:
            #print(dq['citation'])
            if prev_citation == dq['citation']:
                full_text.append(dq.text.strip())
            else:
                if i != 0:
                    #print("\t",full_text, dupe_speaker, prev_citation)
                    add_to_dict(prev_quotation, qdata, dupe_speaker, manual, ' '.join(full_text))
                else:
                    i+=1
                prev_citation = dq['citation']
                dupe_speaker = dq['speaker']
                dupe_manual = manual
                prev_quotation = dq
                full_text = []
                full_text.append(dq.text.strip())
                   # print(dq['citation'])
        #print("\t", full_text, dupe_speaker, prev_citation)
        add_to_dict(prev_quotation, qdata, dupe_speaker, manual, ' | '.join(full_text))



    qdata_rows = []

    for manual in qdata:
       # print(manual)
        for gender in qdata[manual]:
          #  print("\t",gender)
            for speaker in sorted(qdata[manual][gender]):
               # print("\t\t",speaker)
                #quote_count = 0
                for speaker_quote in qdata[manual][gender][speaker]:
                    #quote_count += 1
                   # print("\t\t\tQuote ",quote_count,": ")

                    speaker_citation = speaker_quote[0]
                    speaker_citation = re.sub('See also ', '', speaker_citation)
                    speaker_citation = re.sub('[sS]ee ', '', speaker_citation)
                    if re.match(speaker,speaker_citation):
                        speaker_citation = re.sub(speaker,'',speaker_citation)
                    speaker_citation = re.sub('^[:,] ','',speaker_citation)
                    speaker_citation = re.sub(' or Liahona','',speaker_citation)

                    speaker_text = speaker_quote[1]
                    #print(speaker, "\n\t", speaker_citation, "\n\t\t", speaker_text)
                    new_row = [manual, gender, speaker, speaker_citation, speaker_text, speaker_quote[2]]
                    qdata_rows.append(new_row)

    with open('C:\\Users\elena\PycharmProjects\MA_Thesis\Cleaning Programs\quote_data.csv', 'w', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Manual','Gender','Speaker','Citation','Text','Partial'])
        csvwriter.writerows(qdata_rows)

    return

#main()