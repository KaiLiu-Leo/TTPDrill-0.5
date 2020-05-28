import re

import nltk
import helper
from nltk.corpus import stopwords
from pycorenlp import StanfordCoreNLP
import json

class relation_miner():
    def __init__(self, stanfordCoreNLP):
        self.stanfordCoreNLP = stanfordCoreNLP

    def getProperText(self, text):
        pattern = re.compile(r'\b(' + r'|'.join(stopwords.words('english')) + r')\b\s*')
        text = pattern.sub('', text)
        #        print(text)
        return text

    def depparse(self, text):
        output = self.stanfordCoreNLP.annotate(text, properties={
            'annotators': 'depparse',
            'outputFormat': 'json'
        })

        parsed = []
        for i in output["sentences"]:
            current_parsed = []
            #        for j in i["basicDependencies"]:
            for j in i["enhancedPlusPlusDependencies"]:
                # exm: 1st sentence> [('ROOT', 'ROOT', 'eat'), ('nsubj', 'eat', 'I'), ('dobj', 'eat', 'chicken'), ('punct', 'eat', '.')]
                # 2nd sentence> [('ROOT', 'ROOT', 'love'), ('nsubj', 'love', 'I'), ('dobj', 'love', 'chicken'), ('punct', 'love', '.')]
                current_parsed.append(tuple((j['dep'], j['governorGloss'], j['dependentGloss'])))
            # parsed example:
            # [
            #   [('ROOT', 'ROOT', 'eat'), ('nsubj', 'eat', 'I'), ('dobj', 'eat', 'chicken'), ('punct', 'eat', '.')],
            #   [('ROOT', 'ROOT', 'love'), ('nsubj', 'love', 'I'), ('dobj', 'love', 'chicken'), ('punct', 'love', '.')]
            # ]
            parsed.append(current_parsed)
        return parsed

    def get_important_relations(self, dep_tree, sentence):
        extracted_words = dict()
        what_bagofwords = set()
        where_bagofwords = set()
        where_attribute_bagofwords = set()
        how_bagofwords = set()
        why_bagofwords = set()
        when_bagofwords = set()
        subject_bagofwords = set()
        action_bagofwords = set()

        for node in dep_tree[0]:
            #            print(node)
            self.get_relation(node, 'dobj', what_bagofwords, where_bagofwords)
            # if node[0] == 'dobj':
            #   action_bagofwords.add(verb+" "+obj)

            self.get_relation(node, 'nsubj',
                              what_bagofwords,
                              subject_bagofwords)

            self.get_relation(node, 'nmod:on',
                              what_bagofwords,
                              where_attribute_bagofwords)

            self.get_relation(node, 'nmod:in',
                              where_attribute_bagofwords,
                              where_attribute_bagofwords)

            self.get_relation(node, 'advcl:to',
                              what_bagofwords,
                              why_bagofwords)

            self.get_relation(node, 'compound',
                              where_bagofwords,
                              where_bagofwords)

            self.get_relation(node, 'nsubjpass',
                              where_bagofwords,
                              where_bagofwords)

            self.get_relation(node, 'nmod:agent',
                              where_bagofwords,
                              where_bagofwords)
            self.get_relation(node, 'nmod:from',
                              where_bagofwords,
                              where_bagofwords)
            self.get_relation(node, 'nmod:to',
                              where_bagofwords,
                              where_bagofwords)
            self.get_relation(node, 'nmod:with',
                              where_bagofwords,
                              where_bagofwords)
            self.get_relation(node, 'nmod:via',
                              where_bagofwords,
                              where_bagofwords)
            self.get_relation(node, 'nmod:over',
                              where_bagofwords,
                              where_bagofwords)
            self.get_relation(node, 'nmod:for',
                              where_bagofwords,
                              where_bagofwords)
            self.get_relation(node, 'nmod:via',
                              where_bagofwords,
                              where_bagofwords)
            self.get_relation(node, 'nmod:through',
                              where_bagofwords,
                              where_bagofwords)
            self.get_relation(node, 'nmod:using',
                              where_bagofwords,
                              where_bagofwords)
            self.get_relation(node, 'nmod:into',
                              where_bagofwords,
                              where_bagofwords)

        #        what_bafofwords.append(verb)
        #        where_bagofwords.append(obj)
        extracted_words['what'] = helper.remove_stopwords(what_bagofwords)
        extracted_words['where'] = helper.remove_stopwords(where_bagofwords)
        extracted_words['where_attribute'] = helper.remove_stopwords(where_attribute_bagofwords)
        extracted_words['why'] = helper.remove_stopwords(why_bagofwords)
        extracted_words['when'] = helper.remove_stopwords(when_bagofwords)
        extracted_words['how'] = helper.remove_stopwords(how_bagofwords)
        extracted_words['subject'] = helper.remove_stopwords(subject_bagofwords)
        extracted_words['action'] = helper.remove_stopwords(action_bagofwords)
        extracted_words['text'] = sentence


        return extracted_words

    def get_relation(self, node, relation_type, *argv):
        #        print(node)
        if node[0] == relation_type:
            k = 1
            for arg in argv:
                #                print(arg)
                arg.add(node[k])
                k += 1
            #                print(arg)
            #            print(node[1], node[2])
            return node[1], node[2]

    def list_important_info(self, text):

        dep_parse_tree = self.depparse(text)
        #        print(dep_parse_tree)
        important_dict = self.get_important_relations(dep_parse_tree, text)
        return important_dict

    def all_imp_stuff(self, text):
        ourput_list = list()
        for sent in text:
            print(sent)
            dict_ = self.list_important_info(sent)
            print(dict_)
            ourput_list.append(dict_)

        return ourput_list

    def get_important_relations_new(self, list_of_tuples, sentence):
        list_of_forest = []
        for tuples in list_of_tuples:
            nodes = {}
            forest = []
            for count1 in tuples:
                print(count1)
                # count1:
                # ('ROOT', 'ROOT', 'eat')
                # ('nsubj', 'eat', 'I')
                # ('dobj', 'eat', 'chicken')
                # ('punct', 'eat', '.')
                rel, parent, child = count1
                # nodes[child]
                # {'Name': 'eat', 'Relationship': 'ROOT'}
                # {'Name': 'I', 'Relationship': 'nsubj'}
                # {'Name': 'chicken', 'Relationship': 'dobj'}
                # {'Name': '.', 'Relationship': 'punct'}

                # if rel in ['dobj','amod','compound']:
                    # print(count1)
                    # nodes[parent] = {'Name': parent, 'Relationship': rel}
                nodes[child] = {'Name': child, 'Relationship': rel}

            for count2 in tuples:
                # count2
                # ('ROOT', 'ROOT', 'eat')
                # ('nsubj', 'eat', 'I')
                # ('dobj', 'eat', 'chicken')
                # ('punct', 'eat', '.')
                rel, parent, child = count2
                # node
                # {'Name': 'eat', 'Relationship': 'ROOT'}
                # {'Name': 'I', 'Relationship': 'nsubj'}
                # {'Name': 'chicken', 'Relationship': 'dobj'}
                # {'Name': '.', 'Relationship': 'punct'}
                # if rel in ['dobj', 'amod', 'compound']:
                    # print(count2)
                node = nodes[child]

                if parent == 'ROOT':
                    # {'Name': 'eat', 'Relationship': 'ROOT'}
                    forest.append(node)
                else:
                    # parent
                    # {'Name': 'eat', 'Relationship': 'ROOT'}
                    # {'Name': 'eat', 'Relationship': 'ROOT', 'children': [{'Name': 'I', 'Relationship': 'nsubj'}]}
                    # {'Name': 'eat', 'Relationship': 'ROOT', 'children': [{'Name': 'I', 'Relationship': 'nsubj'}, {'Name': 'chicken', 'Relationship': 'dobj'}]}
                    parent = nodes[parent]
                    if not 'children' in parent:
                        parent['children'] = []
                    children = parent['children']
                    children.append(node)

            list_of_forest.append(forest)

        print('---------------------------------------')
        print(list_of_forest)
        print(list_of_tuples)
        # for relation in dep_tree[0]:
        #     if relation[0] == 'dobj':
        #
        #     print(relation)
        return

