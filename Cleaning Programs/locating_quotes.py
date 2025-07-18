import os
import re
import xml.etree.ElementTree as ET
import scripture_references
from bs4 import BeautifulSoup
import spacy
nlp = spacy.load('en_core_web_sm')

def check_quote(to_check):
    no_ellipses = re.sub(' \.','',to_check)
    quote_words = no_ellipses.split(' ')
    quote_len = len(quote_words)
    uppers = len(re.findall('[A-Z]',to_check))
    #if it's a title, it's not a quote
    #if it's less than 6 words long, it's definitely not a quote
    if round(uppers/quote_len, 2) > 0.4 or quote_len < 6:
        return False
    #else:
    #    print(to_check)
    return True

def find_entity(text_line):
    doc = nlp(text_line)
    #this is bad code for right now. I'm so sorry, but this has to get done.
    people = set()
    adding_entities = ['Church Handbook','First Presidency','Origen','Hermas','Elder Chi Hong (Sam) Wong',
                       'Chi Hong (Sam) Wong','Brother Page','John the Baptist','Christal','Sister Spafford',
                       'Bishop Victor L. Borwn','Brigham Young','E. Cecil McGavin','Elder Faust','Elder Packer',
                       'Elder Ulisses Soares','Joy D. Jones','Clare Middlemiss','Teaching in the Savior\'s Way',
                       'Ezra Taft Benson','Elder D. Todd Christofferson','D. Todd Christofferson','True to the Faith',
                       'James E. Talmage','Handbook 2','Hymns','John Taylor','The Family: A Proclamation to the World',
                       'Joseph Smith','John H. Groberg','Victor L. Brown','History of the Church','Our Heritage',
                       'James E. Faust','John A. Widtsoe','John K. Carmack','Teaching — No Greater Call',
                       'Old Testament Student Manual','Elder Holland','Ezra Thayer','President Monson',
                       'Hartman Rector Jr.']

    for added_entity in adding_entities:

        if re.search(added_entity, text_line):
            if added_entity == 'First Presidency':
                if not re.search('[of|in] the First Presidency',text_line):
                    people.add(added_entity)
            else:
                people.add(added_entity)

    not_relevant_entities = ['27th ed','3rd ed','59–60','5th ed','5th ed.','72–73','Aaron','Abednego','Abel','Abinadi',
                             'Adam','Ahab','Amalekites','Amalickiah','Ammonites','Ammoron','Amnon','Amulek','Amulon',
                             'Arise','Ashamed','Atonement','Balaam','Barnabas','Begotten','Begotten Son','Behold',
                             'Beloved Son','Bethel','Bilhah','Blessings','Bossy','Britannica','Carry You Home','Cast',
                             'Children','Christian Courage','Christlike','Church History','Church History Library',
                             'Creator','Dad','Destitute','Duty Calls','ed','Elders','Ensign','Eph','Ephesus','Ephraim',
                             'Faith','Galilee','Gethsemane','Gift','God','Godhead','Godly','Golgotha','Goliaths',
                             'Gomorrah','Good Cheer','Gospel','Gospel Doctrine','Gospel Questions',
                             'Grace','hallmark','Hezekiah','Him Crucified','His Atonement','His Son','Holy Being',
                             'Honesty','Hosanna','Hur','Imp','Israelites','Jehovah','Jer','Jesse','Jesus',
                             'Jesus Christ','Jesus Christ\'s','Jesus the Christ','Jesus\'','Joseph of Egypt',
                             'Joseph Smith Papers','Joseph Smith Translation','Judah','Judas','King Agrippa',
                             'King Ahab','King Benjamin','King Benjamin\'s','King Josiah','King Noah','King Saul',
                             'knelt','Knowledge','Lectures','lesbian behavior','Lesson 45','Lowly','meek','Mercy Meet',
                             'Millennium','Mole Crickets','Mom','Morianton','Mormon Doctrine','Naaman','Nazareth',
                             'Nebuchadnezzar','Nephi','Nephite','Nephites','Nineveh','Noah','Num','Older','once',
                             'Order','Ours','outdo','outward appearance','Passover','Patriarchal',
                             'Peter Went Out','Pharisee','Pharisees','Prepare Yourselves','Pride','Primary',
                             'Pure Christlike','Pure Testimony','Redeemer','Refer','Rehoboam','Relief Society',
                             'Respond','Resurrection','Riches','Rom','Sabbath','Said Caleb','Savior','Saul',
                             'Scriptures','Seek','Seek Learning','Sermon','Sherem','Shine Forth','Shun','Simple Gospel','Sin','socializes',
                             'Son','Sorrow','Spiritual Gifts','Spiritual Survival','Story Gems','Study Guide',
                             'The Prophet Lehi','Thou Art Converted','Thummim','Thy Kingdom Come','Thy Stakes',
                             'town hall','Twinkie','Wept Bitterly','Whom','Whom Thou Hast Sent','Writings','Ye',
                             'Ye Be Wearied','Lehi','Elijah','Goliath','Manuscript History','Laman','Lemuel','Gal',
                             'Lev','Prophet','Apostle','Paul','Grandpa Art','Grandma Lou','Eve','Brethren',
                             'Brigham Young University','Lutheran','Simon','Andrew','Samson','David','Enoch','Peter',
                             'Matt','Gabriel','Mary','Zacchaeus','Martha','Tiny Mary','Old Bob','Tommy','McConnells',
                             'Quorums','Elder King Follett','Quorum','Benbow','Jane','Rachel','Rebekah','Grandfather',
                             'Grandmother','Hannah','Samuel','Alvin','Isaac']
    for entity in doc.ents:

        if entity.label_ == "PERSON":
            #print(entity.text, ";", entity.start_char, ";",  entity.end_char, ";",  entity.label_)
            if not scripture_references.check_if_scripture(entity.text):
                if not re.match('[a-z]', entity.text):
                    if entity.text not in not_relevant_entities:
                        if len(re.findall('Brigham Young',text_line)) > 0 and len(re.findall('Brigham Young University', text_line)) > 0:
                            pass
                        else:
                            people.add(entity.text)
   # print("\n")
    if "Sam) Wong" in people:
        people.remove('Sam) Wong')
        people.add('(Sam) Wong')
    if 'Spencer W.] Kimball' in people:
        people.remove('Spencer W.] Kimball')
        people.add('Spencer W. Kimball')
    to_remove = set()

    for person in sorted(people,key=len)[:-1]:
        for check_person in people:
            if person != check_person:
                temp_person = re.sub('Elder ','',person)
                temp_person = re.sub('Sister ','',temp_person)
                temp_person = re.sub('\'s','',temp_person)

                if re.search(temp_person, check_person):
                    to_remove.add(person)

    for remove in to_remove:
        people.remove(remove)
    return people

