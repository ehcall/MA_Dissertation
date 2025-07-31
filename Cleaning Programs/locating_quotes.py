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
    if re.search('What I have received', to_check):
        #hardcoded because it's the exception to the rounding rule
        return True
    if quote_len < 5:
        return False
    elif round(uppers/quote_len, 2) > 0.4 and quote_len < 15:
        #print(to_check)
        return False
    elif re.search('To the Presidents and Members',to_check):
        return False
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
                      'commented','published', 'quoted','made','offered','observed','recorded','replied']
    for match in matches:
        match_id, (start, end) = match
        if str(speaker_doc[end]) in speaking_verbs:
            return str(speaker_doc[start])
        elif str(speaker_doc[start]) == 'Emma' and str(speaker_doc[end]) == 'support':
            return 'Lucy Mack Smith'
    if re.search('Richard G. Scott', text_line):
        return 'Richard G. Scott'
    if re.search('Henry B. Eyring', text_line):
        return 'Henry B. Eyring'
    if re.search('Thomas S. Monson', text_line):
        return 'Thomas S. Monson'
    if re.search('First Presidency', text_line):
        return 'First Presidency'
    if re.search('Vaughn J. Featherstone', text_line):
        return 'Vaughn J. Featherstone'
    if re.search('Ezra Taft Benson', text_line):
        return 'Ezra Taft Benson'
    if re.search('Russell M. Nelson', text_line):
        return 'Russell M. Nelson'
    if re.search('Jeffrey R. Holland', text_line):
        return 'Jeffrey R. Holland'
    if re.search('Gordon B. Hinckley', text_line):
        return 'Gordon B. Hinckley'

    if re.search('James E. Talmage', text_line):
        return 'James E. Talmage'
    if re.search('Robert D. Hales', text_line):
        return 'Robert D. Hales'
    if re.search('M. Russell Ballard', text_line):
        return 'M. Russell Ballard'
    if re.search('LeGrand Richards', text_line):
        return 'LeGrand Richards'
    line_string = "CHECK THIS LINE: " + text_line
    return (line_string)

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
    cited_people = set()
    other_people = set()
    new_people = set()
    if len(people) < 1:
        #hardcoding some stuff in
        if re.search('Vincenzo di Francesca',full_text):
            cited_people.add('Vincenzo di Francesca')
            other_people.add('Vincenzo di Francesca')
        elif re.search('Hosanna Shout', full_text):
            cited_people.add('Encyclopedia of Mormonism')
            other_people.add('Encyclopedia of Mormonism')
        elif re.search('The proclamation', full_text):
            cited_people.add('The Family: A Proclamation to the World')
            other_people.add('The Family: A Proclamation to the World')
        elif re.search('The Prophet', full_text):
            cited_people.add('Joseph Smith')
            other_people.add('Joseph Smith')
        elif re.search('I always want to be', full_text):
            cited_people.add('Children\'s Songbook')
            other_people.add('Children\'s Songbook')
        elif re.search('Neither the law of Moses', full_text):
            cited_people.add('The Life and Teachings of Jesus and His Apostles')
            other_people.add('The Life and Teachings of Jesus and His Apostles')
        elif re.search('Life isn\'t always easy', full_text):
            cited_people.add('M. Russell Ballard')
            other_people.add('M. Russell Ballard')
        elif re.search('Paramore',full_text):
            cited_people.add('James M. Paramore')
            other_people.add('James M. Paramore')
        elif re.search('Word of Wisdom',full_text):
            cited_people.add('A missionary')
            other_people.add('A missionary')
        elif re.match('[a-z]',full_text):
            cited_people.add('Neal A. Maxwell')
            other_people.add('Neal A. Maxwell')
        else:
            print("Couldn't find a speaker for this line: ",full_text)

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
        if 'James R. Clark' in cited_people:
            new_people.add('First Presidency')
            return new_people
        return cited_people
    elif len(cited_people) > 1 and len(other_people) == 0:
        if 'Joseph Smith\'s' in cited_people:
            new_people.add('Gospel Topics')
            return new_people
        else:
            return cited_people
    elif len(other_people) > 0 and len(cited_people) == 0:
        if re.search('Church History in the Fulness of Times', full_text):
            new_people.add('Church History in the Fulness of Times')
            return new_people
        else:
            new_people.add(speaker_from_verb(edited_text_quote))

        return new_people
    elif len(cited_people) > 0 and len(other_people) > 0:
        combined_set = cited_people & other_people
        if 'Joseph Fielding Smith' in cited_people:
            other_people.discard('Joseph Fielding Smith')
            other_people.discard('Zacharias')
            other_people.discard('Elisabeth')
            return other_people
        elif 'James R. Clark' in cited_people:
            other_people.discard('James R. Clark')
            if 'Joseph F. Smith' in cited_people:
                other_people.add('First Presidency')
            return other_people
        elif 'Edward L. Kimball' in cited_people:
            combined_set.discard('Edward L. Kimball')
            return combined_set
        elif 'Bruce R. McConkie' in cited_people:
            other_people.discard('Bruce R. McConkie')
            return other_people
        elif 'G. Homer Durham' in cited_people:
            other_people.discard('G. Homer Durham')
            return other_people
        elif 'Stanley B. Kimball' in cited_people:
            combined_set.discard('Stanley B. Kimball')
            return combined_set
        elif 'Albert L. Zobell Jr.' in cited_people:
            other_people.discard('Albert L. Zobell Jr.')
            return other_people
        elif 'History of the Church' in cited_people:
            other_people.discard('History of the Church')
            if len(other_people) == 1:
                return other_people
            else:
                new_people.add('History of the Church')
                return new_people
        elif 'John A. Widtsoe' in cited_people:
            combined_set.discard('John A. Widtsoe')
            return combined_set
        elif 'Julie B. Beck' in other_people:
            new_people.add('Julie B. Beck')
            return new_people
        else:
            if 'Brigham Young' in cited_people and re.search('University',full_text):
                other_people.discard('Brigham Young')
                return other_people
            elif len(other_people) == 1:
                if 'First Presidency' in other_people:
                    return other_people
                elif 'Gospel Topics' in other_people:
                    return cited_people
                elif 'George Frideric Handel' in other_people:
                    return cited_people
                else:
                    return other_people
            elif len(cited_people) == 1:
                if 'Richard G. Scott' in other_people:
                    other_people.discard('Richard G. Scott')
                    return other_people
                elif 'Belle S. Spafford' in cited_people or \
                        'Boyd K. Packer' in cited_people or \
                        'Don L. Searle' in cited_people or \
                        'E. Cecil McGavin' in cited_people or \
                        'Robert J. Matthews' in cited_people or \
                        'Wilford Woodruff' in cited_people or \
                        'Brigham Young' in cited_people:
                    return cited_people
                elif 'Joseph Smith' in cited_people:
                    new_people.add('First Presidency')
                    return new_people
                elif 'Lucy Mack Smith' in other_people:
                    new_people.add('Lucy Mack Smith')
                    return new_people
                elif 'Martin Harris' in cited_people:
                    new_people.add('Revelations in Context')
                    return new_people
                elif 'Wilford Woodruff' in other_people:
                    #this one is weird because it's Joseph Smith from Woodruff's words...
                    new_people.add('Joseph Smith')
                    return new_people
                else:
                    return other_people.difference(cited_people)

                #print(cited_people, other_people)
                #print("\t\t",edited_text_quote)
            else:
                if other_people == cited_people:
                    if 'Gordon B. Hinckley' in cited_people:
                        new_people.add('Marjorie P. Hinckley')
                        return new_people
                    else:
                        speaker_check = speaker_from_verb(edited_text_citation)
                        if re.match('CHECK',speaker_check):
                            return cited_people
                        else:
                            new_people.add(speaker_check)
                            return new_people
                else:
                    if 'Frederick G. Williams' in other_people:
                        new_people.add('Frederick G. Williams')
                        return new_people
                    elif 'Joseph Smith Sr.' in other_people:
                        new_people.add('Joseph Smith Sr.')
                        return new_people
                    elif 'Joseph Smith' in other_people:
                        new_people.add('Joseph Smith')
                        return new_people
                    elif 'Frederick William Hurst' in other_people:
                        new_people.add('Frederick William Hurst')
                        return new_people
    return new_people

