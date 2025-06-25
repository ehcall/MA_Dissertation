import os
import re
import xml.etree.ElementTree as ET
import scripture_references


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
def modify_quote(old_quote):
    new_quote = old_quote
    old_quote = re.sub(r'([^:])\n\"',r'\1 <qb /> ',old_quote)

    possible_quotes = re.finditer('\"[\s\S]*?\"',old_quote)
    prev_citation = ""
    prev_quote = ""
    quote_citation = ""
    for pq in possible_quotes:
       # print(pq.group())
        if check_quote(pq.group()):
            possible_citation = re.match(" \(.*?\)",old_quote[pq.end():])
            if possible_citation:
                quote_citation = ''
                grouped_citation = possible_citation.group().split("; ")
               # print(len(grouped_citation))
                scripture_ref = False
                if len(grouped_citation) == 1:
                    #print(len(grouped_citation[0].split(' ')))
                    if len(grouped_citation[0].split(' ')) < 8:
                        scripture_ref = scripture_references.check_if_scripture(grouped_citation[0])
                    if not scripture_ref:

                        if not re.search('[0-9]',possible_citation.group()):
                            if re.search('Hymns',possible_citation.group()) \
                                or re.search('Gospel Topics',possible_citation.group()) \
                                or re.search('No Greater Call',possible_citation.group()) \
                                or re.search('Explanatory Introduction',possible_citation.group()) \
                                or re.search('National Press Club', possible_citation.group()):
                                quote_citation = possible_citation.group()
                        else:
                            quote_citation = possible_citation.group()
                else:
                    if re.search('Conference Report',possible_citation.group()) or re.search('Ensign',possible_citation.group()):
                        quote_citation = possible_citation.group()
                    #if it has more than four semicolons, it's typically just scriptures
                    elif len(grouped_citation) < 3:
                        citation_1 = grouped_citation[0]
                        citation_1_ref = scripture_references.check_if_scripture(citation_1)
                        citation_2 = grouped_citation[1]
                        citation_2_ref = scripture_references.check_if_scripture(citation_2)
                        if citation_1_ref and citation_2_ref:
                            #both scriptures
                            pass
                          #  print(possible_citation.group())
                        if not citation_1_ref and not citation_2_ref:
                            quote_citation = possible_citation.group()

                        elif citation_1_ref or citation_2_ref:
                            if not citation_1_ref and re.search('[0-9]',citation_1):
                                quote_citation = possible_citation.group()
                            elif not citation_2_ref and re.search('Teaching',citation_2):
                                quote_citation = possible_citation.group()



                    '''
                    if not scripture_ref:
                       # citation_item = re.sub('^in ','',citation_item)
                       # citation_item = re.sub('^or ','',citation_item)
                        if possible_citation.group() == prev_citation:
                            pass
                        else:
                            if not re.search('[0-9]',possible_citation.group()):
                                if re.search('Gospel Topics',possible_citation.group()) \
                                    or re.search('No Greater Call',possible_citation.group()) \
                                    or re.search('National Press Club Forum',possible_citation.group()) \
                                    or re.search('Explanatory Introduction',possible_citation.group()):
                                    # almost certainly a citation
                                    
                                    print(pq.group(),"\n",quote_citation)
                                    #TODO: Something

                            else:
                                #almost certainly a citation
                                #TODO: something
                                quote_citation = possible_citation.group()
                                print(pq.group(), "\n", quote_citation)
                        prev_citation = possible_citation.group()
'''
                if quote_citation != '':
                    quote_citation = re.sub("^ ",'',quote_citation)
                    new_quote = old_quote[:pq.start()] + "<quotation citation=\"" + quote_citation + "\">" + pq.group() + "</quotation>" + old_quote[
                                                                                                        pq.end():]
                    return new_quote

           # print(f"Match: {pq.group()}, Start: {pq.start()}, End: {pq.end()}")
            #print("this is actually a quote; might be a scripture quote though")
           # possible_citation = re.search('(\(.*?\))',test_quote[pq.end():])
           # if possible_citation:
                #TODO: deal with embedded quotations
                #print()

            #    pc_clean_paren = re.sub('[\(\)]','',possible_citation.group())
             #   pc_clean = re.sub('[Ss]ee ','',pc_clean_paren)
            #    pc_clean = re.sub('also ','',pc_clean)
             #   more_pcs = pc_clean.split('; ')
             #   for more_pc in more_pcs:
             #       if len(more_pc.split(' ')) < 7:
             #           scripture_ref = scripture_references.check_if_scripture(more_pc)
             #       if not scripture_ref:
              #          new_quote = test_quote[:pq.start()] + "<quotation>" + pq.group() + "</quotation>" + test_quote[pq.end():]
              #          return new_quote
         #   else:
          #      return old_quote

        else:
            return old_quote

    return old_quote

def main():
    to_modify_dir = "C:\\Users\elena\PycharmProjects\MA_Thesis\Full_Manuals\Sections_XML"
    modified_dir = "C:\\Users\elena\PycharmProjects\MA_Thesis\Full_Manuals\Quotations_XML"

    for manual in os.listdir(to_modify_dir):
      #  hold_up = input("wait a sec")
        to_modify_manual = to_modify_dir + "\\" + manual
        modified_manual = modified_dir + "\\" + manual
        #if re.match("CFM", manual):
        #print(manual)
        tree = ET.parse(to_modify_manual)
        root = tree.getroot()
        potential_quotes = []
        for element in root.iter():
            #print(element.tag)
            if element.tag == 'p' or element.tag == 'li':
                if re.search('\"', element.text):
                    element.text = modify_quote(element.text)

        tree.write(modified_manual)
       # elif re.match("GD", manual):

main()