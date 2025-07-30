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
    if round(uppers/quote_len, 2) > 0.4 or quote_len < 5:
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
                re.search('The doctrines of the gospel', to_check) or \
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
    speaking_verbs = ['told','said','recalled','explained','issued','announced', 'taught','shared','wrote','declared',
                      'commented','published', 'quoted','made','offered',]
    for match in matches:
        match_id, (start, end) = match
        if str(speaker_doc[end]) in speaking_verbs:
            return str(speaker_doc[start])
        elif str(speaker_doc[start]) == 'Emma' and str(speaker_doc[end]) == 'support':
            return 'Lucy Mack Smith'
    if re.match('A hymn such as',text_line):
        return('Henry B. Eyring')
    elif re.match('President M. Russell Ballard\'s message',text_line):
        return('M. Russell Ballard')
    elif re.match('Consider introducing the topic of marriage',text_line):
        return('Robert D. Hales')
    elif re.match('Read Joseph Smith—History',text_line) or \
        re.match('Display the picture of the Martin', text_line):
        return('Gordon B. Hinckley')
    elif re.match('You may want to review Oliver Cowdery',text_line):
        return('James E. Talmage')
    elif re.match(' ?Speaking about Joseph Smith',text_line):
        return('LeGrand Richards')
    elif re.match('When Jeffrey R. Holland was president',text_line):
        return('Jeffrey R. Holland')
    elif re.match('Display the picture of President Wilford Woodruff',text_line) or \
            re.match('Speaking at Christmastime', text_line):
        return('Russell M. Nelson')
    elif re.match('In "The Family: A Proclamation to the World,"',text_line) or \
            re.match('The First Presidency',text_line) or \
            re.match('Explain that the Prophet Joseph Smith', text_line):
        return('First Presidency')
    elif re.match('Share the following story told',text_line):
        return('Vaughn J. Featherstone')
    elif re.match('Some people incorrectly believe',text_line):
        return('Richard G. Scott')
    elif re.match('Explain that in 1952',text_line):
        return('Ezra Taft Benson')
    elif re.match('Share the following story told by Elder Thomas S. Monson',text_line):
        return('Thomas S. Monson')
    elif re.match('In February 1828, Martin Harris',text_line):
        return('Revelations in Context')
    elif re.match('Soon after Sister Belle S. Spafford',text_line):
        return('Belle S. Spafford')
    elif re.match('In July 1839, a large number',text_line):
        return('Wilford Woodruff')
    elif re.match('Explain that Joseph Smith\'s father',text_line):
        return('E. Cecil McGavin')
    elif re.match('The process of translating the Bible',text_line):
        return('Robert J. Matthews')
    elif re.match('Levi Hancock was baptized in November 1830',text_line):
        return('Don L. Searle')
    elif re.match('Explain that before Joseph Smith Sr.',text_line):
        return('Joseph Smith Sr.')
    elif re.match('Frederick William Hurst was working',text_line):
        return('Frederick William Hurst')
    elif re.match('3. Suggestion for teaching',text_line):
        return('Boyd K. Packer')
    elif re.match('Some of the workers suggested they build the temple',text_line):
        return('Joseph Smith')
    else:
        line_string = "CHECK THIS LINE: " + text_line
        return(line_string)
       # return ''

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
                             'Grandmother','Hannah','Samuel','Alvin','Isaac','Peter 5:5','Stakes','Strong Modeling',
                             'Gentiles','Gentile','Keepers']
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


def clean_citation(quote_citation):
    cleaned_citation = re.sub('[\(\)]','',quote_citation)
    cleaned_citation = re.sub('^in ','',cleaned_citation)
    cleaned_citation = re.sub('^[Ss]ee ','',cleaned_citation)
    split_citation = cleaned_citation.split('; ')
    citation_options = []
    if len(split_citation) > 1:

        #print(split_citation)
        if re.match('\"That Ye May Be',split_citation[0]) or \
                re.match('\"Minutes and Blessings',split_citation[0]) or \
                re.match('Journal, December',split_citation[0]):
            citation_options.append(cleaned_citation)
        else:
            for sc in split_citation:
                if not re.match('[sS]ee',sc) and not \
                    re.match('italics',sc) and not \
                    re.match('spelling',sc) and not \
                    re.search('^quoted',sc) and not \
                    re.search('Conference Report',sc):
                    #print(re.sub('^or ','',sc))
                    citation_options.append(re.sub('^or ','',sc))
    else:
        citation_options.append(split_citation[0])


    cleaned_citation = re.sub('^quoted in','',citation_options[0])
    cleaned_citation = re.sub('^told by','',cleaned_citation)
    cleaned_citation = re.sub('^quoted by','',cleaned_citation)
    #print(cleaned_citation)
    return cleaned_citation


