from flask import Flask, request
import configuration
# import preProcessTool
from mapModule import seperated_ontology
import json

import mapModule

app = Flask(__name__)
preprocessOntologies = configuration.preprocessOntologies #preProcessTool.preProcessTool(isGhaithOntology=configuration.isGhaithOntology)
configuration.isFile=False

'''
    Creates the final map for the server.
'''
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

def mapFromCSV(csv_list):
    __list__ = list()
    for mapped_list in csv_list[1:]:
        try:
            __dict__ = dict()
            __dict__['serial'] = '1'
            __dict__['subSerial'] = '0'
            __dict__['typeOfAction'] = 's'
            __dict__['original_sentence'] = mapped_list[0]
            __temp_dict__ = {'description': '', 'data': mapped_list[1], 'link': '', 'highlight': ''}
            __dict__['action'] = __temp_dict__
            __temp_dict__ = {'description': '', 'data': mapped_list[2], 'link': '', 'highlight': ''}
            __dict__['object'] = __temp_dict__
            __temp_dict__ = {'description': '', 'data': mapped_list[3], 'link': '', 'highlight': ''}
            __dict__['goal'] = __temp_dict__
            __temp_dict__ = {'description': '', 'data': mapped_list[4], 'link': '', 'highlight': ''}
            __dict__['precondition'] = __temp_dict__
            __temp_dict__ = {'description': '', 'data': mapped_list[5], 'link': '', 'highlight': ''}
            __dict__['api'] = __temp_dict__
            __temp_dict__ = {'description': '', 'data': mapped_list[6], 'link': '', 'highlight': ''}
            __dict__['techId'] = __temp_dict__
            __temp_dict__ = {'description': '', 'data': mapped_list[7], 'link': '', 'highlight': ''}
            __dict__['technique'] = __temp_dict__
            __temp_dict__ = {'description': '', 'data': mapped_list[8], 'link': '', 'highlight': ''}
            __dict__['tactic'] = __temp_dict__
            __list__.append(__dict__)
        except:
            print('None')
    print('--------------------------------------Final Result ----------------------------------------------------------')
    for __ in __list__:
        print(__)
    return __list__

def server_mapping(result, ttp_df):
    __list__ = list()
    for mapped_technique in result:
        text = mapped_technique['text']
        mapped = mapped_technique['map']
        for each_mapped in mapped:
            try:
                report_text = each_mapped['text']
                action_vector = each_mapped['bow']
                mitre_mapped = each_mapped['map']
                for ____ in mitre_mapped:
                    ttp_id = ____['ttp_id']
                    if (____['ttp_score'] >= configuration.BM25_THRESHOLD):
                        __dict__ = dict()
                        __dict__['serial'] = '1'
                        __dict__['subSerial'] = '0'
                        __dict__['typeOfAction'] = 's'
                        __dict__['original_sentence'] = report_text
                        __temp_dict__ = {'description':'','data':action_vector['what'],'link':'','highlight':''}
                        __dict__['action'] = __temp_dict__
                        __temp_dict__ = {'description':'','data':action_vector['where'],'link':'','highlight':''}
                        __dict__['object'] = __temp_dict__
                        __temp_dict__ = {'description':'','data':action_vector['why'],'link':'','highlight':''}
                        __dict__['goal'] = __temp_dict__
                        __temp_dict__ = {'description':'','data':action_vector['when'],'link':'','highlight':''}
                        __dict__['precondition'] = __temp_dict__
                        __temp_dict__ = {'description':'','data':action_vector['how'],'link':'','highlight':''}
                        __dict__['api'] = __temp_dict__
                        __temp_dict__ = {'description':'','data':____['ttp_id'],'link':'','highlight':''}
                        __dict__['techId'] = __temp_dict__
                        __temp_dict__ = {'description':'','data':ttp_df[ttp_id]['TECHNIQUE'],'link':'','highlight':''}
                        __dict__['technique'] = __temp_dict__
                        __temp_dict__ = {'description':'','data':ttp_df[ttp_id]['TACTIC'],'link':'','highlight':''}
                        __dict__['tactic'] = __temp_dict__
                        __list__.append(__dict__)
            except:
                print('None')
            print('\n\n')
    print('--------------------------------------Final Result ----------------------------------------------------------')
    for __ in __list__:
        print(__)
    return __list__


