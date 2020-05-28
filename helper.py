import re, nltk, json, os
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.corpus import stopwords
import pandas
import regex_checker
stopword_lists = stopwords.words('english')
stopword_lists.append('-')
stopword_lists.append('some')

stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()



class FileReader():
    def __init__(self, file_name):
        self.file_name = file_name

    def read_file(self):
        with open(self.file_name,'r', encoding="utf8") as report:
            strs = report.read()
        self.text = strs.lower()
        # print(strs)
        return self.text

    def print_sentence(self, sent_list):
        for sent in enumerate(sent_list):
            print('Sentence ',sent[0],':',sent[1])
        return

    def get_all_sentences(self, text):
        sentence_tokenize_list = list()
        paragraphs = text.split('\n')
        for paragraph in paragraphs:
            sent_tokenize = nltk.sent_tokenize(paragraph)
            for sentence in sent_tokenize:
                sentence_tokenize_list.append(sentence)
        return sentence_tokenize_list

    # # Return the valid senteces only, Do not consider the topic sentence
    def get_all_valid_sentences(self, text):
        sentence_tokenize_list = list()
        paragraphs = text.split('\n')
        for paragraph in paragraphs:
            sent_tokenize = nltk.sent_tokenize(paragraph)
            for sentence in sent_tokenize:
                print(sentence)
                ###
                # if len(sentence) == sentence.rfind('.') + 1:
                    # sentence = self.remove_fullstop(sentence)
                sentence = self.remove_filepath(sentence)
                sentence = sentence.translate(str.maketrans('', '', '!"#$%&\()*+,.:;<=>?@[\\]^_`{|}~')).lower()
                sentence_tokenize_list.append(sentence)
        return sentence_tokenize_list

    def get_sent_tokenize(self, text):
        sentence_tokenize_list = list()
        sent_tokenize = nltk.sent_tokenize(text)
        for sentence in sent_tokenize:
            ###
            if len(sentence) == sentence.rfind('.') + 1:
                # sentence = self.remove_fullstop(sentence)
                sentence = self.remove_filepath(sentence)
                sentence_tokenize_list.append(sentence)
        return sentence_tokenize_list


    def remove_fullstop(self, text):
        """This method removes the fullstop in the middle of a sentence eg. 'services.exe' changes to 'servicesexe'."""
        """
        :parameter text str
        :return str
        """
        result_string = text.replace('.','',text.count('.')-1)
        return result_string

    # def remove_filepath(self, text):
    #     x = re.findall(r"([a-zA-Z]:[\\\\[a-zA-Z0-9]*]*)", text)
    #
    #     for _ in x:
    #         text = text.replace(_,'file path',1)
    #     x = re.findall(r'(\/.*?\.[\w:]+)',text)
    #     for _ in x:
    #         text = text.replace(_,'file path',1)
    #     return text

    def remove_filepath(self, text):
        # r'((((? < !\w)[A - Z, a - z]:) | (\.{1, 2}\\))([ ^\b % \ / \ |:\n\"]*))|(\"\2([^%\/\|:\n\"]*)\")|((?<!\w)(\.{1,2})?(?<!\/)(\/((\\\b)|[^ \b%\|:\n\"\\\/])+)+\/?)|(%([a-zA-Z]+)%)\\((?:[a-zA-Z0-9() ]*\\)*).*'
        pattern = re.compile(r'%(\w+\\?)*%\\(\w+\.[a-zA-Z]{2,4})?')
        cleantext = re.sub(pattern, ' directory ', str(text))
        pattern = re.compile(r"((((?<!\w)[A-Z,a-z]:)|(\.{1,2}\\))([^\b%\/\|:\n\"]*))|(\"\2([^%\/\|:\n\"]*)\")|((?<!\w)(\.{1,2})?(?<!\/)(\/((\\\b)|[^ \b%\|:\n\"\\\/])+)+\/?)|(%([a-zA-Z]+)%)\\((?:[a-zA-Z0-9() ]*\\)*).*")
        cleantext = re.sub(pattern, ' directory ', str(text))
        # registry_key_pattern = '(HKEY_LOCAL_MACHINE\\|HKLM\\)([a-zA-Z0-9\s_@\-\^!#.\:\/\$%&+={}\[\]\\*])'
        # cleantext = re.sub(registry_key_pattern, ' registry key ', str(text))
        # pattern = re.compile(r'([a-zA-Z]:[\\\\[a-zA-Z0-9]*]*)')
        # cleantext = re.sub(pattern, ' ', str(cleantext))
        pattern = re.compile(r'(\/.*?\.[\w:]+)')
        cleantext = re.sub(pattern, ' ', str(cleantext))
        pattern = re.compile(r'“')
        cleantext = re.sub(pattern, ' ', str(cleantext))
        pattern = re.compile(r'”')
        cleantext = re.sub(pattern, ' ', str(cleantext))
        pattern = re.compile(r'\((.*?)\)')
        cleantext = re.sub(pattern, ' ', str(cleantext))
        pattern = re.compile(r'(\w+\\\w+(\\)?)')
        cleantext = re.sub(pattern, ' ', str(cleantext))
        # File Extension .exe|.zip
        pattern = re.compile(r'(\.[a-z]{3})')
        cleantext = re.sub(pattern, ' ', str(cleantext))
        # [12] remove
        pattern = re.compile(r'(\[\d+\])')
        cleantext = re.sub(pattern, ' ', str(cleantext))
        # IP Address, Port
        pattern = re.compile(r'([0-9]{1,3}\.){3}[0-9]{1,3}\:[0-9]{2,5}|([0-9]{1,3}\.){3}[0-9]{1,3}')
        text = re.sub(pattern, ' ip address ', str(cleantext))

        # text = text.replace('.','',text.count('.')-1)

        return str(text.strip())

    def symantec_sent_tokenize(self, text):
        sentence_tokenize_list = list()
        paragraphs = text.split('\n')
        for paragraph in paragraphs:
            sent_tokenize = nltk.sent_tokenize(paragraph)
            for sentence in sent_tokenize:
                new_sentence = sentence
                new_sentence = regex_checker.dll_matcher(new_sentence)
                new_sentence = regex_checker.regex_ip_address(new_sentence)
                new_sentence = regex_checker.regex_registry_key(new_sentence)
                new_sentence = new_sentence.replace('&lt;', ' ')
                new_sentence = new_sentence.replace('&gt;', ' ')
                new_sentence = new_sentence.replace('[removed]', ' ')
                new_sentence = new_sentence.replace('[', '')
                new_sentence = new_sentence.replace(']', '')
                new_sentence = regex_checker.get_url_match(new_sentence)

                ###
                # if len(sentence) == sentence.rfind('.') + 1:
                    # sentence = self.remove_fullstop(sentence)
                # try:
                #     sentence = self.remove_filepath(sentence)
                # except:
                #     print('Error in regex.')
                sentence_tokenize_list.append({'original':sentence,'processed':new_sentence})
        return sentence_tokenize_list



