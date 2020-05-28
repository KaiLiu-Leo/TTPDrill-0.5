# from utilities import FileReader
import configuration
from relation_miner import relation_miner
from ontology_reader import ReadOntology
from BM25 import BM25, BM25L, BM25Okapi, BM25Plus



def getOntology(isStemmer):
    from ontology_reader import ReadOntology
    file_name = 'resources/ontology_details.csv'
    ontology = ReadOntology()
    ontology_df = ontology.read_csv(file_name)
    ontology_dict = ontology.data_frame.to_dict('records')
    __ = ontology.split_ontology_list(ontology_dict)
    what_list = list()
    for i in __:

        what_list.append([i['Id'], i['action_what'], i['action_where'], i['why_what'], i['why_where']])
#    print(what_list[0])
    # list_map_dict is the mapping for ontology to mitre t value
    what_list, list_map_dict = combine_parsed_ontology_in_bow(what_list,isStemmer)
    ttp_df = ontology.read_mitre_TTP()
    # for key, val in ttp_df.items():
    #     print(key, val['TECHNIQUE'] )
    # print(ttp_df)



    # file_name = 'resources/ontology_details_1.csv'
    # file_name = 'resources/ontology_details.csv'
    # file_name = 'resources/export_dataframe.csv'
    # ontology = ReadOntology()
    # ontology_df = ontology.read_csv(file_name)
    # ontology_dict = ontology.refine_ontology()
    # stem_list = ontology.stem()
    # # for ont  in stem_list:
    # #     print(ont['action_what'])
    # ontology.print_ontology(stem_list)
    #
    #
    #
    # what_list = list()
    # for i in stem_list:
    #     what_list.append([i['Id'], i['action_what'], i['action_where']])
    # #what_list[0]

    return what_list, list_map_dict, ttp_df

def combine_parsed_ontology_in_bow(what_list, isStemmer):
    list_map_dict = dict()
    new_list = list()
    for index in enumerate(what_list):
        a = list()
        for attribute in index[1]:
            if type(attribute) is str:
                a.append(attribute.strip())
            elif type(attribute) is list:
                for each_sttribute in attribute:
                    for each_word in each_sttribute.split(' '):
                        if isStemmer:
                            a.append(stemmer.stem(each_word.strip()))
                        else:
                            a.append(lemmatizer.lemmatize(each_word.strip()))
        a = helper.remove_stopwords(a)
        list_map_dict[index[0]] = a[0]
        new_list.append(a[1:])

    return new_list, list_map_dict




from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()
import helper




# working with separated ontology


# def read_API_doc():
#     import pandas
#     api_data_frame = pandas.read_csv('resources/API_Description_MSDN.csv', encoding="ISO-8859-1")
#     return api_data_frame.to_dict('records')
#
# def main():
#
#     isAPI = False
#
#
#     """----------------------------------------------------------------------------------------"""
#     ### Building Ontology
#     isStemmer = True
#     what_list, list_map, ttp_df = getOntology(isStemmer)
#     # what_list, list_map, ttp_df = getGhaithOntology(isStemmer)
#     bm25_model = BM25Okapi(what_list)
#     """-----------------------------------------------------------------------------------------"""
#
#
#
#
#     if isAPI:
#         api_dict_list = read_API_doc()
#         print("----------------------------------------------------------------------------------------")
#         for api in api_dict_list:
#             # for key, val in api.items():
#             print("-----------------------------------" + api['API_NAME'] + "-----------------------------------")
#             print('API_NAME: ', api['API_NAME'])
#             print('API_Description: ', api['API_Description'])
#             extracted_list = getReportExtraction(False, True, True,  api['API_Description'])
#             query(extracted_list, what_list, list_map, bm25_model, ttp_df)
#
#             print("-----------------------------------" + api['API_NAME'] + "-----------------------------------\n\n")
#
#     else:
#
#         isFile = True
#
#         #while(True):
#         if isFile:
#             report_name = 'scrapper/only_description/Trojan.Mdrop.BWJ.2008-102219-5606-99.txt'
#             # report_name = 'C:\\Users\\rrahman3\\Google Drive\\Study UNCC\\TTPDrill Handover\\Raw Threat Reports\\ThreatReport\\relevent\\Infostealer.Alina_ThreatReport.txt'
#             # report_name = 'C:\\Users\\rrahman3\\Google Drive\\Study UNCC\\TTPDrill Handover\\Raw Threat Reports\\ThreatReport\\ghaith\\tested_output\\Trojan.Downexec.B_ThreatReport.txt'
#
#         else:
#             report_name = input("Enter Text:\t")
#         extracted_list = getReportExtraction(isFile, True, True, report_name)
#         # print(what_list)
#         query(extracted_list,what_list,list_map, bm25_model, ttp_df)
#
#
# def combine_reports(infile='test_reports', outfile='combined_reports_evaluated.txt'):
#     import os
#     from os import listdir
#     from os.path import isfile, join
#     onlyfiles = [os.path.join(infile,f) for f in listdir(infile) if isfile(join(infile, f))]
#     text = ''
#
#     for file in onlyfiles:
#         text += '-'*50+'\n'
#         text += file + '\n'
#         text += '-'*50+'\n'
#         with open(file,'r') as f:
#             text += f.read() + '\n'
#         text += '-'*50 + '\n'
#     with open(outfile,'w') as f:
#         f.write(text)
#     return