def locate_speakers(full_text, quote_data, citation):
    people = find_entity(full_text)
    edited_text_quote = full_text[:quote_data.start()] + "{QUOTATION}" + full_text[quote_data.end():]
    edited_text_citation = re.sub(citation,'{CITATION}',edited_text_quote)
    #print(edited_text)
   # print(quote_data.group())
    cited_people = set()
    other_people = set()
    new_people = set()
    if len(people) < 1:
        #hardcoding some stuff in
        if re.search('Vincenzo di Francesca',full_text):
            cited_people.add('Vincenzo di Francesca')
            other_people.add('Vincenzo di Francesca')
        elif re.search('The Prophet', full_text):
            cited_people.add('Joseph Smith')
            other_people.add('Joseph Smith')
        elif re.search('Hosanna Shout', full_text):
            cited_people.add('Encyclopedia of Mormonism')
            other_people.add('Encyclopedia of Mormonism')
        elif re.search('The proclamation', full_text):
            cited_people.add('The Family: A Proclamation to the World')
            other_people.add('The Family: A Proclamation to the World')
        elif re.search('Conference Report', full_text):
            cited_people.add('Neal A. Maxwell')
            other_people.add('Neal A. Maxwell')
        elif re.search('Life isn\'t always easy', full_text):
            cited_people.add('M. Russell Ballard')
            other_people.add('M. Russell Ballard')
        elif re.search('Hosanna Shout', full_text):
            cited_people.add('')
            other_people.add('')
        elif re.search('I always want to be', full_text):
            cited_people.add('Children\'s Songbook')
            other_people.add('Children\'s Songbook')
        elif re.search('Neither the law of Moses', full_text):
            cited_people.add('The Life and Teachings of Jesus and His Apostles')
            other_people.add('The Life and Teachings of Jesus and His Apostles')
        else:
            cited_people.add('A missionary')
            other_people.add('A missionary')
    for person in people:
        #ignore people in the quoted text
        if re.search(person, citation):
            cited_people.add(person)
        if re.search(person, edited_text_citation):
            other_people.add(person)
    if len(cited_people) == 0 and len(other_people) == 1:
        return other_people
    elif len(cited_people) == 1 and len(other_people) == 0:
        return cited_people
    elif len(cited_people) == 1 and cited_people == other_people:
        return cited_people
    elif len(cited_people) > 1 and len(other_people) == 0:
        if 'Joseph Smith\'s' in cited_people:
            new_people.add('Gospel Topics')
            return new_people
        else:
            return cited_people
    elif len(other_people) > 0 and len(cited_people) == 0:
        potential_speakers = set()
        potential_speakers.add(speaker_from_verb(edited_text_quote))
        return potential_speakers
    elif len(cited_people) > 0 and len(other_people) > 0:
        combined_set = cited_people & other_people

        if 'Joseph Fielding Smith' in cited_people:
            other_people.discard('Joseph Fielding Smith')
            return other_people
        elif 'Edward L. Kimball' in cited_people:
            combined_set.discard('Edward L. Kimball')
            return combined_set
        elif 'Bruce R. McConkie' in cited_people:
            other_people.discard('Bruce R. McConkie')
            return other_people
        elif 'John A. Widtsoe' in cited_people:
            combined_set.discard('John A. Widtsoe')
            return combined_set
        elif 'G. Homer Durham' in cited_people:
            other_people.discard('G. Homer Durham')
            return other_people
        elif 'Stanley B. Kimball' in cited_people:
            combined_set.discard('Stanley B. Kimball')
            return combined_set
        elif 'History of the Church' in cited_people:
            #print(cited_people, other_people)
            other_people.discard('History of the Church')
            if len(other_people) == 1:
                return other_people
            else:
                new_people.add('History of the Church')
                return new_people
        else:
            if len(other_people) == 1:
                if 'Gospel Topics' in other_people:
                    return cited_people
                elif 'Joseph F. Smith' in other_people:
                    return cited_people
                elif 'The Family: A Proclamation to the World' in cited_people:
                    return cited_people
                else:
                    return other_people
            else:
                speaker_check = speaker_from_verb(edited_text_citation)
                if re.match('CHECK',speaker_check):
                    for cited_person in cited_people:
                        other_people.discard(cited_person)
                    return other_people
                else:
                    new_people.add(speaker_check)
                    return new_people
    else:
        print(other_people, cited_people)
        print('\t',full_text)

