from AllenNLP import get_Allen_NLP_Extraction
import configuration
from helper import FileReader
from relation_miner import relation_miner
from BM25 import BM25Okapi
import preProcessTool

def getReportExtraction(isFile=True, isLemmatize=True, isStem=True, file_name = 'reports/fireeye_fin7_application_shimming.txt'):

    preprocess_tools = FileReader(file_name)
    # text_list = list of str, contains valid sentences with no fullstop or file path with them
    if isFile:
        text = preprocess_tools.read_file()
        # text = text.replace('\n',' ')
        text_list = preprocess_tools.get_all_valid_sentences(text)
    else:
        text = file_name
        text_list = preprocess_tools.get_all_valid_sentences(text)
    # print(text_list)

    # # Start NLP Server
    stanfordNLP = configuration.model_STANFORD
    r_miner = relation_miner(stanfordNLP)

    extracted_infor_list = r_miner.all_imp_stuff(text_list)
    extracted_list = get_all(extracted_infor_list, isLemmatize, isStem)

    return extracted_list

def get_all(temp_list, isLmmatize=True, isStem=True):
    from ontology_reader import utilities as util
    util_stemmer = util()
    all_list = list()
    for temp_dict in temp_list:
        all_dict = dict()
        tt_list = list()
        for key, val in temp_dict.items():
            if key == 'what' or key == 'where' or key == 'where_attribute' or key == 'why' or key == 'when' or key == 'how' or key == 'subject':
                for __ in val:
                    tt_list.append(util_stemmer.lemmatize_and_stem(__.lower(), isLmmatize, isStem))
        all_dict['text'] = temp_dict['text']
        all_dict['bow'] = set(tt_list)
        all_list.append(all_dict)
    return all_list


"""
    ...Important Methods...
"""
def query(extracted_list, ontology_list, list_map, bm25_model):
    # print('------------------------',extracted_list)
    for tokenized_query in extracted_list:
        # print('bag_of_word:',tokenized_query)
        top_index, match_ttp, score = bm25_model.get_top_n(tokenized_query, ontology_list, n=configuration.top_n)
        ttp_id = [list_map[index] for index in top_index]
        # print(ttp_id)
        # print(score)
    return zip(top_index, match_ttp, score, ttp_id)

# what contains zip(top_index, match_ttp, score, ttp_id)
# ttp_id is for mapping to the matched result
def find_max_map(what_why_how_list):
    import numpy as np
    result_list = list()
    for i in what_why_how_list:
        for each_result in i:
            result_list.append(each_result)
    # print('result_list: ', result_list)
    scores = [x[2] for x in result_list]
    # print('soces: ', scores)
    top_n = np.argsort(scores)[::-1]
    # top_n = np.argsort(scores)[::-1][:configuration.top_n]
    print(top_n)
    return top_n, result_list

def select_best_match(ttp_df, tokenized_query, mapped_list, what_why_how_list,sentence):
    isFirstTime = True
    # print('top_n: ', top_n)
    top_n, result_list = find_max_map(what_why_how_list)

    ttpsense_output_dict_new = dict()
    ttpsense_output_dict_new['text'] = sentence
    ttpsense_output_dict_new['bow'] = tokenized_query

    temp_list = list()

    ttp_df_unique_dict = dict()
    for i in top_n:

        matched_entity = result_list[i]
        # try:
        ttp_index = matched_entity[0]
        ttp_id = matched_entity[3]

        if ttp_id not in list(ttp_df_unique_dict.keys()):

            ttp_df_unique_dict[ttp_id] = '1'
            try:
                ttp_technique = ttp_df[ttp_id]['TECHNIQUE']
                ttp_tactic = ttp_df[ttp_id]['TACTIC']
            except:
                ttp_technique = '_'
                ttp_tactic = '_'
            ttp_ontology = matched_entity[1]
            ttp_score = matched_entity[2]

            # isFirstTime = False
            # else:
            #     ttpsense_output_dict['bow'] = ''
            ttpsense_output_dict = dict()
            if (ttp_score >= configuration.BM25_THRESHOLD):

                ttpsense_output_dict['ttp_index']=ttp_index
                ttpsense_output_dict['ttp_score']=ttp_score
                ttpsense_output_dict['ttp_id']=ttp_id
                ttpsense_output_dict['ttp_technique']=ttp_technique
                ttpsense_output_dict['ttp_tactic']=ttp_tactic
                ttpsense_output_dict['ttp_ontology']=ttp_ontology
                print(ttp_index, ' : ', ttp_score, ' : ', ttp_id, ' : ', ttp_technique, ' : ', ttp_tactic, ' : ', ttp_ontology)
                # temp_list.append(ttpsense_output_dict)
                # mapped_list.append(ttpsense_output_dict)

            else:
                ttpsense_output_dict['ttp_index'] = '_'
                ttpsense_output_dict['ttp_score'] = '_'
                ttpsense_output_dict['ttp_id'] = '_'
                ttpsense_output_dict['ttp_technique'] = '_'
                ttpsense_output_dict['ttp_tactic'] = '_'
                ttpsense_output_dict['ttp_ontology'] = '_'
                print(ttp_index, ' : ', ttp_score, ' : ', ttp_id, ' : ', ttp_technique, ' : ', ttp_tactic, ' : ',ttp_ontology)
                # temp_list.append(ttpsense_output_dict)
                # mapped_list.append(ttpsense_output_dict)

            temp_list.append(ttpsense_output_dict)

        # except:
        #     print('None')
    ttpsense_output_dict_new['map'] = temp_list
    mapped_list.append(ttpsense_output_dict_new)
    return