def clean_speakers(dirty_speakers, text_line):
    cleaned_speakers = set()
    if dirty_speakers == None:
        return cleaned_speakers
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
            new_text = re.sub(r'(^\"[^\"]*?)\r?\n\"', r'\1 ¶ ', current_text)
            new_text = re.sub(r'([^\"]\r?\n)(\"[^\"]*?)\r?\n\"', r'\1\2 ¶ ', new_text)
            # if a line starts with a quotation, but does not end in a quotation,
                # you should combine it with the quotation below
            while re.search(r'[^\"]\r?\n\"[^\"]*?\r?\n\"', new_text):
                new_text = re.sub(r'([^\"]\r?\n\"[^\"]*?)\r?\n\"', r'\1 ¶ ', new_text)

            text_element.string = new_text
            possible_quotes = re.finditer('\".*?\"',text_element.string)
            pq_count = re.findall('\".*?\"',text_element.string)
            quote_count = 0
            all_quotes = []

            for pq in possible_quotes:
                if check_quote(pq.group()):
                    quote_count += 1
                    non_quotation_text = new_text[:pq.start()] + new_text[pq.end():]
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
                            if re.search('I always want to be',pq.group()):
                                plausible_citations.append('Children\'s Songbook')
                            elif re.search('A man would get nearer',pq.group()):
                                plausible_citations.append('Joseph Smith')
                            elif re.search('Without the Atonement',pq.group()):
                                plausible_citations.append('Russell M. Nelson')
                            elif re.search('A power went',pq.group()):
                                plausible_citations.append('A missionary')
                            elif re.search('grow varieties',pq.group()):
                                plausible_citations.append('(in Conference Report, Apr. 1989, 7; or Ensign, May 1989, 7)')
                            elif re.search('happiness in family life',pq.group()):
                                plausible_citations.append('The Family: A Proclamation to the World')

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
                                    if re.search('Hymns',option.group()):
                                        if re.search("Again We Meet", option.group()):
                                            plausible_citations.append(option.group())
                                        else:
                                            pass
                                    elif check_citation(option.group()):
                                        plausible_citations.append(option.group())
                            else:
                                if re.match('\(36\)', option.group()):
                                    plausible_citations.append('Our Heritage, 36')
                                else:
                                    has_been_scrip = True

                    if len(plausible_citations) < 1 and has_been_scrip:
                         if re.search('Elder Haight', non_quotation_text):
                            plausible_citations.append('Elder Haight')
                        #it's probably a scripture otherwise though
                    elif len(plausible_citations) < 1 and not has_been_scrip:
                        if re.search('[Pp]roclamation',non_quotation_text):
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
                reversed_quotes = all_quotes[::-1]
                if len(all_quotes) > 1:
                    partial = True
                else:
                    partial = False
                for q in reversed_quotes:
                    q_quote = q[0]
                    q_citation = q[1]
                    q_speaker = q[2]
                    contents_start = q_quote.start() - 1
                    modify_text = text_element.contents[0]
                    long_comments = []

                    if len(text_element.contents) > 1:
                        long_comments.extend(text_element.contents[1:])

                    if contents_start < 0:
                        contents_start = 0

                    try:
                        text_element.clear()
                    except AttributeError:
                        print(text_element)

                    quote_tag = soup.new_tag('quotation', speaker=q_speaker, citation=q_citation,
                                             string=q_quote.group(), partial_quote=partial)
                    new_contents = [modify_text[:contents_start], quote_tag, modify_text[q_quote.end() + 1:]]
                    if len(long_comments) > 1:
                        new_contents.extend(long_comments)

                    text_element.extend(new_contents)

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
        #hold = input("wait a sec")
        with open(modified_manual, 'w', encoding='utf-8') as modifying_manual:
            modifying_manual.write(soup.prettify())

#main()