def clean_speakers(dirty_speakers, text_line):
    cleaned_speakers = set()
    for speaker in dirty_speakers:
        new_speaker = re.sub('Elder ','',speaker)
        new_speaker = re.sub('Bishop ','',new_speaker)
        new_speaker = re.sub('Smith\'s','Smith',new_speaker)
        if new_speaker == 'Monson':
            new_speaker = 'Thomas S. Monson'
        if new_speaker == 'Ballard':
            new_speaker = 'M. Russell Ballard'
        if new_speaker == 'Benson':
            new_speaker = 'Ezra Taft Benson'
        if new_speaker == 'Bradford':
            new_speaker = 'William R. Bradford'
        if new_speaker == 'David A. Bednar\'s':
            new_speaker = 'David A. Bednar'
        if new_speaker == 'Elisabeth':
            new_speaker = 'Joseph Smith'
        if new_speaker == 'Joseph Fielding Smith Jr.':
            new_speaker = 'Joseph Fielding Smith'
        if new_speaker == 'Chi Hong':
            new_speaker = 'Chi Hong (Sam) Wong'
        if new_speaker == 'Eyring':
            new_speaker = 'Henry B. Eyring'
        if new_speaker == 'Faust':
            new_speaker = 'James E. Faust'
        if new_speaker == 'Haight':
            new_speaker = 'David B. Haight'
        if new_speaker == 'Hinckley':
            new_speaker = 'Gordon B. Hinckley'
        if new_speaker == 'Holland':
            new_speaker = 'Jeffrey R. Holland'
        if new_speaker == 'Hyde':
            new_speaker = 'Orson Hyde'
        if new_speaker == 'Maxwell':
            new_speaker = 'Neal A. Maxwell'
        if new_speaker == 'McConkie':
            new_speaker = 'Bruce R. McConkie'
        if re.match('Prophet',new_speaker):
            new_speaker = 'Joseph Smith'
        if new_speaker == 'Smith':
            new_speaker = 'Joseph F. Smith'
        if new_speaker == 'Wirthlin':
            new_speaker = 'Joseph B. Wirthlin'
        if new_speaker == 'Woodruff':
            new_speaker = 'Wilford Woodruff'
        if new_speaker == 'Zacharias':
            new_speaker = 'Joseph Smith'
        if new_speaker == 'Young':
            new_speaker = 'Brigham Young'
        cleaned_speakers.add(new_speaker)
    return cleaned_speakers
