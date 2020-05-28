import requests
from bs4 import BeautifulSoup
from csv import writer

# Please change the output file name
output_file_name = 'Mitre_Techniue_Description_1.csv'
input_file_name = ''

def get_all_attack_list(link, attack_list, class_name='table table-bordered table-light mt-2'):

    response = requests.get(link)
    print(link,end='\n\n')
    soup = BeautifulSoup(response.content, 'html.parser')
    table_details = soup.find_all(class_=class_name)
    for table_rows in table_details:
        for table_row in table_rows.find_all('tr'):
            table_columns = table_row.find_all('td')
            if table_columns.__len__() > 0:
                attack_list.append('https://attack.mitre.org/techniques/' + table_columns[0].text)
    return attack_list

links = {
#            'https://attack.mitre.org/techniques/pre/',
            'https://attack.mitre.org/techniques/enterprise/',
#            'https://attack.mitre.org/techniques/mobile/',
        }
class_name = 'table table-bordered table-light mt-2'

attack_list = list()

for link in links:
    attack_list = get_all_attack_list(link, attack_list, class_name)

attack_list.__len__()