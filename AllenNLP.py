# pip3 install torch==1.3.0+cpu torchvision==0.4.1+cpu -f https://download.pytorch.org/whl/torch_stable.html
# pip install allennlp
from allennlp.predictors.predictor import Predictor
import logging
# import nltk
# from utilities import remove_stopwords
import configuration
# predictor = Predictor.from_path("../bert-base-srl-2019.06.17.tar.gz")
# predictor.predict(
#   sentence="Did Uriah honestly think he could beat the game in under three hours?"
# )
import re
semantec_description_pattern = re.compile(r'\[(.*?)\]')
from nltk.stem.wordnet import WordNetLemmatizer
logger = logging.getLogger(__name__)
"""
{
    'verbs':
        [
            {
                'verb': 'looks',
                'description': '[ARG0: The Trojan] [V: looks] [ARG1: for certain file types , including some ,] [ARGM-PRP: to upload them to a Google Drive account] .',
                'tags': ['B-ARG0', 'I-ARG0', 'B-V', 'B-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'B-ARGM-PRP', 'I-ARGM-PRP', 'I-ARGM-PRP', 'I-ARGM-PRP', 'I-ARGM-PRP', 'I-ARGM-PRP', 'I-ARGM-PRP', 'I-ARGM-PRP', 'O']
            },
            {
                'verb': 'including',
                'description': 'The Trojan looks for [ARG2: certain file types] , [V: including] [ARG1: some] , to upload them to a Google Drive account .',
                'tags': ['O', 'O', 'O', 'O', 'B-ARG2', 'I-ARG2', 'I-ARG2', 'O', 'B-V', 'B-ARG1', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']
            },
            {
                'verb': 'upload',
                'description': '[ARG0: The Trojan] looks for certain file types , including some , to [V: upload] [ARG1: them] [ARG2: to a Google Drive account] .',
                'tags': ['B-ARG0', 'I-ARG0', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'B-V', 'B-ARG1', 'B-ARG2', 'I-ARG2', 'I-ARG2', 'I-ARG2', 'I-ARG2', 'O']
            }
        ],
    'words':
        ['The', 'Trojan', 'looks', 'for', 'certain', 'file', 'types', ',', 'including', 'some', ',', 'to', 'upload', 'them', 'to', 'a', 'Google', 'Drive', 'account', '.']
}
"""

def print_AllenNLP_predictor(predictor):
    lists = predictor['verbs']
    # for extraction in lists:
    #     print(extraction['verb'])
        # print()



def process_single_AllenNLP_description(single_extraction_description):
    # match [Arg0:the Trpjan]
    match = semantec_description_pattern.findall(single_extraction_description)
    single_extraction_dictionary = dict()
    for results in enumerate(match):
        tuples = results[1]
        arg_name = tuples[0:tuples.find(':')].strip() # Arg0
        arg_val = tuples[tuples.find(':') + 1:].strip() # the Trojan
        if arg_name not in list(single_extraction_dictionary.keys()):
            single_extraction_dictionary[arg_name] = arg_val
    return single_extraction_dictionary

def get_subject_verb():
    pass

def process_IOC_from_semantec_extraction_list(semantec_extraction_list, sentence_dict):
    out_list = list()
    for semantec_dict in semantec_extraction_list:
        for key in semantec_dict.keys():
        # if 'ARG1' in semantec_dict.keys():
            temp_sent = semantec_dict[key]
            semantec_dict[key] = temp_sent.replace('following', sentence_dict['original'])
        # if 'ARG2' in semantec_dict.keys():
        #     temp_sent = semantec_dict['ARG2']
        #     semantec_dict['ARG2'] = temp_sent.replace('following', sentence_dict['original'])
        out_list.append(semantec_dict)
    return out_list