def modify_quote(soup):

    text_elements = soup.find_all(['p','li'])
    for text_element in text_elements:
        current_text = text_element.string
        if current_text:
            text_element.clear()
            new_text = re.sub(r'([^\)][^:])\r?\n\"', r'\1 ¶ ', current_text)
            text_element.string = new_text
            possible_quotes = re.finditer('\".*?\"',text_element.string)
            pq_count = re.findall('\".*?\"',text_element.string)
            quote_count = 0
            all_quotes = []
            for pq in possible_quotes:
                if check_quote(pq.group()):
                    quote_count += 1
                    non_quotation_text = new_text[:pq.start()] + new_text[pq.end():]
                    #possible_citation = re.match("\?? \(.*?\)", new_text[pq.end():])
                    possible_citations = re.finditer("\(.*?\)", non_quotation_text)
                    pc_count = re.findall("\(.*?\)", non_quotation_text)
                    plausible_citations = []
                    quote_citation = ''
                    if len(pc_count) < 1:
                        #no possible citation could be found in the paragraph
                        if re.search('\?\"$', pq.group()) or \
                                (re.match(' ?[a-z]\. ?',non_quotation_text)
                                 and not re.search('Elder Haight',non_quotation_text)) or \
                                len(non_quotation_text) < 2 or len(pq.group()) < 79:
                            #it's not relevant. don't worry about it
                            pass
                        else:
                            #hardcoding relevant passages
                            if re.search('I always want to be',pq.group()) or \
                                re.search('A man would get nearer',pq.group())or \
                                re.search('Without the Atonement',pq.group()) or \
                                re.search('A power went',pq.group()) or \
                                re.search('grow varieties',pq.group()) or \
                                re.search('happiness in family life',pq.group()):
                                #TODO: something with these phrases
                                plausible_citations.append('IDK it has one')
                                #print(pq.group())
                          #  else:
                                #pass
                    else:
                        has_been_scrip = False
                        for option in possible_citations:
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
                                if re.match('\(36\)', option.group()):
                                    plausible_citations.append('Our Heritage, 36')
                                else:
                                    has_been_scrip = True

                    if len(plausible_citations) < 1 and has_been_scrip:
                         if re.search('Elder Haight', non_quotation_text):
                          #      #TODO: deal with Haight
                                plausible_citations.append('Elder Haight')
                               # pass
                            #it's probably a scripture otherwise though
                    elif len(plausible_citations) < 1 and not has_been_scrip:
                        if re.search('[Pp]roclamation',non_quotation_text):
                         #       #TODO: deal with proclamation
                            plausible_citations.append('Fam Proc')

                    if len(plausible_citations) > 1:
                        if re.search('the heart \[and\] the spirit',pq.group()):
                            pass
                        elif re.search('One able',pq.group()):
                            quote_citation = plausible_citations[1]
                        else:
                            quote_citation = plausible_citations[quote_count-1]
                    elif len(plausible_citations) == 1:
                        if len(pq.group()) < 100:
                            if re.match(' ?\?',new_text[pq.end():]) or \
                                re.match(' ?\(D\&', new_text[pq.end():]) or \
                                re.match(' ?\(Doctrine and Covenants', new_text[pq.end():]) or \
                                re.match(' ?\:', new_text[pq.end():]) or \
                                re.match(' ?[crwo]', new_text[pq.end():]) or \
                                re.match(' ?A', new_text[pq.end():]) or \
                                re.search('the place of my', pq.group()) or \
                                re.match(' ?\([3M]', new_text[pq.end():]):
                                    #we don't want this
                                pass
                            else:
                                quote_citation = plausible_citations[0]
                        else:
                            quote_citation = plausible_citations[0]

                    if quote_citation != '':
                        cleaned_citation = clean_citation(quote_citation)
                        quote_speakers = locate_speakers(new_text, pq, cleaned_citation)

                        speaker = ', '.join(str(x) for x in clean_speakers(quote_speakers, new_text))
                        all_quotes.append([pq, cleaned_citation, speaker])

            if len(all_quotes) > 0:
                print("New Element")
            for a_quote in all_quotes:
                print("\t",a_quote)

                '''
                      print(speaker)
                        contents_start = pq.start() - 1
                        if contents_start < 0:
                            contents_start = 0
                        try:
                            text_element.clear()
                        except AttributeError:
                            print(text_element)
                        quote_tag = soup.new_tag('quotation', speaker=speaker, citation=quote_citation,
                                                 string=pq.group(), partial_quote="False")
                        new_contents = [new_text[:contents_start], quote_tag, new_text[pq.end() + 1:]]
                        text_element.extend(new_contents)
                    else:
                        print(pq.group())
                       # print(cleaned_citation)
                       '''

    return

'''
                   
                        if quote_citation != '':
                            #adds the quotation tag
                            
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

#main()