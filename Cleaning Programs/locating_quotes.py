import os
import re
import scripture_references
from bs4 import BeautifulSoup
import spacy
from spacy.matcher import DependencyMatcher
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

def check_citation(to_check):
    if re.match('\([Ss]ee', to_check):
        if re.match('\([Ss]ee (also )?Teaching ', to_check) or \
                re.match('\([Ss]ee (also )?True ', to_check) or \
                re.match('\([Ss]ee [b-z]', to_check) or \
                re.search('item [0-9]', to_check) or \
                re.match('\([Ss]ee (also )?Doctrines ', to_check):
            return False
        else:
            if re.search("Christofferson", to_check) or \
                    re.search("Andersen", to_check) or \
                    re.search("Packer", to_check):
                return False
            else:
                return True
    else:
        if re.search('Hymns,',to_check):
            #idk if any of the hymns are actually quoted?? keep this separate just in case
            return False
        elif re.match('\([cpsf]',to_check) or \
                re.search('gave some examples',to_check) or \
                re.search('media-library',to_check) or \
                re.search('Our Heritage, page 101',to_check) or \
                re.match('\(For the',to_check) or \
                re.match('\(Note',to_check) or \
                re.match('\([0-9]',to_check) or \
                re.match('\(D\&',to_check):
            return False
        else:
            return True

nlp.add_pipe('merge_entities')
def speaker_from_verb(text_line):
    speaker = ''
    # https://stackoverflow.com/questions/67259823/problem-to-extract-ner-subject-verb-with-spacy-and-matcher
    # add pipe is outside this function; I don't think it's causing issues for the other speaker stuff
    pattern = [
        {
            "RIGHT_ID": "person",
            "RIGHT_ATTRS": {"ENT_TYPE": "PERSON", "DEP": "nsubj"},
        },
        {
            "LEFT_ID": "person",
            "REL_OP": "<",
            "RIGHT_ID": "verb",
            "RIGHT_ATTRS": {"POS": "VERB"},
        }
    ]
    matcher = DependencyMatcher(nlp.vocab)
    matcher.add('PERVERB',[pattern])
    speaker_doc = nlp(text_line)
    matches = matcher(speaker_doc)
    speaking_verbs = ['told','said','recalled','explained','issued','announced']
    tbd = []
    for match in matches:
        match_id, (start, end) = match
        if str(speaker_doc[end]) in speaking_verbs:
            tbd = []
            return str(speaker_doc[start])
        elif str(speaker_doc[start]) == 'Emma' and str(speaker_doc[end]) == 'support':
            tbd = []
            return 'Lucy Mack Smith'
        tbd.append([speaker_doc[start], speaker_doc[end]])
    if len(tbd) > 0:
        return 'History of the Church'
    else:
        return ''

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
                        if len(re.findall('Brigham Young',entity.text)) > 0 and len(re.findall('Brigham Young University', text_line)) > 0:
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
            new_text = re.sub(r'([^:])\r?\n\"', r'\1 ¶ ', current_text)
            text_element.string = new_text
            possible_quotes = re.finditer('\".*?\"',text_element.string)
            pq_count = re.findall('\".*?\"',text_element.string)

            needs_citation = []
            for pq in possible_quotes:

                if check_quote(pq.group()):

                    non_quotation_text = new_text[:pq.start()] + new_text[pq.end():]
                    possible_citation = re.match("\?? \(.*?\)", new_text[pq.end():])
                    possible_citations = re.finditer("\(.*?\)", non_quotation_text)
                    pc_count = re.findall("\(.*?\)", non_quotation_text)

                    plausible_citations = []
                    if len(pc_count) < 1:
                        #no possible citation could be found in the paragraph
                        #TODO: come back
                        #print(pq.group())
                        pass
                    else:
                        has_been_scripture = False
                        for option in possible_citations:

                            #scripture_ref = False
                            scripture_ref = scripture_references.check_if_scripture(option.group())
                            if not scripture_ref:
                                if not re.search('[0-9]',option.group()):
                                    if re.search('Hymns', option.group()) \
                                            or re.search('Gospel Topics', option.group()) \
                                            or re.search('No Greater Call', option.group()) \
                                            or re.search('Explanatory Introduction', option.group()) \
                                            or re.search('National Press Club', option.group()):
                                        #TODO: this is a citation
                                        plausible_citations.append(option.group())

                                else:
                                    if check_citation(option.group()):
                                        plausible_citations.append(option.group())
                            else:
                                has_been_scripture = True
                            if re.match('\(36\)',option.group()):
                                plausible_citations.append('Our Heritage, 36')
                                has_been_scripture = False
                        if len(plausible_citations) < 1 and has_been_scripture:
                            if re.search('Elder Haight', non_quotation_text):
                                #TODO: deal with Haight
                                pass
                            #it's probably a scripture otherwise though
                        elif len(plausible_citations) < 1 and not has_been_scripture:
                            if re.search('[Pp]roclamation',non_quotation_text):
                                print(pq.group())
                            #otherwise it's a scripture or a question

    return

