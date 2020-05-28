import helper
# files = ['ontology/cyber_object_list.txt']#, 'ontology/UniqueALLCyberObjects_Ghaith.txt']
# cyber_object_files = ['ontology/cyber_object_list.txt', 'ontology/Symantec_objs_LIMITED_IOC.txt']
cyber_object_files = [
    'ontology/cyber_object_list.txt',
    'ontology/Symantec_objs_LIMITED_IOC.txt',
    'ontology/UniqueALLCyberObjects_Ghaith.txt'
]

# files = ['ontology/example_action_where.txt']#, 'ontology/UniqueALLCyberObjects_Ghaith.txt']
# output_file = 'ontology/cyber_object_from_examples.txt'
output_file = 'ontology/combined_cyber_object.txt'

def combine_cyber_object(files=cyber_object_files):
    text = ''
    for file in files:
        text += helper.read_file(file) + '\n'
    text = text.split('\n')
    dict_cyber = dict()
    for tt in text:
        tt = tt.translate(str.maketrans('', '', '!"#$%&\()*+,.:;<=>?@[\\]^_`{|}~')).lower()
        key = helper.stem_and_lemmatize(tt, isRemoveStopword=True)
        dict_cyber[key] = helper.remove_stopwords(tt)
    what_list = list(set(list(dict_cyber.values())))
    what_list.sort()
    # for __ in what_list:
    #     print(__)
    # print(len(what_list))
    helper.write_file(output_file, what_list)
    return


def ___(file):
    text = helper.read_file(file)
    text = text.split('\n')
    length = int(len(text)/4)
    for i in range(0,4):
        helper.write_file(file+'_'+str(i), text[i*length:(i+1)*length+1])


def sort_file(file_name='ontology/cyber_object_list.txt'):
    text = helper.read_file(file_name)
    text_list = list(set(text.split('\n')))
    text_list.sort()
    helper.write_file(file_name,text_list)

import nltk
import AllenNLP
import configuration
import os
from os import listdir
from os.path import isfile, join
def readfile(file_name):
    sent_list = helper.read_file(file_name)
    sent_list = sent_list.split('\n')
    final_sent_list = list()
    for sent in sent_list:
        sent_tokenize = nltk.sent_tokenize(sent)
        for sentence in sent_tokenize:
            # print(sentence)
            final_sent_list.append(sentence)
    return final_sent_list

def cyber_object_miner(file_name):
    sents = readfile(file_name)
    cyber_objects_words = list()
    cyber_objects_arg1 = list()
    action_verbs = list()
    for sentence in sents:
        extraction_list = list()
        try:
            predict = configuration.model_AllenNLP_SRL.predict(sentence=sentence)
            if len(predict['verbs']) == 0:
                # print('AllenNLP can not extract: ', sentence)
                cyber_objects_words.append(helper.remove_stopwords(sentence))
            else:
                for extractions in predict['verbs']:
                    verb = extractions['verb']
                    # checking from the verb_list
                    # print(verb)
                    action_verbs.append(verb)
                    # if helper.is_dictionay_key(configuration.preprocessOntologies.verb_dict,
                    #                            configuration.stemmer.stem(verb)):
                    description = extractions['description']
                    # print('description:',description)
                    # # print(description)
                    single_extraction_dict = AllenNLP.process_single_AllenNLP_description(description)
                    extraction_list.append(single_extraction_dict)
                extraction_list = AllenNLP.analyze_whole_sentence(extraction_list)
                extraction_list = AllenNLP.delete_extra_args(extraction_list)
                # print(single_extraction_dict)
                for single_extraction_dict in extraction_list:
                    try:
                        cyber_objects_arg1.append(helper.remove_stopwords(single_extraction_dict['where']))
                    except:
                        pass
                        # print('ARG1 not predent')
        except:
            pass

    return cyber_objects_arg1, cyber_objects_words, action_verbs

def process_all_symantec(infile):
    onlyfiles = [os.path.join(infile,f) for f in listdir(infile) if isfile(join(infile, f))]
    count_files = 0
    for file in onlyfiles:
        count_files += 1
        try:
            args, words, verbs = cyber_object_miner(file)
            helper.write_file('ontology/Cyber_Object_Miner/arg1_all.txt',args,mode='a+')
            helper.write_file('ontology/Cyber_Object_Miner/ioc_all.txt',words,mode='a+')
            helper.write_file('ontology/Cyber_Object_Miner/verbs_all.txt',verbs,mode='a+')
            # print(os.path.join(outfile,file[file.find('\\')+1:file.rfind('.')]+'.csv'))
            if count_files % 250 == 0:
                print('Already Processed:',count_files)
                try:
                    sort_file('ontology/Cyber_Object_Miner/arg1_all.txt')
                    sort_file('ontology/Cyber_Object_Miner/ioc_all.txt')
                    sort_file('ontology/Cyber_Object_Miner/verbs_all.txt')
                except:
                    print('Error while sorting:', count_files)
        except:
            print('Error Processinf File:', file, ':', count_files)

if __name__ == '__main__':
    # combine_cyber_object()
    # ___(output_file)
    # process_all_symantec('C:\\Users\\rrahman3\\PycharmProjects\\TTPSense_Git\\scrapper\\symantec_only_descryption\\')
    # sort_file('ontology/Cyber_Object_Miner/arg1_all.txt')
    # sort_file('ontology/Cyber_Object_Miner/ioc_all.txt')
    # sort_file('ontology/Cyber_Object_Miner/verbs_all.txt')
    sort_file('ontology/Symantec_objs_LIMITED_IOC.txt')