from mapModule import process_directory
from mapModule import query
from mapModule import getReportExtraction

import Example_Ontology
'''
document = 'Lazarus Group keylogger KiloAlfa obtains user tokens from interactive sessions to execute itself with API call CreateProcessAsUserA under that user\'s context.'
{
    'top_spans': [[0, 1], [0, 3], [3, 3], [11, 11], [12, 12], [14, 14], [16, 16], [18, 20], [18, 21]], 
    'predicted_antecedents': [-1, -1, -1, -1, 3, 3, -1, -1, -1], 
    'document': ['Lazarus', 'Group', 'keylogger', 'KiloAlfa', 'obtains', 'user', 'tokens', 'from', 'interactive', 'sessions', 'to', 'execute', 'itself', 'with', 'API', 'call', 'CreateProcessAsUserA', 'under', 'that', 'user', "'s", 'context', '.'], 
    'clusters': [[[0, 1], [12, 12]], [[0, 3], [14, 14]]]}
'''

def coref_test():
    predictor = configuration.model_AllenNLP_Coref
    documents = [
        'Lazarus Group keylogger KiloAlfa obtains user tokens from interactive sessions to execute itself with API call CreateProcessAsUserA under that user\'s context.',
        'HiddenWasp installs reboot persistence by adding itself to /etc/rc.local.'
    ]
    for sent in documents:
        result = predictor.predict(document=sent)
        document = result['document']
        top_spans = result['top_spans']
        predicted_antecedents = result['predicted_antecedents']
        clusters = result['clusters']

        print(result)


