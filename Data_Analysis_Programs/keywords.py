import os
import csv
import re

# SET CORPUS VARIABLES
keyword_data = {
    'all_text_corpus':{
        'overall_text':{
            'size': 610453,
            'unit_type':{
                'class': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                'hw': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                'pos': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                'sem': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                'word': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
            }
        },
        'cfm_text':{
                'size': 200798,
                'unit_type':{
                    'class': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                    'hw': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                    'pos': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                    'sem': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                    'word': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                }
            },
        'gd_text':{
                'size': 409655,
                'unit_type': {
                    'class': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                    'hw': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                    'pos': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                    'sem': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                    'word': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                }
            },
    },
    'quotations_corpus':{
        'all_gendered_quotes':{
            'all_gendered_quotes_overall':{
                'size': 94444,
                'unit_type': {
                    'class': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                    'hw': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                    'pos': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                    'sem': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                    'word': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                }
            },
            'cfm_gendered_quotes':{
                'size': 30212,
                'unit_type': {
                    'class': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                    'hw': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                    'pos': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                    'sem': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                    'word': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                }
            },
            'gd_gendered_quotes':{
                'size': 64232,
                'unit_type': {
                    'class': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                    'hw': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                    'pos': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                    'sem': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                    'word': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                }
            }
        },
        'female_quotes':{
            'all_female_quotes':{
                'size': 4234,
                'unit_type': {
                    'class': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                    'hw': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                    'pos': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                    'sem': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                    'word': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                }
            },
            'cfm_female_quotes':{
                'size': 2840,
                'unit_type': {
                    'class': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                    'hw': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                    'pos': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                    'sem': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                    'word': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                }
            },
            'gd_female_quotes':{
                'size': 1394,
                'unit_type': {
                    'class': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                    'hw': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                    'pos': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                    'sem': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                    'word': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                }
            },
        },
        'male_quotes':{
            'all_male_quotes':{
                'size': 90210,
                'unit_type': {
                    'class': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                    'hw': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                    'pos': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                    'sem': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                    'word': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                }
            },
            'cfm_male_quotes':{
                'size': 27372,
                'unit_type': {
                    'class': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                    'hw': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                    'pos': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                    'sem': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                    'word': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                }
            },
            'gd_male_quotes':{
                'size': 62838,
                'unit_type': {
                    'class': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                    'hw': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                    'pos': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                    'sem': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                    'word': {
                        'ngrams': {
                            '1': [],
                            '2': [],
                            '3': []
                        },
                    },
                }
            },
        },
    }
}

stopwords = ['1','2','3','4','5','6','7','8','9','10','\'d','\'s','\'re','n\'t','\'m','\'ll','\'ve','\'ca',
             'what','which','who','whom','this','that','these','those','am','is','are','was','were','be','been','being',
             'have','has','had','having','do','does','did','doing','a','an','the','and','but','if','or','because','as',
             'until','while','of','at','by','for','with','about','against','between','into','through','during','before',
             'after','above','below','to','from','up','down','in','out','on','off','over','under','again','further',
             'then','once','here','there','when','where','why','how','all','any','both','each','few','more','most',
             'other','some','such','no','nor','not','only','own','same','so','than','too','very','s','t','can','will',
             'just','don','should','now','a.','b.','c.','d.','e.','f.','g.','h.','i.','j.']
pronouns = ['i','me', 'my','myself','we','our','ours','ourselves','you','your','yours','yourself','yourselves',
            'he','him','his', 'himself','she','her','hers','herself','it','its','itself',
            'they','them','their','theirs','themselves']
