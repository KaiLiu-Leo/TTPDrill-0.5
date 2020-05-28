import pandas
import copy

import re
import pandas
from nltk.stem import WordNetLemmatizer, PorterStemmer
import helper
import configuration
class ParseGhaithOntology():

    def __init__(self):
        pass

    def read_csv(self,file_name='resources/ontology_ghaith.csv'):
        data_frame = pandas.read_csv(file_name, encoding="ISO-8859-1")
        data_frame = data_frame.fillna('0')
        data_frame_dict = data_frame.to_dict('records')
        return  data_frame_dict

    def parse_ontology(self, data_frame_dict):
        util = utilities()
        ontology_list = list()
        ontology_dict_map = dict()
        for dict_entry in enumerate(data_frame_dict):
            temp_list = list()
            for key, val in dict_entry[1].items():
                # try:
                if key == 'CODE':
                    ontology_dict_map[dict_entry[0]] = re.search("T\d*", val).group().lower()
                if key == 'NAME':
                    list_of_word = val.strip().split(' ')
                    # print('qwertyuioqwertyuiqwertyuio',list_of_word)
                    words = [util.lemmatize_and_stem(word, isLmmatize=configuration.isLemmatize, isStem=configuration.isStem) for word in list_of_word]
                    ontology_list.append(words)
                    # print('zxcvbnmZxcvbnmzxcvbnm',words)
                #
                # except:
                #     break

        # ontology_list.append(temp_list)
        return ontology_list, ontology_dict_map

def read_ghaith_ontology():
    from ontology_reader import ParseGhaithOntology
    ontology = ParseGhaithOntology()
    ontology_dict = ontology.read_csv()
    what_list, list_map_dict = ontology.parse_ontology(ontology_dict)
    mapped_list = zip(list_map_dict.values(), what_list)
    data_frame = pandas.DataFrame(mapped_list)
    data_frame.to_csv(r'resources/ghaith_onto.csv', index=None, header=True)
    return what_list, list_map_dict