# def regex_checker():
#     reader = FileReader('reports/test.txt')
#     # text = 'Monitor for registry key creation and/or modification events for the keys of  HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Custom  and  HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\InstalledSDB'
#     import re
#     # pattern = re.compile(r'(\w+\\\w+(\\)?)')
#     # result = re.sub(pattern=pattern, repl='', string=text)
#     # print(result)
#     text = reader.read_file()
#     text = reader.remove_filepath(text)
#     print(text)
#
# Reads the file and create mitre mapping dictionary
# {'ID':{'TECHNIQUE':'DLL Injection','TACTIC':'Defense Evasion'}}
# returns the ttp_df, mitre id to technique-tactic map

def create_mitre_TTP_dictionary(file_name = 'ontology/mitre_ttp.csv'):
    mitre_tech_df = pandas.read_csv(file_name,encoding="ISO-8859-1")
    mitre_tech_list = mitre_tech_df.to_dict('records')
    mitre_tech_dict = dict()
    for mitre_tech in mitre_tech_list:
        try:
            tactic = mitre_tech_dict[mitre_tech['ID']]['TACTIC'] + ','
        except:
            tactic = ''
        mitre_tech_dict[mitre_tech['ID'].lower().strip()] = {'TECHNIQUE':mitre_tech['TECHNIQUE'].strip(),'TACTIC':tactic + mitre_tech['TACTIC'].strip()}
    return mitre_tech_dict

def get_technique_and_tactic(id, ttpdf):
    try:
        return ttpdf[id]
    except:
        return False