import coreference
if __name__=='__main__':
    # main()
    # seperated_ontology(False)
    # start_core_nlp_server()
    # process_directory('test_reports/Ransom.PowerWare.B.2016-072210-0220-99.txt')
    # process_directory('reposts/msdn_descryption.txt', 'reports')
    # process_directory('test_reports/Backdoor.Avubot.2015-121611-5748-99.txt')
    # process_directory('reports/test.txt')
    # test_map()
    # process_directory()
    import time
    start_time = time.time()
    import AllenNLP, mapModule
    from AllenNLP import get_Allen_NLP_Extraction
    # text = coreference.coref_text_with_files(configuration.model_AllenNLP_Coref,file_name='reports/infostealer_test.txt')
    # process_directory('reports/infostealer_test.txt', 'analysis_ttpsense/infostealer_test_1.csv')
    # process_directory('test_reports/Backdoor.Avubot.2015-121611-5748-99.txt')
    # process_directory('test_reports/old_version/Ransom.PowerWare.2014-060513-1113-99.txt','test_reports/old_version_output/Ransom.PowerWare.2014-060513-1113-99.csv')
    # contributors = ['Ruhani','Moumita','Qi Duan','Mohiuddin','Rawan']
    # contributors = ['Moumita']
    # for contributor in contributors:
    #     process_directory('C:\\Users\\rrahman3\\Google Drive\\TTPSense_Evaluation\\Symantec Evaluation\\Contributors\\'+contributor+'\\raw_data_1',
    #                       'C:\\Users\\rrahman3\\Google Drive\\TTPSense_Evaluation\\Symantec Evaluation\\Contributors\\'+contributor+'\\raw_data_output_new_1')
    # process_directory(
    #     'C:\\Users\\rrahman3\\Google Drive\\TTPSense_Evaluation\\Symantec Evaluation\\Contributors\\Moumita\\raw_data_1\\Backdoor.Krademok.2011-121417-0311-99.txt',
    #     'C:\\Users\\rrahman3\\Google Drive\\TTPSense_Evaluation\\Symantec Evaluation\\Contributors\\Moumita\\raw_data_output_new_1\\Backdoor.Krademok.2011-121417-0311-99_1.csv')


    # process_directory('C:\\Users\\rrahman3\\Google Drive\\TTPSense_Evaluation\\Symantec Evaluation\\Contributors\\Moumita\\raw_data',
    #                   'C:\\Users\\rrahman3\\Google Drive\\TTPSense_Evaluation\\Symantec Evaluation\\Contributors\\Moumita\\raw_data_output')
    # process_directory('test_reports/Symantec_Evaluation_Reports','test_reports/Symantec_Evaluation_Reports_Results')
    # process_directory('reports/test.txt','reports/Infostealer.Kuang.B.csv')
    # process_directory(
    #     'C:\\Users\\rrahman3\\PycharmProjects\\ttpsense\\test_reports\\only_description\\Infostealer\\Infostealer.Atesla.2016-083012-3504-99.processed',
    #     'C:\\Users\\rrahman3\\PycharmProjects\\ttpsense\\test_reports\\only_description\\ruhani_test\\Infostealer.Atesla.2016-083012-3504-99.csv'
    # )
    # process_directory(
    #     'C:\\Users\\rrahman3\\Google Drive\\TTPSense_Evaluation\\Symantec Evaluation\\AllSymantecReports\\Infostealer\\Infostealer.Banker.H.2010-070313-2338-99.processed',
    #     'C:\\Users\\rrahman3\\Google Drive\\TTPSense_Evaluation\\Symantec Evaluation\\AllSymantecReports\\Infostealer.Banker.H.2010-070313-2338-99.csv'
    # )
    # process_directory(
    #     'C:\\Users\\rrahman3\\Google Drive\\TTPSense_Evaluation\\Symantec Evaluation\\AllSymantecReports\\Infostealer\\Infostealer.ABCHlp.2003-060511-5140-99.processed',
    #     'C:\\Users\\rrahman3\\Google Drive\\TTPSense_Evaluation\\Symantec Evaluation\\AllSymantecReports\\test_1.csv'
    # )
    process_directory('reports/test.txt','reports/test_3.csv')
    # process_directory('C:\\Users\\rrahman3\\PycharmProjects\\ttpsense\\test_reports\\only_description\\ruhani_test',
    #                   'C:\\Users\\rrahman3\\PycharmProjects\\ttpsense\\test_reports\\only_description\\ruhani_test\\new_output')
    # mapModule.seperated_ontology(configuration.preprocessOntologies, report_name='reports/test.txt')
    # process_directory('reports/talos_fin7.txt','reports/talos_fin7.csv')
    # process_directory('test_reports/Symantec_Evaluation_Reports','test_reports/Symantec_Evaluation_Reports_Results')
    # process_directory('test_reports/Symantec_Evaluation_Reports/Backdoor.Cimuz.2011-071502-1007-99.txt','test_reports/Symantec_Evaluation_Reports_Results/Backdoor.Cimuz.2011-071502-1007-99.csv')
    # process_directory('test_reports/new_version','test_reports/new_version_output')
    # ttpsense_output_dict_list = mapModule.mitre_mapping_with_new_ontology(configuration.extracted_list, configuration.preprocessOntologies)
    # mapModule.print_output(ttpsense_output_dict_list, 'analysis_ttpsense/fin_7_mapping_test.csv')
    # process_directory('reports/extraction_test.txt', 'analysis_ttpsense/extraction_test_6.csv')
    # process_directory('test_reports/Symantec_Evaluation_Reports/Backdoor.Duuzer.2015-082113-4423-99.txt', 'test_reports/Backdoor.Duuzer.2015-082113-4423-99_2.csv')
    # process_directory('reports/test.txt', 'analysis_ttpsense/fin_analysis_with_example_ontology_5.csv')
    # text = coreference.coref_text_with_files(configuration.model_AllenNLP_Coref,file_name='scrapper/simplified_symentec_reports/Infostealer.Spamnost.2011-121917-3758-99.txt')
    # list = get_Allen_NLP_Extraction(predictor=configuration.model_AllenNLP_SRL, isFile=False, isLemmatize=True, isStem=True, isSymantecReport=False, isFileWrite=True, file_name=text)
    # list = get_Allen_NLP_Extraction(predictor=configuration.model_AllenNLP_SRL, isFile=True, isLemmatize=True, isStem=True, isSymantecReport=False, isFileWrite=True, file_name='reports/test.txt')
    # AllenNLP.print_extraction(list)
    end_time = time.time()
    print('Time: ', (end_time-start_time))
    # testFuncNew()
    # combine_reports()

    # Example_Ontology.main()
    # coref_test()

