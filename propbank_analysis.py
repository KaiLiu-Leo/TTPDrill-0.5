import json
import configuration
def read_json(file_name='resources/propbank.json'):
    with open(file_name, 'r') as json_file:
        data = json.load(json_file)
    print(data.keys().__len__())
    # for key in data.keys():
    #     print(data[key][list(data[key].keys())[0]]['arg'])
    propbank_verbs = dict()
    for key, val in data.items():
        if configuration.stemmer.stem(key) in list(configuration.preprocessOntologies.verb_dict.keys()):
            argument_dict = dict()
            arg_lists = data[key][list(val.keys())[0]]['arg']
            for args in arg_lists:
                argument_dict[args.split('-')[0]] = args.split('-')[1]
            propbank_verbs[configuration.stemmer.stem(key)] = argument_dict
    return propbank_verbs

def print_propbank_verb(propbank_verbs):
    for key, val in propbank_verbs.items():
        print(key, ':', val)
    # key = list(data['inject'].keys())[0]
    # print(data['inject'][key]['arg'])

'''
    { 'inject':{'Arg0':'PAG','Arg1':'PPT'}}
'''
if __name__ == '__main__':
    propbank_verbs = read_json()
    print_propbank_verb(propbank_verbs)