@app.route("/", methods=["POST"])
def hello():
    temp = request.get_data()
    dict_json = json.loads(temp.decode('utf-8'))
    temp = dict_json['value']

    # temp = temp.decode('utf-8')
    # print(temp.decode('utf-8'))
    # data = json.loads(temp)
    # print(data)
    # temp = data['value']
    # # reportTxt = temp
    # temp_text = temp
    # if '\\n' in temp:
    #     temp_text = ''.join(temp.split('\\n'))
    # print(temp_text)
    # reportTxt = 'Malware deletes a file.'
    # reportTxt = 'On June 9th, 2017 Morphisec Lab published a blog post detailing a new infection vector technique using an RTF document containing an embedded JavaScript OLE object. When clicked it launches an infection chain made up of JavaScript, and a final shellcode payload that makes use of DNS to load additional shellcode from a remote command and control server. In this collaboration post with Morphisec Lab and Cisco\'s Research and Efficacy Team, we are now publishing details of this new document variant that makes use of an LNK embedded OLE object, which extracts a JavaScript bot from a document object, and injects a stealer DLL in memory using PowerShell. The details we are releasing are to provide insight into attack methodologies being employed by sophisticated groups such as FIN7 who are consistently changing techniques between attacks to avoid detection, and to demonstrate the detection capabilities of the AMP for Endpoints and Threat Grid product lines. This is relevant to the constantly changing threats that are affecting multiple types of industries on a daily basis.'
    # reportTxt = 'Cobalt Group has sent malicious Word OLE compound documents to victims.'

    # print("***********************:  ", reportTxt)
    # result = seperated_ontology(preprocessOntologies, isDependencyParser=configuration.isDependencyParser,isGhaithOntology=configuration.isGhaithOntology, report_name='reports/test.txt')
    result = seperated_ontology(preprocessOntologies, isDependencyParser=configuration.isDependencyParser,isGhaithOntology=configuration.isGhaithOntology, report_name=temp)
    csv_list = mapModule.create_output_map(result,text='')
    return {'result':mapFromCSV(csv_list)}

if __name__ == "__main__":
    print('___server___')
    # test = b'{"output":"json","value":"On June 9th, 2017 Morphisec Lab published a blog post detailing a new infection vector technique using an RTF document containing an embedded JavaScript OLE object. When clicked it launches an infection chain made up of JavaScript, and a final shellcode payload that makes use of DNS to load additional shellcode from a remote command and control server. In this collaboration post with Morphisec Lab and Cisco\'s Research and Efficacy Team, we are now publishing details of this new document variant that makes use of an LNK embedded OLE object, which extracts a JavaScript bot from a document object, and injects a stealer DLL in memory using PowerShell. The details we are releasing are to provide insight into attack methodologies being employed by sophisticated groups such as FIN7 who are consistently changing techniques between attacks to avoid detection, and to demonstrate the detection capabilities of the AMP for Endpoints and Threat Grid product lines. This is relevant to the constantly changing threats that are affecting multiple types of industries on a daily basis.\\nINFECTION VECTOR\\nThe dropper variant that we encountered makes use of an LNK file to execute wscript.exe with the beginning of the JavaScript chain from a word document object:\\n\\nThis chain involves a substantial amount of base64 encoded JavaScript files that make up each component of the JavaScript bot. It also contains the reflective DLL injection PowerShell code to inject an information stealing malware variant DLL which will be discussed further.\\n"}'
    # test = str(test)

    app.run()
    # hello(test)
    print('___server___')
    # hello('Malware deletes a file.')