'''
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
                                quote_start = pq.start()-1
                                if quote_start < 0:
                                    quote_start = 0
                                not_quote_citation_text = new_text[:quote_start] + " {QUOTED TEXT} {CITATION}" \
                                                          + new_text[pq.end()+possible_citation.end():]
                                not_quote_citation_text = re.sub('\{CITATION\}.*?\)\.$','{CITATION}',not_quote_citation_text)
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

                            # We are ignoring embedded quotes
                            if len(citation_folks) == 1 and citation_folks == elsewhere_folks:
                                #There is one citation person and one elsewhere person and they are the same
                                quote_speaker.append(citation_folks.pop())
                            elif len(citation_folks) == 1 and len(elsewhere_folks) == 0:
                                #there is one citation person and no one anywhere
                                quote_speaker.append(citation_folks.pop())
                            elif len(citation_folks) > 1 and len(elsewhere_folks) == 0:
                                # There are multiple people cited, but no one elsewhere
                                 for cfolk in citation_folks:
                                     if not re.match('Joseph Smith\'s',cfolk):
                                        quote_speaker.append(cfolk)
                            elif len(elsewhere_folks) == 1 and len(citation_folks) == 0:
                                #there is one elsewhere person and no one anywhere
                                quote_speaker.append(elsewhere_folks.pop())
                            elif (len(elsewhere_folks) > 0 and len(citation_folks) == 0) or \
                                    (len(elsewhere_folks) > 0 and re.search('quoted',possible_citation.group())):
                                #there are more than one elsewhere people and no citation people
                                #orrrr there are citation people, but there's a 'quoted by/in' in the citation
                                temp_not_quote_citation_text = re.sub(r'([A-Z])\.',r'\1',not_quote_citation_text)
                                temp_not_quote_citation_text = re.sub(r'(Jr)\.',r'\1',temp_not_quote_citation_text)
                                split_nqct = re.split('[\.\?]',temp_not_quote_citation_text)
                                more_possible_speakers = []
                                for line in split_nqct:

                                    if re.search('\{QUOTED TEXT\}',line):
                                        line = re.sub(r' ([A-Z]) ',r' \1. ',line)
                                        line = re.sub(r' (Jr) ',r' \1. ',line)
                                        for ef in elsewhere_folks:
                                            if re.search(ef,line):
                                                more_possible_speakers.append(ef)
                                if len(more_possible_speakers) > 1:
                                    #In these remaining cases, there's usually two people mentioned in the sentence
                                    quote_speaker.append(speaker_from_verb(new_text))
                                elif len(more_possible_speakers) == 1:
                                    #One person mentioned in sentence before quote
                                    quote_speaker.append(more_possible_speakers[0])
                                else:
                                    #so, the thing going wrong is one of two things: the speaker is mentioned elsewhere
                                    #ORRRR there's a split quote. which I've got to deal with anyways.
                                    pass
                            elif len(citation_folks) == 1 and len(elsewhere_folks) == 1:
                                quote_speaker.append(elsewhere_folks.pop())
                            else:
                                if 'Joseph Fielding Smith' in citation_folks:
                                   # print('JFS')
                                    quote_speaker.append(elsewhere_folks.pop())
                                elif 'Edward L. Kimball' in citation_folks:
                                    quote_speaker.append(elsewhere_folks.pop())
                                elif 'Bruce R. McConkie' in citation_folks:
                                    quote_speaker.append(elsewhere_folks.pop())
                                elif 'John A. Widtsoe' in citation_folks:
                                    quote_speaker.append(elsewhere_folks.pop())
                                elif 'History of the Church' in citation_folks:

                                    if len(elsewhere_folks) == 1:
                                        #This isn't foolproof, but it's the best I'm gonna get

                                        quote_speaker.append(elsewhere_folks.pop())
                                    else:
                                        quote_speaker.append(speaker_from_verb(new_text))
                                        #print(elsewhere_folks)
                                else:
                                    #this gets the element that's shared between the two sets
                                    shared_speakers = elsewhere_folks & citation_folks
                                    if shared_speakers:
                                        quote_speaker.append(shared_speakers.pop())
                                    else:
                                        quote_speaker.append(speaker_from_verb(new_text))

                            #adds the quotation tag
                            speaker = ', '.join(str(x) for x in quote_speaker)

                            contents_start = pq.start() - 1
                            if contents_start < 0:
                                contents_start = 0

                            try:
                                text_element.clear()
                            except AttributeError:
                                print(text_element)

                            new_contents = []
                            start_quote = 0
                            if not (re.match('\?',quote_citation) and speaker == 'Neal A. Maxwell'):
                                if len(needs_citation) > 0:
                                    if re.search('Why We Are Organized',quote_citation):
                                        speaker = 'Julie B. Beck'
                                    for quote_section in needs_citation:
                                        new_contents.append(new_text[start_quote:quote_section.start()-1])
                                        quote_tag = soup.new_tag('quotation', speaker=speaker, citation=quote_citation,
                                                                 string=quote_section.group(), partial_quote="True")
                                        new_contents.append(quote_tag)
                                        start_quote = quote_section.end() + 1

                                    quote_tag = soup.new_tag('quotation', speaker=speaker, citation=quote_citation,
                                                             string=pq.group(), partial_quote="True")
                                    new_contents.append(new_text[start_quote:contents_start])
                                    new_contents.append(quote_tag)
                                    new_contents.append(new_text[pq.end() + 1:])
                                else:
                                    #Hardcoded thing I had to fix
                                    if re.search('the most important preparation is of yourself', new_text):
                                        speaker = 'Boyd K. Packer'
                                        quote_citation = 'Boyd K. Packer, Teach Ye Diligently [1975], 219'
                                    if re.search('Elders\' Journal', quote_citation) and speaker == 'Neal A. Maxwell':
                                        speaker = 'Joseph Smith'
                                    quote_tag = soup.new_tag('quotation', speaker=speaker, citation=quote_citation,
                                                             string=pq.group(), partial_quote="False")
                                    new_contents = [new_text[:contents_start], quote_tag, new_text[pq.end() + 1:]]

                                text_element.extend(new_contents)

                        else:
                            #don't do anything with this because they're basically all scriptures,
                            #except for some video narration that I'm ignoring
                            pass
                    else:
                        #Quotes without citations, but there's only one of it in the paragraph
                        if len(pq_count) < 2:
                            speaker = ''
                            citation = ''
                            if re.search("A man would get nearer to God",pq.group()):
                                speaker = 'Joseph Smith'
                                citation = ''
                            elif re.search("appeared within viewing distance", pq.group()):
                                speaker = 'Frederick G. Williams'
                                citation = 'The Revelations of the Prophet Joseph Smith, comp. Lyndon W. Cook [1981], 198.'
                            elif re.search("A power went through me at that moment", pq.group()):
                                speaker = 'A missionary'
                                citation = ''
                            elif re.search("the sound of the voice of the", pq.group()):
                                speaker = 'Spencer W. Kimball'
                                citation = 'Conference Report, Apr. 1977, 115; or Ensign, May 1977, 78'
                            elif re.search("I always want to be with my own family",pq.group()):
                                speaker = 'Children\'s Songbook'
                                citation = 'Families Can Be Together Forever'
                            elif re.search("happiness in family life is most likely to be achieved",pq.group()) \
                                    or re.search("successful marriages and families are established",pq.group()):
                                speaker = 'The First Presidency'
                                citation = 'The Family: A Proclamation to the World'
                            elif re.search("When an enemy had told a scandalous story", pq.group()):
                                speaker = 'Joseph Smith'
                                citation = 'Jesse W. Crosby, quoted in Hyrum L. Andrus and Helen Mae Andrus, comps., They Knew the Prophet [1974], 144.'
                            elif re.search("Perhaps Jesus felt not only a sense",pq.group()) \
                                    or re.search("He took His three apostles with Him",pq.group()) \
                                    or re.search("The three chosen apostles were taught",pq.group()):
                                speaker = 'David B. Haight'
                                citation = 'Conference Report, Apr. 1977, 9–10; or Ensign, May 1977, 7–9'
                            elif re.search("grow varieties of corn and beans that", pq.group()):
                                speaker = 'Joseph B. Wirthlin'
                                citation = 'Conference Report, Apr. 1989, 7; or Ensign, May 1989, 7'
                            elif re.search("a correct idea of",pq.group()):
                                speaker = 'Joseph Smith'
                                citation = 'Lectures on Faith [1985], 38'
                            else:

                                pass

                            #I mean, if I can clean this up, I can make it a function
                            if not (speaker == '' and citation == ''):
                                try:
                                    text_element.clear()
                                except AttributeError:
                                    print(text_element)
                                contents_start = pq.start() - 1
                                if contents_start < 0:
                                    contents_start = 0
                                quote_tag = soup.new_tag('quotation', speaker=speaker, citation=citation,
                                                         string=pq.group(), partial_quote="False")
                                new_contents = [new_text[:contents_start], quote_tag, new_text[pq.end() + 1:]]
                                text_element.extend(new_contents)
                        #Quotes without citations that are part of a bigger paragraph
                        else:
                            needs_citation.append(pq)
                            '''





def main():
    to_modify_dir = "C:\\Users\elena\PycharmProjects\MA_Thesis\Full_Manuals\Sections_XML"
    modified_dir = "C:\\Users\elena\PycharmProjects\MA_Thesis\Full_Manuals\Quotations_XML"

    for manual in os.listdir(to_modify_dir):
       # print('\n',manual)
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