def get_and_process_semantec_role_label_list(predictor, sentence):
    predict = predictor.predict(sentence=sentence)
    # print(predict)
    extraction_list = list()
    if len(predict['verbs']) == 0:
        print('AllenNLP can not extract: ', sentence)
        return False, extraction_list
    '''
    sentence='When clicked it launches an infection chain made up of JavaScript, and a final shellcode payload that makes use of DNS to load additional shellcode from a remote command and control server.'
    predict = {
        'verbs': 
            [
                {
                    'verb': 'clicked', 
                    'description': '[ARGM-TMP: When] [V: clicked] [ARG1: it] launches an infection chain made up of JavaScript , and a final shellcode payload that makes use of DNS to load additional shellcode from a remote command and control server .', 
                    'tags': ['B-ARGM-TMP', 'B-V', 'B-ARG1', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']
                }, 
                {
                    'verb': 'launches', 
                    'description': '[ARGM-TMP: When clicked] [ARG0: it] [V: launches] [ARG1: an infection chain made up of JavaScript , and a final shellcode payload that makes use of DNS to load additional shellcode from a remote command and control server] .', 
                    'tags': ['B-ARGM-TMP', 'I-ARGM-TMP', 'B-ARG0', 'B-V', 'B-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'I-ARG1', 'O']
                }, 
                {
                    'verb': 'made', 
                    'description': 'When clicked it launches [ARG1: an infection chain] [V: made] up [ARG0: of JavaScript] , and a final shellcode payload that makes use of DNS to load additional shellcode from a remote command and control server .', 
                    'tags': ['O', 'O', 'O', 'O', 'B-ARG1', 'I-ARG1', 'I-ARG1', 'B-V', 'O', 'B-ARG0', 'I-ARG0', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']
                }, 
                {
                    'verb': 'makes', 
                    'description': 'When clicked it launches an infection chain made up of JavaScript , and [ARG0: a final shellcode payload] [R-ARG0: that] [V: makes] [ARG1: use] [ARG2: of DNS] [ARG2: to load additional shellcode from a remote command and control server] .', 
                    'tags': ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'B-ARG0', 'I-ARG0', 'I-ARG0', 'I-ARG0', 'B-R-ARG0', 'B-V', 'B-ARG1', 'B-ARG2', 'I-ARG2', 'B-ARG2', 'I-ARG2', 'I-ARG2', 'I-ARG2', 'I-ARG2', 'I-ARG2', 'I-ARG2', 'I-ARG2', 'I-ARG2', 'I-ARG2', 'I-ARG2', 'O']
                }, 
                {
                    'verb': 'load', 
                    'description': 'When clicked it launches an infection chain made up of JavaScript , and a final shellcode payload [ARG0: that] makes use of DNS to [V: load] [ARG1: additional shellcode] [ARGM-DIR: from a remote command and control server] .', 
                    'tags': ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'B-ARG0', 'O', 'O', 'O', 'O', 'O', 'B-V', 'B-ARG1', 'I-ARG1', 'B-ARGM-DIR', 'I-ARGM-DIR', 'I-ARGM-DIR', 'I-ARGM-DIR', 'I-ARGM-DIR', 'I-ARGM-DIR', 'I-ARGM-DIR', 'O']
                }
            ], 
        'words': ['When', 'clicked', 'it', 'launches', 'an', 'infection', 'chain', 'made', 'up', 'of', 'JavaScript', ',', 'and', 'a', 'final', 'shellcode', 'payload', 'that', 'makes', 'use', 'of', 'DNS', 'to', 'load', 'additional', 'shellcode', 'from', 'a', 'remote', 'command', 'and', 'control', 'server', '.']
    }
    '''
    # attack_vector_list = list()
    # bag_of_word_list = list()
    for extractions in predict['verbs']:
        verb = extractions['verb']
        # checking from the verb_list
        print(verb)
        if helper.is_dictionay_key(configuration.preprocessOntologies.verb_dict, configuration.stemmer.stem(verb)):
            description = extractions['description']
            # print('description:',description)
            # # print(description)
            single_extraction_dict = process_single_AllenNLP_description(description)
            print(single_extraction_dict)
            extraction_list.append(single_extraction_dict)
            '''
            single_extraction_dict = {
                'ARGM-TMP': 'When clicked', 
                'ARG0': 'it', 'V': 'launches', 
                'ARG1': 'an infection chain made up of JavaScript , and a final shellcode payload that makes use of DNS to load additional shellcode from a remote command and control server'
            }, 
            # isMaliciousAction, attack_vector = analyze_single_extraction(single_extraction_dict)
            # 
            # if isMaliciousAction:
            #     # filter out non cyber objects
            #     isMalicious = filter_based_on_cyber_object(attack_vector)
            # 
            #     if isMalicious:
            #         extraction_list.append(single_extraction_dict)
            #         attack_vector_list.append(attack_vector)
            #         bag_of_word_list.append(create_bag_of_word_from_attack_vector(attack_vector, ['what', 'where']))
            # 
            # else:
            #     print('Non Malicious Vector:', attack_vector)


            attack_vector = {'what':'','where':'','why':'','how':'','when':''}
            '''
    '''
    extraction_list = [
        {
            'ARGM-TMP': 'When', 
            'V': 'clicked', 
            'ARG1': 'it'
        }, 
        {
            'ARGM-TMP': 'When clicked', 
            'ARG0': 'it', 'V': 'launches', 
            'ARG1': 'an infection chain made up of JavaScript , and a final shellcode payload that makes use of DNS to load additional shellcode from a remote command and control server'
        }
    ]

    '''

    return True, extraction_list#, attack_vector_list, bag_of_word_list