class ReadOntology():

    def __init__(self):
        #        self.temp_refined_ontolog = dict()
        self.mitre_tech_list = list()
        pass

    def read_mitre_TTP(self, file_name = 'resources/mitre_ttp.csv'):
        self.mitre_tech_df = pandas.read_csv(file_name,encoding="ISO-8859-1")
        self.mitre_tech_list = self.mitre_tech_df.to_dict('records')
        self.mitre_tech_dict = dict()
        for mitre_tech in self.mitre_tech_list:
            try:
                tactic = self.mitre_tech_dict[mitre_tech['ID']]['TACTIC'] + ','
            except:
                tactic = ''
            self.mitre_tech_dict[mitre_tech['ID'].lower()] = {'TECHNIQUE':mitre_tech['TECHNIQUE'],'TACTIC':tactic + mitre_tech['TACTIC']}
        return self.mitre_tech_dict

    def read_csv(self, file_name):
        if file_name is None:
            self.data_frame = pandas.read_csv('resources/ontology_details.csv', encoding="ISO-8859-1")
        else:
            self.data_frame = pandas.read_csv(file_name, encoding="ISO-8859-1")
        self.data_frame = self.data_frame.fillna('')
        return self.data_frame

    def split_ontology(self, ontology_list, split_char):

        refined_ontology_list = list()
        for each_row in ontology_list:
            print(each_row)
            action_what = each_row['action_what']
            #    print(type(action_what))
            action_where = each_row['action_where']
            if type(action_what) != type(0) and type(action_where) != type(0):
                #        print(action_what)
                what_list = action_what.split(split_char)
                where_list = action_where.split(split_char)
                for each_what in what_list:
                    for each_where in where_list:
                        new_entry = copy.deepcopy(each_row)
                        new_entry['action_what'] = each_what.strip()
                        new_entry['action_where'] = each_where.strip()

                        refined_ontology_list.append(new_entry)
        return refined_ontology_list

    """
        This method takes a list of string and returns a list of string without '/', ',', '-'
    """
    def replace_string(self, list_string):
        return_list = list()
        if type(list_string) != type(0) and type(list_string) != type(0.0):
            temp = list_string.replace('/', ',')
            temp = temp.replace('-', ' ')
            return_list = [word.strip() for word in temp.split(',')]
        return return_list


    def split_ontology_list(self, ontology_list):
        refined_ontology_list = list()
        for each_row in ontology_list:
            # __action_what_list = self.replace_string(each_row['action_what'])
            # __action_where_list = self.replace_string(each_row['action_where'])
            # __why_what_list = self.replace_string(each_row['why_what'])
            # __why_where_list = self.replace_string(each_row['why_where'])
            each_row['action_what'] = self.replace_string(each_row['action_what'])
            each_row['action_where'] = self.replace_string(each_row['action_where'])
            each_row['why_what'] = self.replace_string(each_row['why_what'])
            each_row['why_where'] = self.replace_string(each_row['why_where'])
            each_row['how_what'] = self.replace_string(each_row['how_what'])
            each_row['how_where'] = self.replace_string(each_row['how_where'])

        return ontology_list



    def refine_ontology(self):
        ontology_dict = self.data_frame.to_dict('records')
        temp = self.split_ontology(ontology_dict, '/')
        temp_refined_ontology = self.split_ontology(temp, ',')
        self.temp_refined_ontology = temp_refined_ontology
        return temp_refined_ontology

    def print_ontology(self, data_frame):
        if data_frame is None:
            for __ in self.temp_refined_ontology:
                #    if __['_2'] == '212':
                print(__['Id'], ',', __['action_what'], ',', __['action_where'])
        else:
            for __ in data_frame:
                #    if __['_2'] == '212':
                print(__['Id'], ',', __['action_what'], ',', __['action_where'])

    def write_ontology(self, file_name, data_frame):
        if data_frame is None:
            data_frame = pandas.DataFrame(self.temp_refined_ontology)
        if file_name is not None:
            data_frame.to_csv(r'resources/export_dataframe_1.csv', index=None, header=True)
        else:
            data_frame.to_csv(file_name, index=None, header=True)

    def stem(self, ontology_list):
        from nltk.stem import PorterStemmer
        from nltk.tokenize import word_tokenize
        import copy
        ps = PorterStemmer()
        stem_list = list()

        for single_dict in ontology_list:
            temp_dict = dict()
            for key, val in single_dict.items():
                try:
                    temp_dict[key] = ps.stem(val)
                except:
                    temp_dict[key] = val
            stem_list.append(temp_dict)
        return stem_list


def split_1(ontology_dict):
    list_ = list()
    for __each__entry__ in ontology_dict:
        what_list = __each__entry__['action_what'].split(',')
        list_.append([ __each__entry__['Id'],__each__entry__['action_what'].split('/'),__each__entry__['action_where']])
    for __each__ in list_:
        print(__each__)

def preprocess_string(string):
    temp = string.replace('-',' ')
    temp = temp.replace('(',' ')
    temp = temp.replace(')',' ')
    return temp.strip()