def test():
    from helper import FileReader
    from helper import StanfordServer
    isFile = True
    isStemmer = False
    isServerRestart = False
    report_name = 'reports/test.txt'
    preprocess_tools = FileReader(report_name)
    text = preprocess_tools.read_file()
    text_list = preprocess_tools.get_sent_tokenize(text)
    stanfordServer = StanfordServer()
    if isServerRestart:
        stanfordServer.startServer()
    stanfordNLP = stanfordServer.get_stanforcorenlp()
    print(text_list)
    # extracted_list = getReportExtraction(isFile, isStemmer, isServerRestart, report_name)
    # print(extracted_list)
    nlp_extract = relation_miner(stanfordNLP)
    extracted_list = nlp_extract.all_imp_stuff(text_list)
    print(extracted_list)

def tree_example():
    from anytree import Node, RenderTree

    udo = Node(name='nsubj')
    marc = Node(name='dobj', parent=udo)
    lian = Node(parent=marc, name='amod')
    dan = Node(parent=udo, name='nmod:for')
    jet = Node(parent=dan, name='nsubj')
    jan = Node(parent=dan, name='compound')
    joe = Node(parent=dan, name='det')

    print(udo)
    Node('/Udo')
    print(joe)
    Node('/Udo/Dan/Joe')

    for pre, fill, node in RenderTree(udo):
        print("%s%s%s" % (pre, node.name, fill))

    print(dan.children)
    (Node('/Udo/Dan/Jet'), Node('/Udo/Dan/Jan'), Node('/Udo/Dan/Joe'))

if __name__=='__main__':
    test()