import coreference
def seperated_ontology(preprocessOntologies, isDependencyParser = configuration.isDependencyParser, isGhaithOntology=configuration.isGhaithOntology, isFile=configuration.isFile, report_name = 'reports/test.txt'):


    configuration.prev_verb = ''
    configuration.prev_subject = ''
    configuration.prev_object = ''
    configuration.prev_sentence = ''
    if isDependencyParser:
        # {'text': 'Mandiant identified that the group leveraged an application shim database to achieve persistence on systems in multiple environments.', 'bow': ['group', 'system', 'leverag', 'identifi', 'applic', 'mandiant', 'databas', 'shim', 'environ', 'achiev', 'persist']}
        extracted_list = getReportExtraction(file_name=report_name, isFile=configuration.isFile, isLemmatize=configuration.isLemmatize, isStem=configuration.isStem)
    else:
        extracted_list = get_Allen_NLP_Extraction(configuration.model_AllenNLP_SRL, file_name=report_name, isFile=configuration.isFile, isLemmatize=configuration.isLemmatize, isStem=configuration.isStem, isFileWrite=False)
        # extracted_list = get_Allen_NLP_Extraction(preprocessOntologies.predictor, file_name=report_name, isFile=configuration.isFile, isLemmatize=configuration.isLemmatize, isStem=configuration.isStem, isFileWrite=False)
    print('-----------------------Extracted list---------------------\n',extracted_list)
    # extracted_list is a list of dictionary contains 2 keys, text and bow, bow is a list of lists.
    # extracted_list = [{text:text,bow:[[bow],[bow]]}, {text:text,bow:[[bow],[bow]]}]
    # {'text':sentence, 'bow':[['ole','embed','object'],...], 'compact_vector':[{'what': 'embedded', 'where': 'OLE object', 'why': '', 'how': '', 'when': ''},...]}}

    if isGhaithOntology:
        ttpsense_output_dict_list = mitre_mapping_with_ghaith_ontology(extracted_list, preprocessOntologies)
    else:
        # ttpsense_output_dict_list = mitre_mapping_with_new_ontology(extracted_list, preprocessOntologies)
        ttpsense_output_dict_list = test_with_new_algorithm(extracted_list, preprocessOntologies)

    return ttpsense_output_dict_list