def mix_what_where(ontology_dict, action_what, action_where):
    __list__ = list()
    for __each__entry__ in ontology_dict:
        what_list = preprocess_string(__each__entry__[action_what])
        where_list = preprocess_string(__each__entry__[action_where])
        if ';' in what_list:
            what_list = what_list.split(';')
        else:
            what_list = what_list.split(',')
        if ';' in where_list:
            where_list = where_list.split(';')
        else:
            where_list = where_list.split(',')
        # if len(what_list) == len(where_list) == 1 and what_list[0] == '':
        #     continue
        # __list__ = list()
        if len(what_list) == len(where_list):
            # print(__each__entry__['Id'])
            # print('what: ',what_list)
            # print('where: ', where_list)
            for what_where_ontology in zip(what_list,where_list):
                # print(what_where_ontology)
                temp_mix_what = what_where_ontology[0].split('/')
                temp_mix_where = what_where_ontology[1].split('/')
                # print(temp_mix_what)
                # print(temp_mix_where)
                for what in temp_mix_what:
                    for where in temp_mix_where:
                        __dict__ = dict()
                        __dict__['id'] = __each__entry__['Id']
                        # __dict__['bow'] = what.strip() + ' ' + where.strip()
                        __dict__['what'] = what.strip()
                        __dict__['where'] = where.strip()
                        __list__.append(__dict__)
                        # print(__dict__['id'], __dict__['bow'])
        else:
            print(what_list)
            print(where_list)
            for what in what_list:
                for where in where_list:
                    __dict__ = dict()
                    __dict__['id'] = __each__entry__['Id']
                    # __dict__['bow'] = what.strip() + ' ' + where.strip()
                    __dict__['what'] = what.strip()
                    __dict__['where'] = where.strip()
                    __list__.append(__dict__)
                    # print(__dict__['id'], __dict__['bow'])

        # list_.append([ __each__entry__['Id'],__each__entry__['action_what'].split('/'),__each__entry__['action_where']])


    # for __each__ in list_:
    #     print(__each__)
    return __list__

def write_refined_ontology_file(__list__, file_name):
    import csv
    csv_columns = __list__[0].keys()
    with open(file_name, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=csv_columns)
        writer.writeheader()
        for entry in __list__:
            writer.writerow(entry)
    return

### Now we seperated what_where/why/how for the ontology
class Ontology_Separated():
    def __init__(self):
        file_names = ['ontology/refined_how.csv','ontology/refined_why.csv','ontology/refined_what_where.csv'] # old_ontology
        # file_names = ['ontology/new/refined_how.csv','ontology/new/refined_why.csv','ontology/new/refined_what_where.csv'] # new_ontology
        self.df_list = list()
        for file in file_names:
            self.df_list.append(self.read_csv(file).to_dict('records'))

    def read_csv(self, file_name):
        data_frame = pandas.read_csv(file_name, encoding="ISO-8859-1")
        return data_frame.fillna('')


# used in creating separte ontology
class utilities():
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()

    def convert_dict_to_bow(self,__list__,key_vector):
        big_list = list()
        for entry in __list__:
            temp_list = list()
            for key, val in entry.items():
                # print('key: val', key, val)
                if key_vector == '':
                    temp_str_list = entry[key].split(' ')
                elif key == key_vector or key == 'id':
                    temp_str_list = entry[key].split(' ')
                else:
                    continue
                # print('temp_str_list',temp_str_list)
                for str_ in temp_str_list:
                    if str_.strip() == '':
                        continue
                    temp_list.append(str_.lower().strip())
                # print('temp_list: ',temp_list)
            # print(temp_list)
            big_list.append(temp_list)
        __dict = dict()
        for __ in big_list:
            __dict[' '.join(__)] = __
        big_list = list(__dict.values())
        # print('big_list', big_list)
        # big_list = list(set(big_list))
        print(len(big_list))
        return big_list

    def lemmatize_and_stemm_whole_list(self, __list__, key_vector, isLemmatize=True, isStem=True):
        if key_vector == '':
            temp_list = self.convert_dict_to_bow(__list__, '')
        else:
            temp_list = self.convert_dict_to_bow(__list__, key_vector)
        out_list = list()
        for each_list in temp_list:
            temp_out = list()
            for each_word in each_list:
                temp_out.append(self.lemmatize_and_stem(each_word, isLemmatize, isStem))
            out_list.append(temp_out)
        # self.split_ontology_map(out_list)
        #
        # temp_list = self.convert_dict_to_bow(__list__,'what')
        # out_list = list()
        # for each_list in temp_list:
        #     temp_out = list()
        #     for each_word in each_list:
        #         temp_out.append(self.lemmatize_and_stem(each_word, isLemmatize, isStem))
        #     out_list.append(temp_out)
        return self.split_ontology_map(out_list)

    def lemmatize_and_stem(self, word, isLemmatize, isStem):
        lem_output = word
        if isLemmatize:
            lem_output = self.lemmatizer.lemmatize(word)
        stem_output = lem_output
        # if isStem or word.endswith('ing') or word.endswith('ed') or word.endswith('s'):
        if isStem:
            stem_output = self.stemmer.stem(lem_output)
        return stem_output

    # ['t1181', 'use', 'memory', 'location']
    def split_ontology_map(self, __list__):
        ontology_map = list() # [t1181]
        ontology_list = list() # ['use', 'memory', 'location']
        for element in __list__:
            ontology_map.append(element[0])
            ontology_list.append(element[1:])
        return ontology_map, ontology_list