def modify_quote(soup):

    text_elements = soup.find_all(['p','li'])
    for text_element in text_elements:
        current_text = text_element.string
        if current_text:
            text_element.clear()
            new_text = re.sub(r'([^:])\n\"', r'\1 ¶ ', current_text)
            text_element.string = new_text
            possible_quotes = re.finditer('\"[\s\S]*?\"',text_element.string)

            for pq in possible_quotes:
                if check_quote(pq.group()):
                    possible_citation = re.match(" [\(\[].*?[\)\]]", new_text[pq.end():])
                    if re.search('\(ChurchofJesusChrist.org\)',new_text) and re.search('The Family: A Proclamation to the World', new_text):
                        # hardcoded this because I *cannot* figure out what went wrong with this citation
                        #had to add AttributeError catch
                        possible_citation = 'The Family: A Proclamation to the World'
                    if possible_citation:
                        quote_citation = ''
                        try:
                            pc = re.sub("; italics added",'',possible_citation.group())
                        except AttributeError:
                            pc = possible_citation
                        grouped_citation = pc.split('; ')
                        scripture_ref = False
                        if len(grouped_citation) == 1:
                            # print(len(grouped_citation[0].split(' ')))
                            if len(grouped_citation[0].split(' ')) < 8:
                                scripture_ref = scripture_references.check_if_scripture(grouped_citation[0])
                            if not scripture_ref:

                                if not re.search('[0-9]', possible_citation.group()):
                                    if re.search('Hymns', possible_citation.group()) \
                                            or re.search('Gospel Topics', possible_citation.group()) \
                                            or re.search('No Greater Call', possible_citation.group()) \
                                            or re.search('Explanatory Introduction', possible_citation.group()) \
                                            or re.search('National Press Club', possible_citation.group()):
                                        quote_citation = possible_citation.group()
                                else:
                                    quote_citation = possible_citation.group()
                        else:
                            if re.search('Conference Report', possible_citation.group()) or re.search('Ensign',
                                                                                                      possible_citation.group()):
                                quote_citation = possible_citation.group()
                            # if it has more than four semicolons, it's typically just scriptures
                            elif len(grouped_citation) < 3:
                                citation_1 = grouped_citation[0]
                                citation_1_ref = scripture_references.check_if_scripture(citation_1)
                                citation_2 = grouped_citation[1]
                                citation_2_ref = scripture_references.check_if_scripture(citation_2)
                                if citation_1_ref and citation_2_ref:
                                    # both scriptures
                                    scripture_ref = True
                                #  print(possible_citation.group())
                                if not citation_1_ref and not citation_2_ref:
                                    quote_citation = possible_citation.group()

                                elif citation_1_ref or citation_2_ref:
                                    if not citation_1_ref and re.search('[0-9]', citation_1):
                                        quote_citation = possible_citation.group()
                                    elif not citation_2_ref and re.search('Teaching', citation_2):
                                        quote_citation = possible_citation.group()
                                    else:
                                       # print(grouped_citation)
                                        scripture_ref = True
                            else:
                                scripture_ref = True

                        if quote_citation != '':
                            quote_citation = re.sub("^ \((in )?", '', quote_citation)
                            quote_citation = re.sub("\)$", '', quote_citation)
                            #quote_citation = re.sub("^ ", '', quote_citation)
                            people = find_entity(new_text)
                            citation_folks = set()
                            elsewhere_folks = set()
                            character_folks = set()
                            embedded_folks = set()
                            if len(people) > 0:
                                #print(new_text)
                                #print(pq.start())
                                quote_start = pq.start()-1
                               # print(quote_start,pq.start())

                                if quote_start < 0:
                                    quote_start = 0
                                not_quote_citation_text = new_text[:quote_start] + " {QUOTED TEXT} {CITATION}" \
                                                          + new_text[pq.end()+possible_citation.end():]
                                not_quote_citation_text = re.sub('\{CITATION\}.*?\)\.$','{CITATION}',not_quote_citation_text)
                                #not_quote_citation_text = re.sub('\r\n',' ',not_quote_citation_text)
                               # print(not_quote_citation_text)

                                for person in people:
                                    if re.search(person, pq.group()):
                                        if re.search('«',pq.group()):
                                            embedded_folks.add(person)
                                        else:
                                            character_folks.add(person)
                                    if re.search(person, possible_citation.group()):
                                        citation_folks.add(person)
                                    if re.search(person,not_quote_citation_text):
                                        elsewhere_folks.add(person)
                            else:
                                #okay, so these are the Neal A. Maxwell quotes from the DC_2003 manual.
                                elsewhere_folks.add('Neal A. Maxwell')


                            quote_speaker = []
                            # TODO: Embedded citations
                            if len(embedded_folks) > 0:

                                #there are possibly embedded people
                                pass
                            elif len(citation_folks) == 1 and citation_folks == elsewhere_folks:
                                #There is one citation person and one elsewhere person and they are the same
                                #There are no embedded quotes
                                quote_speaker.append(citation_folks.pop())
                            elif len(citation_folks) == 1 and len(elsewhere_folks) == 0:
                                #there is one citation person and no one anywhere
                                quote_speaker.append(citation_folks.pop())
                                # print(quote_speaker)
                            elif len(citation_folks) > 1 and len(elsewhere_folks) == 0:
                                # There are multiple people cited, but no one elsewhere
                                 for cfolk in citation_folks:
                                     if not re.match('Joseph Smith\'s',cfolk):
                                        quote_speaker.append(cfolk)
                            elif len(elsewhere_folks) == 1 and len(citation_folks) == 0:
                                #there is one elsewhere person and no one anywhere
                                quote_speaker.append(elsewhere_folks.pop())

                            elif len(elsewhere_folks) > 0 and len(citation_folks) == 0:
                                #there are more than one elsewhere people and no citation people
                                #print(not_quote_citation_text)
                                temp_not_quote_citation_text = re.sub(r'([A-Z])\.',r'\1',not_quote_citation_text)
                                temp_not_quote_citation_text = re.sub(r'(Jr)\.',r'\1',temp_not_quote_citation_text)
                                split_nqct = re.split('[\.\?]',temp_not_quote_citation_text)
                                more_possible_speakers = []
                                for line in split_nqct:

                                    if re.search('\{QUOTED TEXT\}',line):
                                        #print(line)
                                        line = re.sub(r' ([A-Z]) ',r' \1. ',line)
                                        line = re.sub(r' (Jr) ',r' \1. ',line)
                                        #print(line)
                                        for ef in elsewhere_folks:
                                            if re.search(ef,line):
                                                more_possible_speakers.append(ef)
                                               # print("Possible speaker: ",ef)
                                #TODO: multiple people mentioned in sentence before quote
                                if len(more_possible_speakers) > 1:
                                    #In these remaining cases, there's usually two people mentioned in the sentence
                                    #and in some cases, it might be easy-ish to figure out who said it
                                    #i.e. "Person --of the Q12-- said"
                                    pass
                                elif len(more_possible_speakers) == 1:
                                    #One person mentioned in sentence before quote
                                    quote_speaker.append(more_possible_speakers[0])
                                else:
                                    #so, the thing going wrong is one of two things: the speaker is mentioned elsewhere
                                    #ORRRR there's a split quote. which I've got to deal with anyways.
                                    pass
                            #TODO: Multiple people cited, multiple people elsewhere
                            else:
                                #pass

                                #print("\t",citation_folks, elsewhere_folks)
                                if 'Joseph Fielding Smith' in citation_folks:
                                    quote_speaker.append(elsewhere_folks.pop())
                                elif 'Edward L. Kimball' in citation_folks:
                                    quote_speaker.append(elsewhere_folks.pop())
                                elif 'Bruce R. McConkie' in citation_folks:
                                    quote_speaker.append(elsewhere_folks.pop())
                                elif 'History of the Church' in citation_folks:
                                    if len(elsewhere_folks) == 1:
                                        #This isn't foolproof, but it's the best I'm gonna get
                                        quote_speaker.append(elsewhere_folks.pop())
                                    else:
                                        print(new_text)
                                        print("\t", elsewhere_folks)
                                else:
                                  #  print(new_text)
                                 #   print("\t", elsewhere_folks)
                                    combined_folks = citation_folks.union(elsewhere_folks)
                                    #print("\t",combined_folks)
                           # print(pq.group())
                            #print("\t",quote_speaker)
                            #print("\t",quote_citation)

                            #adds the quotation tag
                            speaker = ', '.join(str(x) for x in quote_speaker)
                            contents_start = pq.start() - 1
                            if contents_start < 0:
                                contents_start = 0
                            quote_tag = soup.new_tag('quotation',speaker=speaker,citation=quote_citation,string=pq.group())
                            try:
                                text_element.clear()
                            except AttributeError:
                                print(text_element)
                            new_contents = [new_text[:contents_start],quote_tag,new_text[pq.end()+1:]]
                            text_element.extend(new_contents)
                        else:
                            #don't do anything with this because they're basically all scriptures, except for some
                            #video narration that I'm ignoring
                            pass
                    #TODO: What if it's a quote that doesn't have a citation?
                    else:
                        pass
    return




def main():
    to_modify_dir = "C:\\Users\elena\PycharmProjects\MA_Thesis\Full_Manuals\Sections_XML"
    modified_dir = "C:\\Users\elena\PycharmProjects\MA_Thesis\Full_Manuals\Quotations_XML"

    for manual in os.listdir(to_modify_dir):
        print('\n',manual)
        to_modify_manual = to_modify_dir + "\\" + manual
        modified_manual = modified_dir + "\\" + manual
        with open(to_modify_manual,'r', encoding='utf-8') as f:
            file = f.read()
        soup = BeautifulSoup(file,'xml')
        modify_quote(soup)
      #  hold = input("wait a sec")
        with open(modified_manual, 'w', encoding='utf-8') as modifying_manual:
            modifying_manual.write(soup.prettify())

main()