import dictionary_based_ontology, helper
action_dictionary = dictionary_based_ontology.create_cyber_object_dictionary_based_ontology(file_name='ontology/refined_what_where.csv')
# action_dictionary = dictionary_based_ontology.create_cyber_object_dictionary_based_ontology(file_name='ontology/ontoloy_example_description.csv')
# why_ontology = helper.read_csv_file(file_name='ontology/new/refined_why.csv')
why_dictionary = dictionary_based_ontology.create_ttp_id_based_ontology(file_name='ontology/refined_why.csv')
how_dictionary = dictionary_based_ontology.create_ttp_id_based_ontology(file_name='ontology/refined_how.csv')
mitre = dictionary_based_ontology.match_mitre(action_dictionary, why_dictionary, how_dictionary)
# while True:
# <class 'dict'>:
# {
#   'text': 'the trojan may arrive on the compromised computer after being downloaded by other threats .',
#   'map':
#   [
#       {
#           'text': 'the trojan may arrive on the compromised computer after being downloaded by other threats .',
#           'bow': {'what': 'compromised', 'where': 'computer', 'why': '', 'how': '', 'when': ''},
#           'map':
#           [
#               {'ttp_index': 4112, 'ttp_score': 11.284904876233238, 'ttp_id': 't1059', 'ttp_technique': 'Command-Line Interface', 'ttp_tactic': 'Execution', 'ttp_ontology': ['compromis', 'comput']},
#               {'ttp_index': 4262, 'ttp_score': 11.284904876233238, 'ttp_id': 't1005', 'ttp_technique': 'Data from Local System', 'ttp_tactic': 'Collection', 'ttp_ontology': ['compromis', 'comput']}
#           ]
#       }
#   ]
# }
def test_with_new_algorithm(extracted_list, preprocessOntologies):
    ttpsense_output_dict_list = list()
    for each_extraction in extracted_list:
        text = each_extraction['text']
        bow_list = each_extraction['bow']
        # attack_vector_list = each_extraction['attack_vector']
        attack_vector_list = each_extraction['compact_vector']
        ttpsense_output_dict = dict()
        ttpsense_output_dict['text'] = text
        mapped_list = list()
        print('')
        print('Text:\n', text, '\n')
        for tokenized_query in zip(bow_list,attack_vector_list):
            print('Bag of Word: ',tokenized_query[0])
            print('Attack Vector: ',tokenized_query[1])
            if tokenized_query[1]['what'].startswith('perform') and tokenized_query[1]['what'].startswith('action'):
                continue

            mapped_mitre_techniques_list = mitre.matching_algorithm(tokenized_query[1])
            temp_dict = dict()
            temp_dict['text'] = text
            temp_dict['bow'] = tokenized_query[1]
            temp_dict_map_list = list()
            for ttp in mapped_mitre_techniques_list:
                try:
                    ddict = {'ttp_index': 0, 'ttp_score': 20, 'ttp_id': ttp, 'ttp_technique': mitre.ttp_df[ttp]['TECHNIQUE'], 'ttp_tactic': mitre.ttp_df[ttp]['TACTIC'], 'ttp_ontology': ['NA']}
                    temp_dict_map_list.append(ddict)
                except:
                    ddict = {'ttp_index': 0, 'ttp_score': 10, 'ttp_id': ttp, 'ttp_technique': 0, 'ttp_tactic': 0, 'ttp_ontology': ['NA']}
                    temp_dict_map_list.append(ddict)
            temp_dict['map'] = temp_dict_map_list
                # print(ttp, ':', helper.get_technique_and_tactic(ttp, mitre.ttp_df))
            mapped_list.append(temp_dict)

        ttpsense_output_dict['map'] = mapped_list
        ttpsense_output_dict_list.append(ttpsense_output_dict)
    # print_output(ttpsense_output_dict_list, report_name)
    return ttpsense_output_dict_list



import helper
# {'text':sentence, 'bow':['ole','embed','object'], 'attack_vector':{'what': 'embedded', 'where': 'OLE object', 'why': '', 'how': '', 'when': ''}, 'compact_vector':{'what': 'embedded', 'where': 'OLE object', 'why': '', 'how': '', 'when': ''}}}
def mitre_mapping_with_new_ontology(extracted_list, preprocessOntologies):

    ttpsense_output_dict_list = list()
    # print(preprocessOntologies.preprocessed_ontology[5][1])
    for each_extraction in extracted_list:
        text = each_extraction['text']
        bow_list = each_extraction['bow']
        # attack_vector_list = each_extraction['attack_vector']
        attack_vector_list = each_extraction['compact_vector']
        ttpsense_output_dict = dict()
        ttpsense_output_dict['text'] = text
        mapped_list = list()
        print('')
        print('Text:\n', text, '\n')
        for tokenized_query in zip(bow_list,attack_vector_list):
            print('Bag of Word: ',tokenized_query[0])
            print('Attack Vector: ',tokenized_query[1])
            if tokenized_query[1]['what'].startswith('perform') and tokenized_query[1]['what'].startswith('action'):
                continue
            # print('where', [tokenized_query[1]['where']])

            # bm25_model, tokenized_corpus, ttp_id, bow_mapped

            # TFIDF Match.
            result_what_where = query([tokenized_query[0]], configuration.tokenized_corpus, configuration.ttp_id, configuration.bm25_model)
            select_best_match(preprocessOntologies.ttp_df, tokenized_query[1], mapped_list, [result_what_where], text)


            # result_what_where = query([tokenized_query[0]], preprocessOntologies.preprocessed_ontology[2][1], preprocessOntologies.bm25_what_where_map, preprocessOntologies.bm25_what_where)
            # select_best_match(preprocessOntologies.ttp_df, tokenized_query[1], mapped_list, [result_what_where])


            # bow_what = utilities.stem_and_lemmatize(tokenized_query[1]['what']).split()
            # result_what = query([bow_what], preprocessOntologies.preprocessed_ontology[4][1], preprocessOntologies.bm25_what_where_map, preprocessOntologies.bm25_what_where)
            # select_best_match(preprocessOntologies.ttp_df, tokenized_query[1], mapped_list, [result_what])
            #
            # bow_where = utilities.stem_and_lemmatize(tokenized_query[1]['where']).split()
            # result_where = query([bow_where], preprocessOntologies.preprocessed_ontology[5][1], preprocessOntologies.bm25_what_where_map_where, preprocessOntologies.bm25_what_where_where)
            # select_best_match(preprocessOntologies.ttp_df, tokenized_query[1], mapped_list, [result_where])

            # print('-'*100,'WHY','-'*100)
            # result_why = query([tokenized_query[0]], preprocessOntologies.preprocessed_ontology[1][1], preprocessOntologies.bm25_why_map, preprocessOntologies.bm25_why)
            # print('-'*100,'HOW','-'*100)
            # result_how = query([tokenized_query[0]], preprocessOntologies.preprocessed_ontology[0][1], preprocessOntologies.bm25_how_map, preprocessOntologies.bm25_how)
            # select_best_match(preprocessOntologies.ttp_df, tokenized_query[1], mapped_list, [result_what_where])
            # select_best_match(preprocessOntologies.ttp_df, tokenized_query[1], mapped_list, [result_what_where, result_why, result_how])
        ttpsense_output_dict['map'] = mapped_list
        ttpsense_output_dict_list.append(ttpsense_output_dict)
    # print_output(ttpsense_output_dict_list, report_name)
    return ttpsense_output_dict_list