def read_file(file_name):
    with open(file_name, 'r', encoding="utf8") as report:
        text = report.read().lower()
    return text

import pandas
def read_csv_file(file_name,encoding='utf-8'):
    data_frame = pandas.read_csv(file_name, encoding=encoding)
    data_frame = data_frame.fillna('')
    data_frame_dict = data_frame.to_dict('records')
    return  data_frame_dict

def write_file(file_name, lists, mode='w'):
    with open(file_name, mode=mode, encoding="utf8") as file:
        for __ in lists:
            file.write(__)
            file.write('\n')
    return
import csv
def write_csv_from_dictionary(file_name, dict_data):
    csv_columns = list(dict_data[0].keys())
    try:
        with open(file_name, 'w', encoding='utf8',newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in dict_data:
                writer.writerow(data)
    except IOError:
        print("I/O error")
    return

def write_csv_from_data_frame(file_name, data_dict_list):
    data_frame = pandas.DataFrame(data_dict_list)
    data_frame.to_csv(file_name, index=None, header=True)
    return


def remove_stopwords(string):
    tokens = string.lower().split()
    output_string = ' '.join([word for word in tokens if word not in stopword_lists])
    return output_string

def stem_and_lemmatize(string, isRemoveStopword=False):
    if str(type(string)) == '<class \'list\'>' or 'list' in str(type(string)):
        string = ' '.join(string).strip()
    if isRemoveStopword:
        string = remove_stopwords(string.lower())
    tokens = string.split()
    stem_tokens = [lemmatizer.lemmatize(word) for word in tokens]
    stem_tokens = [stemmer.stem(word.strip()) for word in stem_tokens]
    return ' '.join(stem_tokens).strip()

# This method will create a dictionary of from the list that the file contains.
# For example, from verb_list.txt file, it will create a dictionary of the verb_lists
def create_dictionary_from_file(filename = 'ontology/verb_list.txt'):
    verb_lists = list(set(read_file(filename).split('\n')))
    verbs_dictionary = {stem_and_lemmatize(verb,isRemoveStopword=True):remove_stopwords(verb) for verb in verb_lists}
    verb_lists = [verb for verb in verbs_dictionary.keys()]
    return verbs_dictionary, verb_lists

# dictionery, keywork = search word in the keys
def is_dictionay_key(dictionary, keyword):
    try:
        attack_verb = dictionary[keyword]
        return True
    except:
        return False

def create_corpus_for_BM25_model(document_list):
    return [doc.split() for doc in document_list]

import scrapper.SymantecScrapper as scrapper
def copy_files(src_dir='scrapper/symantec_processed_new_1',dst_dir='test_reports/new_version'):
    import shutil
    files = scrapper.get_all_files('test_reports/old_version')
    for file in files:
        src_file = file.replace('.txt','.processed')
        src = os.path.join(src_dir,src_file)
        dst = os.path.join(dst_dir,file)
        shutil.copy(src, dst)


if __name__=='__main__':
    # test_string = 'The Trojan then opens a back door that allows an attacker to perform some actions.'
    # import time
    # start_time = time.time()
    # print(stem_and_lemmatize(test_string))
    # dict__ = {'a':1,'b':2}
    # print(len(dict__))
    # end_time = time.time()
    # print('Time: ', (end_time - start_time))
    # copy_files(src_dir='C:\\Users\\rrahman3\\PycharmProjects\\SymantecReportsProcessor\\scrapper\\symantec_only_descryption\\',dst_dir='test_reports/Symantec_Evaluation_Reports')
    # files = scrapper.get_all_files('C:\\Users\\rrahman3\\PycharmProjects\\TTPSense_Git\\test_reports\\old_version\\')
    # for file in files:
    #     print(file)
    #     # src = os.path.join(src_dir,file)
    import re
    text = 'Next, the Trojan gathers the following information about the compromised computer:'
    while True:
        text = str(input('Enter: '))
        registry_key_pattern = '(HKEY_LOCAL_MACHINE\\|HKLM\\)([a-zA-Z0-9\s_@\-\^!#.\:\/\$%&+={}\[\]\\*])+'
        # registry_key_pattern = '[a-zA-Z]:\\(((?![<>:"/\\|?*]).)+((?<![ .])\\)?)*$'
        cleantext = re.sub(registry_key_pattern, ' registry key ', str(text))
        print(cleantext)

    pass