def get_keyword_dict_variables(long_filename, filename):

    long_filename_data = long_filename.split('/')
    if long_filename_data[1] == 'Text':
        corpus_name = 'all_text_corpus'
        if long_filename_data[2] == 'All':
            sub_corpus_name = 'overall_text'
        elif long_filename_data[2] == 'CFM':
            sub_corpus_name = 'cfm_text'
        elif long_filename_data[2] == 'GD':
            sub_corpus_name = 'gd_text'
        sub_sub_corpus_name = None
    elif long_filename_data[1] == 'Quotes':
        corpus_name = 'quotations_corpus'
        if long_filename_data[2] == 'Gendered':
            sub_corpus_name = 'all_gendered_quotes'
            if re.match('All',long_filename_data[3]):
                sub_sub_corpus_name = 'all_gendered_quotes_overall'
            elif re.match('CFM',long_filename_data[3]):
                sub_sub_corpus_name = 'cfm_gendered_quotes'
            elif re.match('GD',long_filename_data[3]):
                sub_sub_corpus_name = 'gd_gendered_quotes'
        elif long_filename_data[2] == 'Female':
            sub_corpus_name = 'female_quotes'
            if re.match('All',long_filename_data[3]):
                sub_sub_corpus_name = 'all_female_quotes'
            elif re.match('CFM',long_filename_data[3]):
                sub_sub_corpus_name = 'cfm_female_quotes'
            elif re.match('GD',long_filename_data[3]):
                sub_sub_corpus_name = 'gd_female_quotes'
        elif long_filename_data[2] == 'Male':
            sub_corpus_name = 'male_quotes'
            if re.match('All',long_filename_data[3]):
                sub_sub_corpus_name = 'all_male_quotes'
            elif re.match('CFM',long_filename_data[3]):
                sub_sub_corpus_name = 'cfm_male_quotes'
            elif re.match('GD',long_filename_data[3]):
                sub_sub_corpus_name = 'gd_male_quotes'


    filename_data = filename.split(' - ')

    #ngrams
    ngrams_data = filename_data[0].split('-')
    if len(ngrams_data) == 1:
        ngrams = '1'
    else:
        ngrams = ngrams_data[0]

    #unit type
    unit_type = re.sub('( \(.*?)?\.tsv', '', filename_data[-1])

    return corpus_name, sub_corpus_name, sub_sub_corpus_name, unit_type, ngrams

def read_keyword_file(data_folder_path, data_file):
    data_file_path = data_folder_path + "/" + data_file

    keyword_dict_variables = get_keyword_dict_variables(data_folder_path, data_file)
    corpus_name = keyword_dict_variables[0]
    sub_corpus_name = keyword_dict_variables[1]
    sub_sub_corpus_name = keyword_dict_variables[2]
    unit_type = keyword_dict_variables[3]
    ngrams = keyword_dict_variables[4]

    file_data = False
    with open(data_file_path, encoding='utf-8') as tsv_file:
        tsv_reader = csv.reader(tsv_file, delimiter='\t', quotechar='"')
        #print("Attempting to add to this dict spot: ", corpus_name, sub_corpus_name, sub_sub_corpus_name, 'unit_type', unit_type, 'ngrams', ngrams)
        for row in tsv_reader:
            if re.match('--',row[0]):
                file_data = True
            elif file_data is True:
                if sub_sub_corpus_name is None:
                    keyword_data[corpus_name][sub_corpus_name]['unit_type'][unit_type]['ngrams'][ngrams].append(row)
                else:
                    keyword_data[corpus_name][sub_corpus_name][sub_sub_corpus_name]['unit_type'][unit_type]['ngrams'][ngrams].append(row)
    return

def import_keyword_folders():
    for corpus_folder in os.listdir("LancsBox_Data"):
        corpus_folder_path = 'LancsBox_Data/' + corpus_folder
        for sub_corpus_folder in os.listdir(corpus_folder_path):
            if corpus_folder == 'Text':
                sub_corpus_folder_path = corpus_folder_path + "/" + sub_corpus_folder
                for data_file in os.listdir(sub_corpus_folder_path):
                    read_keyword_file(sub_corpus_folder_path,data_file)
            elif corpus_folder == 'Quotes':
                gender_corpus_folder_path = corpus_folder_path + "/" + sub_corpus_folder
                for sub_gender_corpus in os.listdir(gender_corpus_folder_path):
                    sub_gender_corpus_path = gender_corpus_folder_path + "/" + sub_gender_corpus
                    for data_file in os.listdir(sub_gender_corpus_path):
                        read_keyword_file(sub_gender_corpus_path,data_file)
    return

def print_keyword_dict():
    for corpus in keyword_data:
        print(corpus)
        for sub_corpus in keyword_data[corpus]:
            print("\t",sub_corpus)
            if corpus == 'all_text_corpus':
                print("\t\tSize: ",keyword_data[corpus][sub_corpus]['size'])
                print("\t\tUnit Types:")
                for unit_type in keyword_data[corpus][sub_corpus]['unit_type']:
                    print("\t\t\t",unit_type)
            else:
                for sub_sub_corpus in keyword_data[corpus][sub_corpus]:
                    print("\t\t",sub_sub_corpus)

                   # print()