def mitre_mapping_with_ghaith_ontology(extracted_list, preprocessOntologies):
    ttpsense_output_dict_list = list()
    for each_extraction in extracted_list:
        text = each_extraction['text']
        bow_list = each_extraction['bow']
        # print(each_extraction)
        # print('-'*100,'WHAT_WHERE','-'*100)
        ttpsense_output_dict = dict()
        ttpsense_output_dict['text'] = text
        mapped_list = list()
        print('')
        print('Text:\n', text, '\n')
        for tokenized_query in bow_list:
            print('%'*100,tokenized_query)
            print(len(tokenized_query))
            print('-'*100,'WHAT','-'*100)
            result_what_where = query([tokenized_query], preprocessOntologies.bm25_what_where_list, preprocessOntologies.bm25_what_where_map, preprocessOntologies.bm25_what_where)
            select_best_match(preprocessOntologies.ttp_df,tokenized_query, mapped_list, [result_what_where])
        ttpsense_output_dict['map'] = mapped_list
        ttpsense_output_dict_list.append(ttpsense_output_dict)

        """
        ttpsense_output_dict = {
                'text':''
                'map': [
                        {
                            'bow': {
                                        'what':what,
                                        'where':where,
                                        'why':why,
                                        'how':how,
                                        'when':when
                                    }
                            'ttp_index':ttp_index
                            'ttp_score':ttp_score
                            'ttp_id':ttp_id
                            'ttp_technique':ttp_technique
                            'ttp_tactic':ttp_tactic                    
                            'ttp_ontology':ttp_ontology
                        }
                    ],...
            }
        """
    return ttpsense_output_dict_list
# <class 'dict'>:
# {
#   'text': 'the trojan may arrive on the compromised computer after being downloaded by other threats .',
#   'map':
#   [
#       {
#           'text': 'the trojan may arrive on the compromised computer after being downloaded by other threats .',
#           'bow': {'what': 'compromised', 'where': 'computer', 'why': '', 'how': '', 'when': ''},
#           'map':
#           [
#               {'ttp_index': 4112, 'ttp_score': 11.284904876233238, 'ttp_id': 't1059', 'ttp_technique': 'Command-Line Interface', 'ttp_tactic': 'Execution', 'ttp_ontology': ['compromis', 'comput']},
#               {'ttp_index': 4262, 'ttp_score': 11.284904876233238, 'ttp_id': 't1005', 'ttp_technique': 'Data from Local System', 'ttp_tactic': 'Collection', 'ttp_ontology': ['compromis', 'comput']}
#           ]
#       }
#   ]
# }