def get_all_what(file_name='resources/ParsedMitreTechnique_V5.csv', column_name='action_what'):
    ontology = ReadOntology()
    ontology_df = ontology.read_csv(file_name)
    ontology_dict = ontology.data_frame.to_dict('records')
    action_what_set = list()
    for __each__entry__ in ontology_dict:
        what_list = preprocess_string(__each__entry__[column_name])
        temp = list()
        # if ',' in what_list or '/' in what_list:
        # print(what_list)
        what_list = what_list.split(',')
        for ll in what_list:
            aa = ll.split('/')
            for a in aa:
                action_what_set.append(a.strip())
                # print(a)
        # action_what_set.append()
    action_what_set = set(action_what_set)
    for a in action_what_set:
        print(a)
    with open('ontology/'+column_name+'.txt', 'w') as file:
        for a in action_what_set:
            print(a)
            file.write(a+'\n')
    # print(what_list)


import helper
def read_action_what(file_name='action_what.txt'):
    text = helper.read_file(file_name)
    text = text.split('\n')
    dict_cyber = dict()
    for tt in text:
        tt = tt.translate(str.maketrans('', '', '!"#$%&\()*+,.:;<=>?@[\\]^_`{|}~')).lower()

    #     print(dict__)
    #     print('tt:',tt)
    #     if tt == '':
    #         continue
    #     stemmed = configuration.stemmer.stem(configuration.lemmatizer.lemmatize(tt)).lower()
    #     print(stemmed)
    #     if stemmed in dict__.keys():
    #         dict__[stemmed] = dict__[stemmed] + ' ' + tt
    #     else:
    #         dict__[stemmed] = tt + ' '
    #     what_list.append(configuration.stemmer.stem(configuration.lemmatizer.lemmatize(tt)).lower())
        key = helper.stem_and_lemmatize(tt, isRemoveStopword=True)
        dict_cyber[key] = helper.remove_stopwords(tt)
    what_list = list(set(list(dict_cyber.values())))
    what_list.sort()
    for __ in what_list:
        print(__)
    print(len(what_list))
    helper.write_file('ontology/temp.txt', what_list)
    # with open('ontology/all_cyber_list_3.txt','w', encoding='utf-8') as f:
    #     keys = list(dict_cyber.values())
    #     keys.sort()
    #     for tt in keys:
    #         # f.write(tt + ' - ' + dict__[tt] + '\n')
    #         f.write(tt + '\n')
    #         print(tt)
    #     # print(configuration.stemmer.stem(tt))
    return what_list


if __name__=='__main__':
    # get_all_what(column_name='action_what')
    # get_all_what(column_name='why_what')
    # get_all_what(column_name='how_what')
    # get_all_what(column_name='action_where')
    # get_all_what(column_name='why_where')
    # get_all_what(column_name='how_where')
    # get_all_what(column_name='example_action_what')
    # a = configuration.stemmer.stem('modification')
    # b = configuration.stemmer.stem('modify')
    # c = configuration.stemmer.stem('modifies')
    # d = configuration.stemmer.stem('modified')
    # print(a,b,c,d)
    read_action_what(file_name='ontology/UniqueALLCyberObjects_Ghaith.txt')
    # read_action_what(file_name='ontology/all_verb_list.txt')
    # read_action_what(file_name='ontology/example_action_what.txt')
    # read_action_what(file_name='ontology/verb_list.txt')
    # read_action_what(file_name='ontology/action_what.txt')
    # read_action_what(file_name='ontology/why_what.txt')
    # read_action_what(file_name='ontology/how_what.txt')