def calculate_rf(corpus_size, actual_freq):
    rel_freq = actual_freq / corpus_size * 1000
    return rel_freq

def calculate_simple_maths(focus_rf, ref_rf, smoothing_n):
    simple_maths = (focus_rf + smoothing_n) / (ref_rf + smoothing_n)
    return simple_maths
def get_keywords(data):
    group_1 = data[0]
    group_1_name = data[1]
    group_2 = data[2]
    group_2_name = data[3]
    unit_type = data[4]
    ngrams = data[5]

    #print(group_1['size'])
    working_dict = {}
    #this is throwing an error with CFM/GD Female Quotes Word 1 Ngram but I can't figure out why and it still processes so who knows
    group_1_word_list = group_1['unit_type'][unit_type]['ngrams'][ngrams]
    group_2_word_list = group_2['unit_type'][unit_type]['ngrams'][ngrams]

    for word_data in group_1_word_list:
        word = word_data[0]
        if word not in stopwords and not re.search('\:',word):
            actual_freq = word_data[1].replace(',','')
            if word not in working_dict:
                working_dict[word] = {
                    'group_1_af':int(actual_freq),
                    'group_1_rf':calculate_rf(group_1['size'], int(actual_freq)),
                    'group_2_af':0,
                    'group_2_rf':0,
                    'simple_maths':0,
                }
    for word_data in group_2_word_list:
        word = word_data[0]
        if word not in stopwords and not re.search('\:', word):
            actual_freq = word_data[1].replace(',', '')
            if word not in working_dict:
                working_dict[word] = {
                    'group_2_af':int(actual_freq),
                    'group_2_rf':calculate_rf(group_2['size'], int(actual_freq)),
                    'group_1_af':0,
                    'group_1_rf':0,
                    'simple_maths':0,
                }
            else:
                working_dict[word]['group_2_af'] = int(actual_freq)
                working_dict[word]['group_2_rf'] = calculate_rf(group_2['size'], int(actual_freq))

    for word in working_dict:
        focus_rf =  working_dict[word]['group_1_rf']
        ref_rf =  working_dict[word]['group_2_rf']
        working_dict[word]['simple_maths'] = calculate_simple_maths(focus_rf, ref_rf, 0.1)

    new_csv_filename = "Generated_Keyword_Data/" + group_1_name + "_vs_" + group_2_name + "_" \
                       + unit_type + "_" + ngrams + "-ngrams" + ".csv"
    group_1_af_name = group_1_name + "_AF"
    group_1_rf_name = group_1_name + "_RF"
    group_2_af_name = group_2_name + "_AF"
    group_2_rf_name = group_2_name + "_RF"
    with open(new_csv_filename, 'w', newline='',encoding='utf-8') as csv_writefile:
        csv_writer = csv.writer(csv_writefile)
        csv_writer.writerow([unit_type, group_1_af_name, group_1_rf_name, group_2_af_name, group_2_rf_name, 'Simple Maths'])
        for word in working_dict:
            if working_dict[word]['group_1_af'] > 5 or working_dict[word]['group_2_af'] > 5:
                csv_writer.writerow([word, working_dict[word]['group_1_af'], working_dict[word]['group_1_rf'],
                                     working_dict[word]['group_2_af'], working_dict[word]['group_2_rf'],
                                     working_dict[word]['simple_maths']])

    return

