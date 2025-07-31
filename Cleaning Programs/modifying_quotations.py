import os
import re
from bs4 import BeautifulSoup

def add_gender(speaker_name):
    gender = 'M - Male'
    supp_mats = ['Old Testament Student Manual','Hymns','Teaching — No Greater Call','Church Handbook','Gospel Topics',
                 'Handbook 2','History of the Church','Our Heritage','Teaching in the Savior\'s Way','True to the Faith',
                 'Children\'s Songbook','Revelations in Context','Church History in the Fulness of Times',
                 'The Life and Teachings of Jesus and His Apostles', 'Encyclopedia of Mormonism']

    females = ['Ann M. Dibb','Bonnie H. Cordon','Bonnie L. Oscarson','Elaine S. Dalton','Elmina S. Taylor',
               'Janette Hales Beckham','Jean B. Bingham','Joy D. Jones','Julie B. Beck','Laura Russell Bunker',
               'Linda S. Reeves','Margaret D. Nadauld','Mary Ellen Smoot','Mary Isabella Horne','Michelle Craig',
               'Serepta M. Heywood','Sharon Eubank','Sheri L. Dew','Vicki F. Matsumori','Virginia H. Pearce',
               'Virginia U. Jensen', 'Chieko Okazaki','Wendy Nelson','Belle S. Spafford','Cori Christensen',
               'Eliza R. Snow','Lucy Mack Smith','Linda K. Burton', 'Priscilla Sampson-Davis', 'Wendy W. Nelson',
               'Marjorie P. Hinckley']
    if speaker_name in supp_mats:
        #Hymns could probably be adjusted based on who wrote the hymn, but they're kind of treated as gender neutral
        gender = 'S - Supp Mats'
    elif speaker_name in females:
        gender = 'F - Female'
    #print(speaker_name)
    return gender

def lengthen_name(speaker_name):
    new_speaker_name = ''
    if speaker_name == '':
        speaker_name = 'Joseph Smith'
    if speaker_name == 'The Family: A Proclamation to the World':
        speaker_name = 'First Presidency'
    if speaker_name == 'President Monson':
        speaker_name = 'Thomas S. Monson'
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
    elif re.search('Kimball', speaker_name):
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
    elif speaker_name == 'Chi Hong':
        new_speaker_name = 'Chi Hong (Sam) Wong'
    elif speaker_name == 'First Presidency':
        new_speaker_name = 'The First Presidency'
    elif speaker_name == 'Richards':
        #This one is tricky because it's a 'Richards recalled that Joseph Smith told him' situation
        new_speaker_name = 'Willard Richards'
    elif speaker_name == 'Joseph':
        new_speaker_name = 'Joseph Smith'
    elif speaker_name == 'Woodruff':
        new_speaker_name = 'Wilford Woodruff'
    elif speaker_name == 'Wendy Nelson':
        new_speaker_name = 'Wendy W. Nelson'
    elif speaker_name == 'Uchtdorf':
        new_speaker_name = 'Dieter F. Uchtdorf'
    else:
        new_speaker_name = speaker_name
    return new_speaker_name

def standardize_names(soup, all_speakers):
    quotations = soup.find_all('quotation')
    for quotation in quotations:
        speakers = quotation['speaker'].split(', ')
        updated_speakers = []
        gender = ''
        genders = set()
        for speaker in speakers:

            updated_speaker = lengthen_name(speaker)
            updated_speakers.append(updated_speaker)
            all_speakers.add(updated_speaker)
            genders.add(add_gender(updated_speaker))
        if len(genders) > 1:
            if 'S - Supp Mats' in genders and 'M - Male':
                gender = 'M - Male'
            else:
              #  print(genders, speakers)
                gender = 'X - Mixed'
        else:
            gender = genders.pop()
        if len(updated_speakers) > 1:
            quotation['speaker'] = ', '.join(updated_speakers)
        else:
            quotation['speaker'] = updated_speakers
        quotation['gender'] = gender
        #print(quotation['speaker'])

    return
def main():
    to_modify_dir = "C:\\Users\elena\PycharmProjects\MA_Thesis\Full_Manuals\Quotations_XML"
    modified_dir = "C:\\Users\elena\PycharmProjects\MA_Thesis\Full_Manuals\Sources_XML"
    all_speakers = set()
    for manual in os.listdir(to_modify_dir):
      #  hold_up = input("wait a sec")
        to_modify_manual = to_modify_dir + "\\" + manual
        modified_manual = modified_dir + "\\" + manual

        with open(to_modify_manual, 'r', encoding='utf-8') as f:
            file = f.read()
        soup = BeautifulSoup(file, 'xml')
        standardize_names(soup, all_speakers)
        with open(modified_manual, 'w', encoding='utf-8') as modifying_manual:
            modifying_manual.write(soup.prettify())

    #for speaker_name in all_speakers:
       # print(speaker_name)
#main()