def create_output_map(output_map,text):
    csv_list = list()
    csv_header = ['Text','What','Where','Why','When','How','Technique','Tactic','MITRE ID','Ontology that matched','Score']
    csv_list.append(csv_header)
    # temp = ''
    # for i in text:
    #     temp += i + '\n'
    if text != '':
        csv_list.append([text])
    # csv_list.append(['\n'.join(text)])
    for single_map in output_map:
        # temp.append(map['text'])
        isFirst = True
        try:
            for single_match in enumerate(single_map['map']):
                # print(single_match.keys())
                # if single_match[0] % configuration.top_n == 0:

                isNewAction = True
                mapped_list = single_match[1]['map']
                if len(mapped_list) == 0:
                    temp = list()
                    if isFirst:
                        temp.append(single_map['text'])
                        isFirst = False
                    else:
                        temp.append('')
                    if isNewAction:
                        temp.append(single_match[1]['bow']['what'])
                        temp.append(single_match[1]['bow']['where'])
                        temp.append(single_match[1]['bow']['why'])
                        temp.append(single_match[1]['bow']['when'])
                        temp.append(single_match[1]['bow']['how'])
                        isNewAction = False

                    else:
                        temp.append('')
                        temp.append('')
                        temp.append('')
                        temp.append('')
                        temp.append('')

                    temp.append('NA')
                    temp.append('NA')
                    temp.append('NA')
                    csv_list.append(temp)

                else:
                    for mitre_map in mapped_list:
                        temp = list()
                        if isFirst:
                            temp.append(single_map['text'])
                            isFirst = False
                        else:
                            temp.append('')
                        if isNewAction:
                            temp.append(single_match[1]['bow']['what'])
                            temp.append(single_match[1]['bow']['where'])
                            temp.append(single_match[1]['bow']['why'])
                            temp.append(single_match[1]['bow']['when'])
                            temp.append(single_match[1]['bow']['how'])
                            isNewAction = False

                        else:
                            temp.append('')
                            temp.append('')
                            temp.append('')
                            temp.append('')
                            temp.append('')

                        temp.append(mitre_map['ttp_id'])
                        temp.append(mitre_map['ttp_technique'])
                        temp.append(mitre_map['ttp_tactic'])
                        # temp.append(mitre_map['ttp_ontology'])
                        # temp.append(mitre_map['ttp_score'])
                        # temp.append(single_match[1]['ttp_index'])
                        csv_list.append(temp)
        except:
            print('Error Happend...')
    return csv_list


def print_output(output_map,report_name,text):
    import csv
    csv_list = create_output_map(output_map,text)
    with open(report_name, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        for __ in csv_list:
            print(__)
            writer.writerow(__)
    return


import AllenNLP
def process_directory(infile='test_reports', outfile='test_outputs'):

    import os
    from os import listdir
    from os.path import isfile, join
    preprocessOntologies = configuration.preprocessOntologies
    if os.path.isfile(infile):
        text = helper.read_file(os.path.join(infile))
        result = seperated_ontology(preprocessOntologies, report_name=os.path.join(infile))
        # for mapped_mitre in result:
        #     print(mapped_mitre)
            # print('Text', mapped_mitre['text'])
            # for lists in mapped_mitre['map']:
            #     for key, val in lists.items():
            #         print(key, val)
            #     print('\n')
            # print('\n')
        # if not os.path.isdir(outfile):
        #     output_file_path = os.path.join(outfile, infile[infile.find('/')+1:infile.rfind('.')] + '_1.csv')
        # else:
        #     output_file_path = outfile
        print(outfile)
        print_output(result, outfile, text)
    else:
        onlyfiles = [f for f in listdir(infile) if isfile(join(infile, f))]
        for file in onlyfiles:
            print(file)
            if isfile(os.path.join(outfile,file[:file.rfind('.')]+'.csv')):
                print('Already Generated')
                continue
            # print(os.path.join(outfile,file[file.find('\\')+1:file.rfind('.')]+'.csv'))
            text = helper.read_file(os.path.join(infile, file))
            result = seperated_ontology(preprocessOntologies, report_name=os.path.join(infile,file))
            print_output(result, os.path.join(outfile,file[:file.rfind('.')]+'.csv'), text=text)
    return

from nltk import sent_tokenize, word_tokenize, pos_tag
def get_post_tag_dict(sen):
    postag_dict = {}
    list = pos_tag(word_tokenize(sen))
    for tag in list:
        key = tag[0]
        val = tag[1]
        postag_dict[key] = val
    return postag_dict


if __name__=='__main__':
    while True:
        text = str(input('Enter ')).lower()
        # 'the trojan may steal system information and send system information to a remote location'
        result = seperated_ontology(configuration.preprocessOntologies, report_name=text, isFile=False)
        for row in result:
            print(row)
            try:
                map = result['map']
                for lists in map:
                    for key, val in lists.items():
                        print(key,':',val)
            except:
                pass


