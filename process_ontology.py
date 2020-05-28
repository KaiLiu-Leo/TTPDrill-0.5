import helper
import json

file_name = 'ontology/examples/ontology_from_examples.csv'

def shrink_example_ontology():
    ontology_list = helper.read_csv_file(file_name=file_name)
    print('Total Length: ', len(ontology_list))
    shrinked_list = list()
    for ontology in ontology_list:
        new_dict = {
            'id':ontology['id'].lower().strip(),
            'what':ontology['what'].lower().replace(',',' ').strip(),
            'where':ontology['where'].lower().replace(',',' ').replace('"','').strip()
        }
        shrinked_list.append(json.dumps(new_dict))
    shrinked_list = list(set(shrinked_list))
    ontology_list = list()
    for ontology in shrinked_list:
        ontology_list.append(json.loads(ontology))
    helper.write_csv_from_dictionary('ontology/examples/ontology_from_examples_1.csv', ontology_list)
    print('Total Length: ', len(shrinked_list))

def filter_spaces(file_name='ontology/examples/ontology_from_examples_1.csv'):
    ontology_list = helper.read_csv_file(file_name=file_name)
    print('Total Length: ', len(ontology_list))
    shrinked_list = list()
    for ontology in ontology_list:
        new_dict = {
            'id':ontology['id'],
            'what':ontology['what'],
            'where':' '.join(ontology['where'].split())
        }
        shrinked_list.append(new_dict)
    helper.write_csv_from_dictionary('ontology/examples/ontology_from_examples_2.csv', shrinked_list)
    print('Total Length: ', len(shrinked_list))

import re
import configuration
symantec_description_pattern = re.compile(r'\[(.*?)\]')




def process_single_AllenNLP_description(single_extraction_description):
    match = symantec_description_pattern.findall(single_extraction_description)
    single_extraction_dictionary = dict()
    for results in enumerate(match):
        tuples = results[1]
        arg_name = tuples[0:tuples.find(':')].strip()
        arg_val = tuples[tuples.find(':') + 1:].strip()
        single_extraction_dictionary[arg_name] = arg_val
    return single_extraction_dictionary





if __name__ == '__main__':
    # shrink_example_ontology()
    filter_spaces()


