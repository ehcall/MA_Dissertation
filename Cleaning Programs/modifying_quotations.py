import os
import re
from bs4 import BeautifulSoup

def add_gender(speaker_name):
    gender = 'M - Male'
    supp_mats = ['Old Testament Student Manual','Hymns','Teaching — No Greater Call','Church Handbook','Gospel Topics',
                 'Handbook 2','History of the Church','Our Heritage','Teaching in the Savior\'s Way','True to the Faith']

    females = ['Ann M. Dibb','Bonnie H. Cordon','Bonnie L. Oscarson','Elaine S. Dalton','Elmina S. Taylor',
               'Janette Hales Beckham','Jean B. Bingham','Joy D. Jones','Julie B. Beck','Laura Russell Bunker',
               'Linda S. Reeves','Margaret D. Nadauld','Mary Ellen Smoot','Mary Isabella Horne','Michelle Craig',
               'Serepta M. Heywood','Sharon Eubank','Sheri L. Dew','Vicki F. Matsumori','Virginia H. Pearce',
               'Virginia U. Jensen', 'Chieko Okazaki','Wendy Nelson','Belle S. Spafford','Cori Christensen',
               'Eliza R. Snow','Lucy Mack Smith',]
    if speaker_name in supp_mats:
        #Hymns could probably be adjusted based on who wrote the hymn, but they're kind of treated as gender neutral
        gender = 'S - Supp Mats'
    elif speaker_name in females:
        gender = 'F - Female'
    #print(speaker_name)
    return gender

def lengthen_name(speaker_name):
    new_speaker_name = ''
    if speaker_name == 'Ballard':
        new_speaker_name = 'M. Russell Ballard'
    elif speaker_name == 'Benson':
        new_speaker_name = 'Ezra Taft Benson'
    elif speaker_name == 'Bradford':
        new_speaker_name = 'William R. Bradford'
    elif speaker_name == 'Eyring':
        new_speaker_name = 'Henry B. Eyring'
    elif speaker_name == 'Faust':
        new_speaker_name = 'James E. Faust'
    elif speaker_name == 'Hinckley':
        new_speaker_name = 'Gordon B. Hinckley'
    elif speaker_name == 'Holland':
        new_speaker_name = 'Jeffrey R. Holland'
    elif speaker_name == 'Hyde':
        new_speaker_name = 'Orson Hyde'
    elif speaker_name == 'Kimball':
        new_speaker_name = 'Spencer W. Kimball'
    elif speaker_name == 'Maxwell':
        new_speaker_name = 'Neal A. Maxwell'
    elif speaker_name == 'McConkie':
        new_speaker_name = 'Bruce R. McConkie'
    elif speaker_name == 'Monson':
        new_speaker_name = 'Thomas S. Monson'
    elif speaker_name == 'Talmage':
        new_speaker_name = 'James E. Talmage'
    #may not work for all cases
    elif speaker_name == 'Smith':
        new_speaker_name = 'Joseph F. Smith'
    elif speaker_name == 'Wirthlin':
        new_speaker_name = 'Joseph B. Wirthlin'
    elif speaker_name == 'Young':
        new_speaker_name = 'Brigham Young'
    else:
        new_speaker_name = speaker_name
    return new_speaker_name

def standardize_names(soup):
    quotations = soup.find_all('quotation')
    for quotation in quotations:
        speakers = quotation['speaker'].split(', ')
        updated_speakers = []
        gender = ''
        #print(speakers)
        genders = set()
        for speaker in speakers:
            speaker = re.sub('Elder ','',speaker)
            speaker = re.sub('President ','',speaker)
            speaker = re.sub('Prophet ','',speaker)
            speaker = re.sub('Bishop ','',speaker)
            if speaker != 'Teaching in the Savior\'s Way':
                speaker = re.sub('\'s','',speaker)
            if len(speaker.split(' ')) == 1 and speaker != '' and speaker != 'Hymns':
                #print(speaker," ; ",quotation.string)
                speaker = lengthen_name(speaker)
               # print(speaker)
            updated_speakers.append(speaker)
            genders.add(add_gender(speaker))
        if len(genders) > 1:
            if 'S - Supp Mats' in genders and 'M - Male':
                gender = 'M - Male'
            else:
              #  print(genders, speakers)
                gender = 'X - Mixed'
        else:
            gender = genders.pop()
        if updated_speakers[0] == '':
            print(quotation.text)
        quotation['speaker'] = updated_speakers
        quotation['gender'] = gender
        #print(quotation['speaker'])

    return
def main():
    to_modify_dir = "C:\\Users\elena\PycharmProjects\MA_Thesis\Full_Manuals\Quotations_XML"
    modified_dir = "C:\\Users\elena\PycharmProjects\MA_Thesis\Full_Manuals\Sources_XML"

    for manual in os.listdir(to_modify_dir):
      #  hold_up = input("wait a sec")
        to_modify_manual = to_modify_dir + "\\" + manual
        modified_manual = modified_dir + "\\" + manual

        with open(to_modify_manual, 'r', encoding='utf-8') as f:
            file = f.read()
        soup = BeautifulSoup(file, 'xml')
        standardize_names(soup)
        with open(modified_manual, 'w', encoding='utf-8') as modifying_manual:
            modifying_manual.write(soup.prettify())

main()