# By calling this method will create a what where in csv file from the main ontology file
def generate_WHAT_WHERE_from_MOHI_ONTOLOGY():
    file_name = {'old':'resources/ParsedMitreTechnique_V5.csv','new':'ontology/Mitre Technique Analysis.csv'}
    # file_name = 'resources/export_dataframe.csv'
    # file_name = 'resources/ontology_details.csv'
    ontology = ReadOntology()
    ontology_df = ontology.read_csv(file_name['new'])
    # print(ontology_df.head())
    ontology_dict = ontology.data_frame.to_dict('records')
    print(ontology_dict)
    mix_what_where1 = mix_what_where(ontology_dict,'action_what','action_where')
    write_refined_ontology_file(mix_what_where1,'ontology/new/refined_what_where.csv')
    mix_what_where1 = mix_what_where(ontology_dict,'why_what','why_where')
    write_refined_ontology_file(mix_what_where1,'ontology/new/refined_why.csv')
    mix_what_where1 = mix_what_where(ontology_dict,'how_what','how_where')
    write_refined_ontology_file(mix_what_where1,'ontology/new/refined_how.csv')
    # print(len(mix_what_where1))
    # print(mix_what_where1)


def analyze_ontology(file_name = 'ontology/new/refined_why.csv'):
    data_frame=pandas.read_csv(file_name)
    data_frame = data_frame.fillna('')
    data_frame_dict = data_frame.to_dict('records')
    for dd in data_frame_dict:
        if dd['what'].strip() == '':
            print(dd)
    # data_frame = pandas.DataFrame(mapped_list)
    # data_frame.to_csv(r'resources/ghaith_onto.csv', index=None, header=True)
    # with open(file_name, mode='r', encoding='utf-8') as file:
    #     text = file.read().split('\n')
    # with open(file_name, mode='w', encoding='utf-8') as file:
    #     for tt in text:
    #         file.write(tt.lower() + '\n')



if __name__=='__main__1':
    # read_ghaith_ontology()
    # generate_WHAT_WHERE_from_MOHI_ONTOLOGY()
    analyze_ontology('ontology/new/refined_what_where.csv')
    # analyze_ontology('ontology/new/refined_why.csv')
    # analyze_ontology('ontology/new/refined_how.csv')
    # ontology_dict = ontology.split_ontology_list(ontology_dict)
    # print(ontology_dict)
    # stem_list = ontology.stem()
    # # for ont  in stem_list:
    # #     print(ont['action_what'])
    # ontology.print_ontology(stem_list)
    # from ontology_reader import ReadOntology
    #
    # file_name = 'resources/ontology_details.csv'
    # ontology = ReadOntology()
    # ontology_df = ontology.read_csv(file_name)
    # ontology_df
    # ontology_dict = ontology.data_frame.to_dict('records')
    # ontology_dict
    # __ = ontology.split_ontology_list(ontology_dict)
    # print(__)
    # stem_list = ontology.stem(__)
    # for _ in stem_list:
    #    print(_['Id'], _['action_what'], _['action_where'])
    #    print(_['Id'], _['why_what'], _['why_where'])
    # what_list = list()
    # for i in stem_list:
    #     what_list.append([i['Id'], i['action_what'], i['action_where'], i['why_what'], i['why_where']])
    # print(what_list[0])
    # ttp_df = ontology.read_mitre_TTP()
    # for key, val in ttp_df.items():
    #     print(key, val['TECHNIQUE'] )
    # print(ttp_df)