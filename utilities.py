class FileReader():
    def __init__(self, file_name):
        self.file_name = file_name

    def read_file(self):
        with open(self.file_name,'r', encoding="utf8") as report:
            strs = report.read()
        self.text = strs
        # print(strs)
        return strs

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
        pattern = re.compile(r"((((?<!\w)[A-Z,a-z]:)|(\.{1,2}\\))([^\b%\/\|:\n\"]*))|(\"\2([^%\/\|:\n\"]*)\")|((?<!\w)(\.{1,2})?(?<!\/)(\/((\\\b)|[^ \b%\|:\n\"\\\/])+)+\/?)|(%([a-zA-Z]+)%)\\((?:[a-zA-Z0-9() ]*\\)*).*")
        cleantext = re.sub(pattern, 'directory', str(text))
        pattern = re.compile(r'([a-zA-Z]:[\\\\[a-zA-Z0-9]*]*)')
        cleantext = re.sub(pattern, ' ', str(cleantext))
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
        pattern = re.compile(r'(\.[a-z]{3})')
        text = re.sub(pattern, ' file ', str(cleantext))

        # text = text.replace('.','',text.count('.')-1)

        return str(text)

    def symantec_sent_tokenize(self, text):
        sentence_tokenize_list = list()
        paragraphs = text.split('\n')
        for paragraph in paragraphs:
            sent_tokenize = nltk.sent_tokenize(paragraph)
            for sentence in sent_tokenize:
                ###
                # if len(sentence) == sentence.rfind('.') + 1:
                    # sentence = self.remove_fullstop(sentence)
                    # sentence = self.remove_filepath(sentence)
                sentence_tokenize_list.append(sentence)
        return sentence_tokenize_list


import re
import nltk
from nltk.corpus import stopwords
from pycorenlp import StanfordCoreNLP
import json
import os
from nltk.parse.corenlp import CoreNLPServer


# nltk.download('stopwords')
import requests
import os
class StanfordServer():

    def start_core_nlp_server(self):
        home = os.path.expanduser("~")
        if os.name == 'nt':
            java_path = "C:\\Program Files\\Java\\jdk1.8.0_201\\bin\\java.exe"
            download_path = os.path.join(home, "Downloads")
            STANFORD_HOME = os.path.join(download_path, "stanford-corenlp-full-2018-10-05")
        else: #'posix
            java_path ="/usr/lib/jvm/java-8-oracle/"
            download_path = os.path.join(home, "ttp_sense_python")
            STANFORD_HOME = os.path.join(download_path, "lib")

        print('Stanford_Directory: ', STANFORD_HOME)
        os.environ['JAVAHOME'] = java_path

        # # The server needs to know the location of the following files:
        # #   - stanford-corenlp-X.X.X.jar
        # #   - stanford-corenlp-X.X.X-models.jar
        # # Create the server
        server = CoreNLPServer(
            os.path.join(STANFORD_HOME, "stanford-corenlp-3.9.2-models.jar"),
            os.path.join(STANFORD_HOME, "stanford-corenlp-3.9.2.jar"),
            os.path.join(STANFORD_HOME, "stanford-english-corenlp-2018-10-05-models.jar"),
        )
        # # Start the server in the background
        server.start()
        print("Server Started")


    def startServer(self):
        try:
            response = requests.get('http://localhost:9000')
        except requests.exceptions.ConnectionError:
            print('ConnectionError')
            self.start_core_nlp_server()
        return self.get_stanforcorenlp()

    def get_stanforcorenlp(self):
        self.stanfordCoreNLP = StanfordCoreNLP('http://localhost:9000')
        return self.stanfordCoreNLP


def remove_stopwords(word_tekens):
    import nltk
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words('english'))
    filtered_sentence = [w for w in word_tekens if not w in stop_words]
    return filtered_sentence

from nltk.stem import WordNetLemmatizer, PorterStemmer
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()
def lemmatize_and_stem(word, isLmmatize, isStem):
    lem_output = word
    if isLmmatize:
        lem_output = lemmatizer.lemmatize(word)
    stem_output = lem_output
    if isStem or word.endswith('ing') or word.endswith('ed') or word.endswith('s'):
        stem_output = stemmer.stem(lem_output)
    return stem_output


# print(remove_stopwords(['ruani','a','mon','the','ruh']))

def regex_checker():
    reader = FileReader('reports/test.txt')
    # text = 'Monitor for registry key creation and/or modification events for the keys of  HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Custom  and  HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\InstalledSDB'
    import re
    # pattern = re.compile(r'(\w+\\\w+(\\)?)')
    # result = re.sub(pattern=pattern, repl='', string=text)
    # print(result)
    text = reader.read_file()
    text = reader.remove_filepath(text)
    print(text)
if __name__=='__main__':
    regex_checker()
    # pass