def get_verb_and_subject(extraction_list):

    if len(extraction_list) >= 1:
        for extraction in extraction_list:
            # extraction = extraction_list[0]
            arg_list = list(extraction.keys())
            if 'V' in arg_list and 'ARG0' in arg_list:
                if extraction['ARG0'] not in ['you','we']:
                    configuration.prev_verb = extraction['V']
                    configuration.prev_subject = extraction['ARG0']
                    if 'ARG1' in arg_list:
                        configuration.prev_object = helper.remove_stopwords(extraction['ARG1'])
                # else:
                #     configuration.prev_subject = ''
                #     configuration.prev_verb = ''


def print_list(__list__,text, filename= 'test.csv',isFileWrite=True):
    import csv

    with open(filename,'a+', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        file_list = list()
        for __ in __list__:
            file_list = list()
            file_list.append(text)
            text = ''
            for _ in __:
                file_list.append(_)
                # # print(_)
            # file_list.append('')
            writer.writerow(file_list)
    return

import nltk
import coreference
import regex_checker
def get_text_from_input(text, isFile=True, isSymantecReport=False):
    from helper import FileReader
    preprocess_tools = FileReader(text)
    if isFile:
        file_name = regex_checker.get_malware_name(text)
        # file_name = text[:-3]
        # file_name = text[text.rindex('/'):text.rfind('.')
        text = preprocess_tools.read_file()
        if file_name:
            change_text = file_name.replace('.','_')
            text = text.replace(file_name, change_text)
        text = text.replace('back door', 'backdoor')
        # text = text.replace('following', '')

    # else:
    #     text = nltk.sent_tokenize(text)
    print('Sentence: ', text)
    if isSymantecReport:
        text_list = preprocess_tools.symantec_sent_tokenize(text)
    #     text_list = list of {'original':sentence,'processed':new_sentence}
    else:
        text_list = preprocess_tools.get_all_valid_sentences(text)
    preprocess_tools.print_sentence(text_list)
    return text_list

def mitre_description():
    path = 'C:\\Users\\rrahman3\\codes\\research-codes\\python-scraping\\Mitre_Techniue_Description_Enterprise.csv'
    import csv
    __list__ = list()
    with open(path,'r',newline='') as file:
        reader = csv.DictReader(file,delimiter=',',quotechar='"')
        for row in reader:
            __list__.append({'Name':row['Technique Name'],'Text':row['Description']})
            # # print(row['Technique Name'], '\n', row['Description'])
    return __list__

# def precess_list(__list__):
#     predictor = configuration.model_AllenNLP_SRL
#     for examples in __list__:
#         # # print('-'*10 + examples['Name'] + '-'*10)
#         text = get_text_from_input(examples['Text'], False)
#         print_list([],examples['Name'])
#         for sentence in text:
#             res = semantec_finder(predictor, sentence)
#             # # print(res)
#             print_list(res, sentence)


def preprocess_API_Des():
    with open('reports/test.txt') as file:
        a = file.read().split('\n')
        for _a_ in a:
            api_name = _a_.split(' ')[0] + ' '
            lower = _a_.split(' ')[1].lower()
            final_result = api_name + lower + _a_[len(api_name) + len(lower):]
            # # print(final_result)

def get_Allen_NLP_Extraction(predictor, isFile=True, isLemmatize=True, isStem=True, file_name = 'reports/fireeye_fin7_application_shimming.txt', isSymantecReport=True, isFileWrite=True):
    # # print(predictor.predict("Mandiant identified that FIN7 also used this technique to install a payment card harvesting utility to persistent access."))
    print('isSymantecReprot: ',isSymantecReport)
    text = get_text_from_input(file_name, isFile, isSymantecReport=isSymantecReport)
    text = coreference.coref_text_with_list(configuration.model_AllenNLP_Coref,text)

    '''
        text = list of {'original':sentence,'processed':new_sentence}
    '''
    # print(text)
    final_list = list()
    # text = ['Figure 1 displays the two registry keys created when a shim is registered with the “sdbinst.exe” utility.']
    # text = ['The second stage shellcode launched the CARBANAK DLL (stored in a registry key), which spawned an instance of Service Host (“svchost.exe”) and injected itself into that process.']

    isContinuousActions = False
    for sentence_dict in text:
        sentence = sentence_dict['processed']
        print('\nNow Approaching: ', sentence, '\nPrvious Verb: ', configuration.prev_verb, '\nPrevious Subject: ', configuration.prev_subject)
        if len(sentence) == 0:
            continue
        if hasSubject(sentence):
            isContinuousActions = False
            configuration.prev_sentence = sentence
            sentence = sentence.replace('following', '')

            print('Perfectly Structured Sentence')
            isAllenNLPExtract, semantec_extraction_list = get_and_process_semantec_role_label_list(predictor, sentence)

            # print(semantec_extraction_list)
            get_verb_and_subject(semantec_extraction_list)
            print('Each Time: Verb:', configuration.prev_verb, 'Subject:', 'Verb:', configuration.prev_subject)

        # Check non extractable sentences. CPU Speed, Update file
        else:
            print('Not Structured Sentence')

            # if not isAllenNLPExtract:
            print('Verb:', configuration.prev_verb, 'Subject:', 'Verb:', configuration.prev_subject)
            # if isVerbExistInPostTag(sentence) and not helper.stem_and_lemmatize(configuration.prev_verb) == helper.stem_and_lemmatize('perfrom'):
            # if helper.stem_and_lemmatize(configuration.prev_verb) == helper.stem_and_lemmatize('perform'):
            # if  helper.stem_and_lemmatize(configuration.prev_verb) == helper.stem_and_lemmatize('perfrom'):
            isDNS = False
            if isVerbExistInPostTag(sentence):
                isContinuousActions = True
            if isContinuousActions:
                if isVerbExistInPostTag(sentence):
                    isContinuousActions = True
                    new_sentence = configuration.prev_subject + ' may ' + modify_fake_senteces(sentence)
                else:
                    isContinuousActions = True
                    new_sentence = configuration.prev_subject + ' may ' + modify_fake_senteces(sentence)

            else:

                if 'following' in configuration.prev_sentence:
                    new_sentence = configuration.prev_sentence
                else:
                    new_sentence = configuration.prev_subject + ' may ' + \
                                   WordNetLemmatizer().lemmatize(configuration.prev_verb, 'v') + ' ' + \
                                   configuration.prev_object
                               # sentence_dict['processed'] + ' ' + \
                isDNS = True

            sentence = new_sentence
            isAllenNLPExtract, semantec_extraction_list = get_and_process_semantec_role_label_list(predictor, new_sentence)
            print('Sentence:',new_sentence,'\nisAllenNLPExtract: ',isAllenNLPExtract)
            if isDNS:
                semantec_extraction_list = process_IOC_from_semantec_extraction_list(semantec_extraction_list, sentence_dict)
                sentence = sentence.replace('following', sentence_dict['original'])
            print(semantec_extraction_list)


        if isAllenNLPExtract:
            attack_vector_list = analyze_whole_sentence(semantec_extraction_list)



            # attack_vector_list = get_cyber_object(sentence, attack_vector_list)
            # remove the non cyber object extraction
            attack_vector_list = filter_whole_sentence_extraction(attack_vector_list)

            # attack_vector_list = delete_extra_args(attack_vector_list)


            bag_of_word_list = create_bag_of_word_from_whole_sentence(attack_vector_list, ['what', 'where'])

            final_list.append({'text': sentence, 'bow': bag_of_word_list, 'compact_vector': attack_vector_list})

        # else:
        #     sent_list = sentence.split()
        #     if len(sent_list) >= 2:
        #         verb = sent_list[0]
        #         object = helper.remove_stopwords(' '.join(sent_list[1:]))
        #         attack_vector_list = [{'what':verb,'where':object,'why':'','how':'','when':''}]
        #         attack_vector_list = filter_whole_sentence_extraction(attack_vector_list)
        #         bag_of_word_list = create_bag_of_word_from_whole_sentence(attack_vector_list, ['what', 'where'])
        #
        #         final_list.append({'text': sentence, 'bow': bag_of_word_list, 'compact_vector': attack_vector_list})
        # print('semantec_extraction_list:',semantec_extraction_list)
        # print('attack_vector_list:',attack_vector_list)
        # print('bag_of_word_list:',bag_of_word_list)

        # final_list.append({'text':sentence, 'bow':bag_of_word_list, 'compact_vector':attack_vector_list})

    print_extraction(final_list)
    return final_list



def modify_fake_senteces(sentences):
    pos_tag_dict = get_stanford_pos_tag(sentences)
    ss = sentences.split()
    if len(ss) > 0:
        try:
            if pos_tag_dict[ss[0]].startswith('VB'):
                aa = WordNetLemmatizer().lemmatize(ss[0], 'v') + ' ' + ' '.join(ss[1:])
            else:
                aa = ' '.join(ss)
        except:
            aa = ' '.join(ss)
    else:
        aa = ' '.join(ss)
    return aa


def print_extraction(detected_list):
    for dictionary in detected_list:
        # print(dictionary['text'])
        for attack_vector in dictionary['compact_vector']:
            print(attack_vector)
        # print('\n')


def garbase_code_for_cyber_object(final_list):
    print('\n\n\n')
    import bm25_match
    cyber_model = configuration.cyber_model
    cyber_corpus = configuration.cyber_corpus

    missing_list = list()
    attack_list = list()
    cyber_object_based_list = list()


    for extraction in final_list:
        print('\n')
        bow_vector = list()
        c_vector = list()
        for compact_vector in extraction["compact_vector"]:
            if bm25_match.query_cyber_object(cyber_model, compact_vector['where'], cyber_corpus):
                attack_list.append(compact_vector)
                c_vector.append(compact_vector)
                # print(compact_vector)
            else:
                missing_list.append(compact_vector)
                # print('Got Rejected:', compact_vector)

        for compact_list in c_vector:
            temp_word = ''
            for key in compact_list.keys():
                if key in ['what', 'where']:
                    temp_word += helper.stem_and_lemmatize(compact_list[key]) + ' '
            bow_vector.append(temp_word.split())
        cyber_object_based_list.append({'text':extraction['text'], 'bow':bow_vector, 'compact_vector':c_vector})

    print('Attack List:', len(attack_list))
    for lists in attack_list:
        print(lists)
    print('Missing List:', len(missing_list))
    helper.write_csv_from_dictionary('ontology/new/fin7_temp_6.csv',attack_list)
    for lists in missing_list:
        print(lists)
    helper.write_csv_from_dictionary('ontology/extraction.csv',attack_list)
    print(cyber_object_based_list)

# tuple_list = [[('ARG0', 'Mandiant'), ('V', 'identified')], [('ARG0', 'the group'), ('V', 'leveraged'), ('ARG1', 'an application shim database')], [('ARG0', 'the group'), ('V', 'achieve'), ('ARG1', 'persistence'), ('ARGM-LOC', 'on systems in multiple environments')]]
# lists = [('ARG0', 'Mandiant'), ('V', 'identified')], [('ARG0', 'the group'), ('V', 'leveraged'), ('ARG1', 'an application shim database')]
# tuples = ('ARG0', 'Mandiant')
# dict_list = [{'ARG0':'Mandiant'}]
'''
dict_list = 
    [
        {
            'ARGM-TMP': 'When clicked', 
            'ARG0': 'it', 
            'V': 'launches', 
            'ARG1': 'an infection chain made up of JavaScript , and a final shellcode payload that makes use of DNS to load additional shellcode from a remote command and control server'
        }, 
        {
            'ARG0': 'a final shellcode payload', 
            'R-ARG0': 'that', 
            'V': 'makes', 
            'ARG1': 'use', 
            'ARG2': 'to load additional shellcode from a remote command and control server'
        }, 
        {
            'ARG0': 'that', 
            'V': 'load', 
            'ARG1': 'additional shellcode', 
            'ARGM-DIR': 'from a remote command and control server'
        }
    ]
'''
def tuple_list_to_dict_list(tuple_list):
    dict_list = list()
    for lists in tuple_list:
        __dict__ = dict()
        for tuples in lists:
            __dict__[tuples[0]] = tuples[1]
        dict_list.append(__dict__)
    # print('Dict_list: ', dict_list)
    return dict_list

import helper

def create_bow(sentence, lists, keys, isLmmatize=True, isStem=True):
    print('lllistttt',lists)
    bow = list()
    bow_word = ''
    for key in keys:
        if key in lists.keys():
            bow_word += helper.stem_and_lemmatize(lists[key],isRemoveStopword=True)
    bow = list(set(bow_word.split()))
    return bow

def create_attack_vector():
    return {'what':'','where':'','why':'','how':'','when':''}

import helper
# def create_bow_from_allen_nlp(sentence, dict_list, isLmmatize=True, isStem=True):
#     result_list = list()
#     # # print('dict_list', dict_list)
#     attack_vector_list = list()
#     compact_attack_vector_list = list()
#     for lists in dict_list:
#         print('list_res', lists)
#         attack_vector = create_attack_vector()
#         compact_attack_vector = create_attack_vector()
#         # # print('listtttttttttt', lists)
#         # # print([elem in lists.keys() for elem in ['V', 'ARG1']])
#         isAttributePresent = all(elem in lists.keys() for elem in ['ARGM-NEG'])
#         if isAttributePresent:
#             # print('Negetive Sentence Found')
#             continue
#         if 'ARG0' not in list(lists.keys()):
#             continue
#         if 'ARG0' in list(lists.keys()) and lists['ARG0'].strip() == 'we':
#             continue
#         isAttributePresent = all(elem in lists.keys() for elem in ['V', 'ARG1'])
#         if isAttributePresent:
#             if 'itself' in lists['ARG1'].split() or 'it' in lists['ARG1'].split():
#                 bow = create_bow(sentence, lists, ['V', 'ARG0'], isLmmatize, isStem)
#             else:
#                 bow = create_bow(sentence, lists, ['V', 'ARG1'], isLmmatize, isStem)
#
#             if len(bow)>0:
#                 attack_vector['what'] = helper.remove_stopwords(lists['V'])
#                 compact_attack_vector['what'] = helper.remove_stopwords(lists['V'])
#                 if ('itself' in lists['ARG1'].split() or 'it' in lists['ARG1'].split()) and 'ARG0' in lists.keys():
#                     attack_vector['where'] = helper.remove_stopwords(lists['ARG0'])
#                     compact_attack_vector['where'] = helper.remove_stopwords(lists['ARG0'])
#                 else:
#                     attack_vector['where'] = helper.remove_stopwords(lists['ARG1'])
#                     compact_attack_vector['where'] = helper.remove_stopwords(lists['ARG1'])
#                 attack_vector_list.append(attack_vector)
#                 result_list.append(bow)
#
#         isAttributePresent = all(elem in lists.keys() for elem in ['ARGM-PRP'])
#         if isAttributePresent:
#             bow = create_bow(sentence, lists, ['ARGM-PRP'], isLmmatize, isStem)
#             if len(bow)>0:
#                 attack_vector['why'] = helper.remove_stopwords(lists['ARGM-PRP'])
#                 compact_attack_vector['why'] = helper.remove_stopwords(lists['ARGM-PRP'])
#                 attack_vector_list.append(attack_vector)
#                 result_list.append(bow)
#
#         isAttributePresent = all(elem in lists.keys() for elem in ['ARG2'])
#         if isAttributePresent:
#             if 'to' in lists['ARG2'].split():
#                 bow = create_bow(sentence, lists, ['ARG2'], isLmmatize, isStem)
#                 if len(bow)>0:
#                     attack_vector['why'] = helper.remove_stopwords(lists['ARG2'])
#                     compact_attack_vector['why'] = helper.remove_stopwords(lists['ARG2'])
#                     attack_vector_list.append(attack_vector)
#                     result_list.append(bow)
#
#         isAttributePresent = all(elem in lists.keys() for elem in ['ARGM-MNR'])
#         if isAttributePresent:
#             bow = create_bow(sentence, lists, ['ARGM-MNR'], isLmmatize, isStem)
#             if len(bow)>0:
#                 attack_vector['how'] = helper.remove_stopwords(lists['ARGM-MNR'])
#                 compact_attack_vector['how'] = helper.remove_stopwords(lists['ARGM-MNR'])
#                 attack_vector_list.append(attack_vector)
#                 # result_list.append(bow)
#         compact_attack_vector_list.append(compact_attack_vector)
#         # attack_vector_list.append(attack_vector)
#     # print('List From AllenNLP',result_list)
#     # print('ATTACK VECTOR LIST',attack_vector_list)
#     compact_attack_vector_list = delete_extra_arg1(compact_attack_vector_list)
#     result_list = list()
#     for compact_list in compact_attack_vector_list:
#         temp_word = ''
#         for key in compact_list.keys():
#             if key in ['what', 'where']:
#                 temp_word += helper.stem_and_lemmatize(compact_list[key])
#         result_list.append(temp_word.split())
#     return result_list, attack_vector_list, compact_attack_vector_list

def compare_where_with_others(attack_vectors, currrent_index, vector_list):
    where = [x for x in attack_vectors['where'].split()]
    # print(where)
    temp_where = ''
    for i in range (currrent_index+1,len(vector_list)):
        for key, val in vector_list[i].items():
            vals = val.split()
            for vv in vals:
                if vv in where:
                    # print('V:', vv)
                    where.remove(vv)
    attack_vectors['where'] = ' '.join(where)
    return attack_vectors



def delete_extra_args(compact_attack_vector_list):
    temp = list()
    for attcks in enumerate(compact_attack_vector_list):
        temp_vector = compare_where_with_others(attcks[1], attcks[0], compact_attack_vector_list)
        if temp_vector['where'] != '':
            temp.append(temp_vector)
    # for __ in temp:
    #     print(__)
    return temp

if __name__=='__main__':
    import time
    start_time = time.time()

    a = [
            {'what': 'using', 'where': 'RTF document containing embedded JavaScript OLE object', 'why': '', 'how': '', 'when': ''},
            {'what': 'containing', 'where': 'embedded JavaScript OLE object', 'why': '', 'how': '', 'when': ''},
            {'what': 'embedded', 'where': 'JavaScript OLE object', 'why': '', 'how': '', 'when': ''}
    ]

    delete_extra_args(a)
    # process_directory('reports/test.txt')
    # get_Allen_NLP_Extraction(predictor=configuration.model_AllenNLP_SRL, isFile=True, isLemmatize=True, isStem=True, isSymantecReport=False, isFileWrite=False, file_name='reports/test.txt')
    end_time = time.time()
    # print('Time: ', (end_time-start_time)/1000)
# get_Allen_NLP_Extraction(isFile=True, isLmmatize=True, isStem=True, file_name='reports/fireeye_fin7_application_shimming.txt')
# des_list = mitre_description()
# precess_list(des_list)
# preprocess_API_Des()

'''
extracted_dictionary = {
    'ARGM-TMP': 'When clicked', 
    'ARG0': 'it', 'V': 'launches', 
    'ARG1': 'an infection chain made up of JavaScript , and a final shellcode payload that makes use of DNS to load additional shellcode from a remote command and control server'
}
'''
def analyze_whole_sentence(extracted_list):
    compact_attack_vector_list = list()
    for extracted_dictionary in extracted_list:
        isMalicious, compact_attack_vector = analyze_single_extraction(extracted_dictionary)
        if isMalicious:
            compact_attack_vector_list.append(compact_attack_vector)
    return compact_attack_vector_list


def analyze_single_extraction(extracted_dictionary):
    if len(extracted_dictionary) <= 1:
        return False, create_attack_vector()
    args_list = list(extracted_dictionary.keys())
    result_list = list()
    # # print('dict_list', dict_list)
    compact_attack_vector = create_attack_vector()

    # check for negetive sentence
    isAttributePresent = all(elem in args_list for elem in ['ARGM-NEG'])
    if isAttributePresent:
        compact_attack_vector['what'] = 'ARGM-NEG'
        return False, compact_attack_vector

    # Without subject, remove
    # if 'ARG0' not in list(args_list):
    #     return False, create_attack_vector()

    # Subject tracking
    if 'ARG0' in args_list and extracted_dictionary['ARG0'].strip() == 'we':
        # print('Skipped because no ARG0 extracted')
        return False, compact_attack_vector

    # Check for V and ARG1
    isAttributePresent = all(elem in args_list for elem in ['V', 'ARG1'])
    if isAttributePresent:
        # Check for preposition in ARG1, cyber_object
        compact_attack_vector['what'] = helper.remove_stopwords(extracted_dictionary['V'])
        if ('itself' in extracted_dictionary['ARG1'].split() or 'it' in extracted_dictionary['ARG1'].split()) and 'ARG0' in args_list:
            compact_attack_vector['where'] = helper.remove_stopwords(extracted_dictionary['ARG0'])
        else:
            compact_attack_vector['where'] = helper.remove_stopwords(extracted_dictionary['ARG1'])

    # Check for purpose
    isAttributePresent = all(elem in args_list for elem in ['ARGM-PRP'])
    isWhyFound = True
    if isAttributePresent:
        compact_attack_vector['why'] = helper.remove_stopwords(extracted_dictionary['ARGM-PRP'])
        isWhyFound = False

    # Need to add propbank extraction
    isAttributePresent = all(elem in args_list for elem in ['ARG2'])
    if isAttributePresent and isWhyFound:
        if 'to' in extracted_dictionary['ARG2'].split():
            compact_attack_vector['why'] = helper.remove_stopwords(extracted_dictionary['ARG2'])

    # Check for manner --> how
    isAttributePresent = all(elem in args_list for elem in ['ARGM-MNR'])
    if isAttributePresent:
        compact_attack_vector['how'] = helper.remove_stopwords(extracted_dictionary['ARGM-MNR'])

    isAttributePresent = all(elem in args_list for elem in ['ARGM-TMP'])
    if isAttributePresent:
        compact_attack_vector['when'] = extracted_dictionary['ARGM-TMP']
        # compact_attack_vector['when'] = helper.remove_stopwords(extracted_dictionary['ARGM-TMP'])
        # if len(compact_attack_vector['when']) == 0:
        #     return False, compact_attack_vector


    return True, compact_attack_vector

import  bm25_match

def filter_whole_sentence_extraction(compact_attack_vector_list):
    attack_vector_list = list()
    for compact_attack_vector in compact_attack_vector_list:
        isCyberObject = filter_based_on_cyber_object(compact_attack_vector)
        if isCyberObject:
            attack_vector_list.append(compact_attack_vector)
    return attack_vector_list

def filter_based_on_cyber_object(compact_attack_vector):
    if '_' in compact_attack_vector['where']:
        compact_attack_vector['where'] = compact_attack_vector['where'].replace('_', ' ')
    if bm25_match.query_cyber_object(configuration.cyber_model, compact_attack_vector['where'], configuration.cyber_corpus):
        return True
    else:
        print('Missed, Non Cyber:', compact_attack_vector)
        return False


# print('List From AllenNLP',result_list)
# print('ATTACK VECTOR LIST',attack_vector_list)
# compact_attack_vector_list = delete_extra_args(compact_attack_vector_list)
# result_list = list()
# for compact_list in compact_attack_vector_list:
#     temp_word = ''
#     for key in compact_list.keys():
#         if key in ['what', 'where']:
#             temp_word += helper.stem_and_lemmatize(compact_list[key])
#     result_list.append(temp_word.split())
# return result_list, attack_vector_list, compact_attack_vector_list

# keys must be ['what','where','why','where','how']

def create_bag_of_word_from_whole_sentence(attack_vector_list, keys):
    vector_list = list()
    for vector_dict in attack_vector_list:
        bow = create_bag_of_word_from_attack_vector(vector_dict, keys)
        vector_list.append(bow)
    return vector_list

def create_bag_of_word_from_attack_vector(attack_vector, keys):
    bow_word = ''
    for key in keys:
        bow_word += helper.stem_and_lemmatize(attack_vector[key],isRemoveStopword=True) + ' '
    bag_of_word_list = list(bow_word.split())
    return bag_of_word_list

def get_cyber_object(sentence, attack_vectors):
    pos_tag_dict = get_stanford_pos_tag(sentence)
    filtered_vector = list()
    for attack_vector in attack_vectors:
        action_verb = attack_vector['what']
        if action_verb in list(pos_tag_dict.keys()):
            print('action_verb:',action_verb)
            verb_pos_tag = pos_tag_dict[action_verb]

            if verb_pos_tag.startswith('VB'):
                cyber_object = attack_vector['where'].split()
                new_cyber_object_list = list()
                for word in cyber_object:
                    if word in list(pos_tag_dict.keys()):
                        pos_tag = pos_tag_dict[word]
                        if pos_tag.startswith('NN'):
                            new_cyber_object_list.append(word)
                cyber_object = ' '.join(new_cyber_object_list)
                attack_vector['where'] = cyber_object
                filtered_vector.append(attack_vector)
    return filtered_vector

from nltk import sent_tokenize, word_tokenize, pos_tag
def get_ntlk_post_tag_dict(sentence):
    postag_dict = {}
    list = pos_tag(word_tokenize(sentence))
    for tag in list:
        key = tag[0]
        val = tag[1]
        postag_dict[key] = val
    print(postag_dict)
    return postag_dict

def get_stanford_pos_tag(sentence):
    output = configuration.model_STANFORD.annotate(sentence, properties={'annotators': 'pos','outputFormat': 'json'})
    tokens = output['sentences'][0]['tokens']
    pos_tag_dict = dict()
    for token in tokens:
        word = token['word']
        pos = token['pos']
        pos_tag_dict[word] = pos
    # print(pos_tag_dict)
    return pos_tag_dict

def isVerbExistInPostTag(sentence):
    pos_tag_dict = get_stanford_pos_tag(sentence)
    tags = list(pos_tag_dict.values())
    if len(tags) == 1:
        print('Pos tag len 1. Obviously NNN. No Verb.')
        return False
    for tag in tags:
        if tag.startswith('VB'):
            print('POS TAG VB')
            return True
    print('NO POS TAG VB Found.')
    return False

def get_stanford_pos_tag(sentence):
    output = configuration.model_STANFORD.annotate(sentence, properties={'annotators': 'pos','outputFormat': 'json'})
    tokens = output['sentences'][0]['tokens']
    pos_tag_dict = dict()
    for token in tokens:
        word = token['word']
        pos = token['pos']
        pos_tag_dict[word] = pos
    # print(pos_tag_dict)
    return pos_tag_dict

def hasSubject(sentence):
    output = configuration.model_STANFORD.annotate(sentence, properties={'annotators': 'depparse','outputFormat': 'json'})
    # print(output['sentences'][0].keys())
    basicDependencies = output['sentences'][0]['basicDependencies']
    for dep in basicDependencies:
        if 'nsubj' in dep['dep']:
            return True
    return False

if __name__ == '__main__':
    while True:
        text = str(input('Enter: '))
        hasSubject(text)