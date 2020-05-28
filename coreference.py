'''
document = 'Lazarus Group keylogger KiloAlfa obtains user tokens from interactive sessions to execute itself with API call CreateProcessAsUserA under that user\'s context.'
{
    'top_spans': [[0, 1], [0, 3], [3, 3], [11, 11], [12, 12], [14, 14], [16, 16], [18, 20], [18, 21]],
    'predicted_antecedents': [-1, -1, -1, -1, 3, 3, -1, -1, -1],
    'document': ['Lazarus', 'Group', 'keylogger', 'KiloAlfa', 'obtains', 'user', 'tokens', 'from', 'interactive', 'sessions', 'to', 'execute', 'itself', 'with', 'API', 'call', 'CreateProcessAsUserA', 'under', 'that', 'user', "'s", 'context', '.'],
    'clusters': [[[0, 1], [12, 12]], [[0, 3], [14, 14]]]}
'''
from allennlp.predictors.predictor import Predictor
def coref_test(AllenNLP_COREF_PATH, sentence = 'When the Trojan is executed, it copies itself to some location.'):
    # documents = [
    #     # 'Lazarus Group keylogger KiloAlfa obtains user tokens from interactive sessions to execute itself with API call CreateProcessAsUserA under that user\'s context.',
    #     # 'HiddenWasp installs reboot persistence by adding itself to /etc/rc.local.',
    #     'Next, the Trojan creates some registry entry so that it executes whenever Windows starts.'
    # ]
    if len(sentence.strip()) == 0:
        return ''
    # print('Sentence: ',sentence)
    try:
        result = AllenNLP_COREF_PATH.predict(document=sentence)
    except:
        print("Error occured in coref.", sentence)
        return sentence
    document = result['document']
    top_spans = result['top_spans']
    predicted_antecedents = result['predicted_antecedents']
    clusters = result['clusters']
    # print(document)
    # print(top_spans)
    # print(predicted_antecedents)
    # print(clusters)
    new_document = document
    for cluster in clusters:
        # print(cluster)
        # print(cluster[0])
        # print(cluster[1])
        noun = ' '.join(document[cluster[0][0]:cluster[0][1]+1])
        noun = [noun]
        # print(noun)
        for index in range(1,len(cluster)):
            pronuon = ' '.join(document[cluster[index][0]:cluster[index][1]+1])
            new_document = new_document[0:cluster[index][0]] + noun[:] + new_document[cluster[index][1]+1:]
            # print(pronuon)
        # new_sent = sentence.replace(pronuon, noun)
        # print(new_sent)
        print(' '.join(new_document))
    return ' '.join(new_document)

import helper
def coref_text_with_files(model_AllenNLP_Coref, file_name='scrapper/simplified_symentec_reports/Infostealer.Spamnost.2011-121917-3758-99.txt'):
    text = helper.read_file(file_name=file_name)
    processed_text = ''
    for sentence in text.split('\n'):
        processed_text += coref_test(model_AllenNLP_Coref, sentence) + '\n'
    # print(processed_text)
    return processed_text

# text_list = list of {'original':sentence,'processed':new_sentence}
def coref_text_with_list(model_AllenNLP_Coref, text_list):
    processed_text = ''
    return_text_dict = list()
    for sentence in text_list:
        processed_text = coref_test(model_AllenNLP_Coref, sentence['processed'])
        return_text_dict.append({'original':sentence['original'],'processed':processed_text})
    # print(processed_text)
    return return_text_dict

if __name__ == '__main__':
    AllenNLP_COREF_PATH = 'resources/coref-model-2018.02.05.tar.gz'
    model_AllenNLP_Coref = Predictor.from_path(AllenNLP_COREF_PATH)
    # while True:
    #     sentence = str(input('Enter Sentence:\t'))
    #     coref_test(model_AllenNLP_Coref, sentence)
    coref_text_with_files()