def keyword_testing():

    #yeah I tried to read this in as a file and it was a nightmare
    groups_data = [
        [keyword_data['quotations_corpus']['female_quotes']['cfm_female_quotes'], 'CFM_Female_Quotes', keyword_data['quotations_corpus']['female_quotes']['gd_female_quotes'], 'GD_Female_Quotes', 'word', '1'],
        [keyword_data['quotations_corpus']['all_gendered_quotes']['cfm_gendered_quotes'], 'CFM_Gendered_Quotes', keyword_data['quotations_corpus']['all_gendered_quotes']['gd_gendered_quotes'], 'GD_Gendered_Quotes', 'word', '1'],
        [keyword_data['quotations_corpus']['male_quotes']['cfm_male_quotes'], 'CFM_Male_Quotes', keyword_data['quotations_corpus']['male_quotes']['gd_male_quotes'], 'GD_Male_Quotes', 'word', '1'],
        [keyword_data['quotations_corpus']['female_quotes']['all_female_quotes'], 'All_Female_Quotes', keyword_data['quotations_corpus']['male_quotes']['all_male_quotes'], 'All_Male_Quotes', 'word', '1'],
        [keyword_data['all_text_corpus']['overall_text'], 'Overall_Text', keyword_data['quotations_corpus']['all_gendered_quotes']['all_gendered_quotes_overall'], 'All_Gendered_Quotes', 'word', '1'],
        [keyword_data['quotations_corpus']['female_quotes']['cfm_female_quotes'], 'CFM_Female_Quotes', keyword_data['quotations_corpus']['male_quotes']['cfm_male_quotes'], 'CFM_Male_Quotes', 'word', '1'],
        [keyword_data['quotations_corpus']['female_quotes']['gd_female_quotes'], 'GD_Female_Quotes', keyword_data['quotations_corpus']['male_quotes']['gd_male_quotes'], 'GD_Male_Quotes', 'word', '1'],
        [keyword_data['quotations_corpus']['female_quotes']['cfm_female_quotes'], 'CFM_Female_Quotes', keyword_data['quotations_corpus']['female_quotes']['gd_female_quotes'], 'GD_Female_Quotes', 'class', '1'],
        [keyword_data['quotations_corpus']['all_gendered_quotes']['cfm_gendered_quotes'], 'CFM_Gendered_Quotes', keyword_data['quotations_corpus']['all_gendered_quotes']['gd_gendered_quotes'], 'GD_Gendered_Quotes', 'class', '1'],
        [keyword_data['quotations_corpus']['male_quotes']['cfm_male_quotes'], 'CFM_Male_Quotes', keyword_data['quotations_corpus']['male_quotes']['gd_male_quotes'], 'GD_Male_Quotes', 'class', '1'],
        [keyword_data['quotations_corpus']['female_quotes']['all_female_quotes'], 'All_Female_Quotes', keyword_data['quotations_corpus']['male_quotes']['all_male_quotes'], 'All_Male_Quotes', 'class', '1'],
        [keyword_data['all_text_corpus']['overall_text'], 'Overall_Text', keyword_data['quotations_corpus']['all_gendered_quotes']['all_gendered_quotes_overall'], 'All_Gendered_Quotes', 'class', '1'],
        [keyword_data['quotations_corpus']['female_quotes']['cfm_female_quotes'], 'CFM_Female_Quotes', keyword_data['quotations_corpus']['male_quotes']['cfm_male_quotes'], 'CFM_Male_Quotes', 'class', '1'],
        [keyword_data['quotations_corpus']['female_quotes']['gd_female_quotes'], 'GD_Female_Quotes', keyword_data['quotations_corpus']['male_quotes']['gd_male_quotes'], 'GD_Male_Quotes', 'class', '1'],
        [keyword_data['quotations_corpus']['female_quotes']['cfm_female_quotes'], 'CFM_Female_Quotes', keyword_data['quotations_corpus']['female_quotes']['gd_female_quotes'], 'GD_Female_Quotes', 'hw', '1'],
        [keyword_data['quotations_corpus']['all_gendered_quotes']['cfm_gendered_quotes'], 'CFM_Gendered_Quotes', keyword_data['quotations_corpus']['all_gendered_quotes']['gd_gendered_quotes'], 'GD_Gendered_Quotes', 'hw', '1'],
        [keyword_data['quotations_corpus']['male_quotes']['cfm_male_quotes'], 'CFM_Male_Quotes', keyword_data['quotations_corpus']['male_quotes']['gd_male_quotes'], 'GD_Male_Quotes', 'hw', '1'],
        [keyword_data['quotations_corpus']['female_quotes']['all_female_quotes'], 'All_Female_Quotes', keyword_data['quotations_corpus']['male_quotes']['all_male_quotes'], 'All_Male_Quotes', 'hw', '1'],
        [keyword_data['all_text_corpus']['overall_text'], 'Overall_Text', keyword_data['quotations_corpus']['all_gendered_quotes']['all_gendered_quotes_overall'], 'All_Gendered_Quotes', 'hw', '1'],
        [keyword_data['quotations_corpus']['female_quotes']['cfm_female_quotes'], 'CFM_Female_Quotes', keyword_data['quotations_corpus']['male_quotes']['cfm_male_quotes'], 'CFM_Male_Quotes', 'hw', '1'],
        [keyword_data['quotations_corpus']['female_quotes']['gd_female_quotes'], 'GD_Female_Quotes', keyword_data['quotations_corpus']['male_quotes']['gd_male_quotes'], 'GD_Male_Quotes', 'hw', '1'],
        [keyword_data['quotations_corpus']['female_quotes']['cfm_female_quotes'], 'CFM_Female_Quotes', keyword_data['quotations_corpus']['female_quotes']['gd_female_quotes'], 'GD_Female_Quotes', 'pos', '1'],
        [keyword_data['quotations_corpus']['all_gendered_quotes']['cfm_gendered_quotes'], 'CFM_Gendered_Quotes', keyword_data['quotations_corpus']['all_gendered_quotes']['gd_gendered_quotes'], 'GD_Gendered_Quotes', 'pos', '1'],
        [keyword_data['quotations_corpus']['male_quotes']['cfm_male_quotes'], 'CFM_Male_Quotes', keyword_data['quotations_corpus']['male_quotes']['gd_male_quotes'], 'GD_Male_Quotes', 'pos', '1'],
        [keyword_data['quotations_corpus']['female_quotes']['all_female_quotes'], 'All_Female_Quotes', keyword_data['quotations_corpus']['male_quotes']['all_male_quotes'], 'All_Male_Quotes', 'pos', '1'],
        [keyword_data['all_text_corpus']['overall_text'], 'Overall_Text', keyword_data['quotations_corpus']['all_gendered_quotes']['all_gendered_quotes_overall'], 'All_Gendered_Quotes', 'pos', '1'],
        [keyword_data['quotations_corpus']['female_quotes']['cfm_female_quotes'], 'CFM_Female_Quotes', keyword_data['quotations_corpus']['male_quotes']['cfm_male_quotes'], 'CFM_Male_Quotes', 'pos', '1'],
        [keyword_data['quotations_corpus']['female_quotes']['gd_female_quotes'], 'GD_Female_Quotes', keyword_data['quotations_corpus']['male_quotes']['gd_male_quotes'], 'GD_Male_Quotes', 'pos', '1'],
        [keyword_data['quotations_corpus']['female_quotes']['cfm_female_quotes'], 'CFM_Female_Quotes', keyword_data['quotations_corpus']['female_quotes']['gd_female_quotes'], 'GD_Female_Quotes', 'sem', '1'],
        [keyword_data['quotations_corpus']['all_gendered_quotes']['cfm_gendered_quotes'], 'CFM_Gendered_Quotes', keyword_data['quotations_corpus']['all_gendered_quotes']['gd_gendered_quotes'], 'GD_Gendered_Quotes', 'sem', '1'],
        [keyword_data['quotations_corpus']['male_quotes']['cfm_male_quotes'], 'CFM_Male_Quotes', keyword_data['quotations_corpus']['male_quotes']['gd_male_quotes'], 'GD_Male_Quotes', 'sem', '1'],
        [keyword_data['quotations_corpus']['female_quotes']['all_female_quotes'], 'All_Female_Quotes', keyword_data['quotations_corpus']['male_quotes']['all_male_quotes'], 'All_Male_Quotes', 'sem', '1'],
        [keyword_data['all_text_corpus']['overall_text'], 'Overall_Text', keyword_data['quotations_corpus']['all_gendered_quotes']['all_gendered_quotes_overall'], 'All_Gendered_Quotes', 'sem', '1'],
        [keyword_data['quotations_corpus']['female_quotes']['cfm_female_quotes'], 'CFM_Female_Quotes', keyword_data['quotations_corpus']['male_quotes']['cfm_male_quotes'], 'CFM_Male_Quotes', 'sem', '1'],
        [keyword_data['quotations_corpus']['female_quotes']['gd_female_quotes'], 'GD_Female_Quotes', keyword_data['quotations_corpus']['male_quotes']['gd_male_quotes'], 'GD_Male_Quotes', 'sem', '1']]

    with open('group_data.csv', encoding='utf-8') as csv_readfile:
        csv_reader = csv.reader(csv_readfile)
        for row in csv_reader:
            groups_data.append(row)

    #all text vs all gendered quotes (text does contain quotes though)
    #cfm quotes vs gd quotes
    #all female vs all male
    #cfm female vs cfm male
    #gd female vs gd male
    #cfm female vs gd female
    #cfm male vs gd male


    for data in groups_data:
        get_keywords(data)
    return

def main():
    import_keyword_folders()
    keyword_testing()

   # print_keyword_dict()

    #do the thing
    return

main()