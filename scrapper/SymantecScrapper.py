import requests
from bs4 import BeautifulSoup
from csv import writer
import os

# Please change the output file name
output_file_name = 'Mitre_Techniue_Description_1.csv'
input_file_name = ''
class GetReportList():
    pass

def get_all_report_list(link, reports_link_list):
    base_link = 'https://www.symantec.com'
    # reports_link_list = list()
    response = requests.get(link)
    print(link,end='\n\n')
    soup = BeautifulSoup(response.content, 'html.parser')
    # print(soup)
    table_details = soup.find_all('a', href=True)
    import re
    for link in table_details:
        if re.search(r'\d*-\d*-\d*-\d*', link['href']):
            link_ref = link['href']
            unique_ref = link_ref[link_ref.rfind('/') + 1 :]
            link_dict = dict()
            link_dict['title'] = link.text.replace('/','_') + '.' + unique_ref
            link_dict['data'] = base_link + link['href']
            # print(link_dict)
            reports_link_list.append(link_dict)
    return reports_link_list

def write_all_report_list_links_to_csv(report_list, file_name = r'report_links.csv'):
    import pandas
    links_data_frame = pandas.DataFrame(report_list)
    links_data_frame.to_csv(file_name, index=None, header=True)
    return

def read_all_report_list(file_name = r'report_links.csv'):
    import pandas
    links_data_frame = pandas.read_csv(file_name)
    return links_data_frame.to_dict()

# pip install lxml

def symantec_report_scrape(link, report_name):
    output_dict = dict()
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')
    # print(soup)
    output_dict['title'] = report_name
    # output_dict['data'] = response.content
    output_dict['data'] = soup
    # output_dict['data'] = process_html(response)
    return output_dict

def process_html(raw_html):
    soup = BeautifulSoup(raw_html, 'html.parser')
    report_data = ''
    contents = soup.find_all(class_='content')
    for content in contents:
        # text = html_tag_remover(content)
        # print(text)
        text = content.text
        if 'Updated:' in text:
            # print(text.strip())
            text = html_tag_remover(content)
            report_data += text.strip() + '\n'
        elif 'Technical Description' in text:
            # text = html_tag_remover(content)
            # print(content)
            text = html_tag_remover(content)
            # if 'The Trojan may then perform the following actions:' in text:
                # print(content)
                # res = content.findAll('li')
                # for __ in res:
                #     print(__.text)
                # print(res)
                # print(text)
            # print(text.strip())
            report_data += text.strip() + '\n'
    return report_data

def get_all_files_1(directory_name='symantec_html'):
    import os
    for root, dirs, files in os.walk(directory_name):
        for file in files:
            if file.endswith(".arff"):
                print(os.path.join(root, file))
    return

def create_filename(location, title, extension='.txt'):
    import os
    path = os.path.join(os.getcwd(), location)
    if not os.path.isdir(path):
        try:
            print(os.getcwd())
            print()
            os.mkdir(path)
        except OSError:
            print("Creation of the directory %s failed" % path)
        else:
            print("Successfully created the directory %s " % path)

    file_name = os.path.join(path, title + extension)
    isFile = os.path.isfile(file_name)
    return file_name, isFile

def write_to_file(data_dict, file_name):
    with open(file_name,'w',encoding='utf-8') as file:
        file.write(str(data_dict['data']))
    return

def scrape_symantec(link, title, location):
    """
    :param link: url of the symantec report
    :param title: title of the symantec report
    :param location: which location the reports will be saved in your machine.
            use only the folder name. it will automatically create the folder in your current directory.
    :return:
    """
    try:
        file_name, isFile = create_filename(location, title, '.arff')
        print(file_name,isFile)
        if not isFile:
            report_dict = symantec_report_scrape(link, title)
            # report_dict={'title':'ruhani','data':'ruhani'}
            write_to_file(report_dict, file_name)
            print('Now Created: ',file_name)
        else:
            print('Already Exist: ', file_name)
            return
    except:
        print("Error Occured")
    return

def scrape_html(infile='symantec_html', outfile = 'symantec_processed'):

    f_names = get_all_files(infile)
    # f_names = ['Trojan.Bisonal.2015-040108-2018-99.arff']
    print(len(f_names))
    for f_name in f_names:
        output_dict = dict()
        output_dict['title'] = f_name[:f_name.rfind('.')]
        file_name, isFile = create_filename(outfile, output_dict['title'], '.processed')
        # print(f_name)
        if not isFile:
            with open(os.path.join(infile,f_name), 'r', encoding='utf-8') as f_content:
                raw_html = f_content.read()
            output_dict['data'] = process_html(raw_html)
            write_to_file(output_dict, file_name)
        else:
            print('File Already Exists.')

def cerate_link_manually():
    '''
    :return: a list of all symantect report. 18720 symantec reports link
    '''
    links = list()
    # links.append('https://www.symantec.com/security-center/a-z/A')
    base_link = 'https://www.symantec.com/security-center/a-z/'
    # sublinks = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    sublinks = 'ZYXWVUTSRQPONMLKJIHGFEDCBA'
    links.append(base_link + '_1234567890')
    for char in sublinks:
        links.append(base_link + char)
    # print(links)
    return links

def scrape_all(output_location = 'symantec'):
    links = cerate_link_manually()
    total_length = 0
    for link in links:
        links_list = list()
        get_all_report_list(link, links_list)
        # total_length += len(links_list)
        print(link,'\t',len(links_list))
        for link in links_list:
            scrape_symantec(link['data'], link['title'], output_location)
    # total_length = len(links_list)
    print(total_length)

def get_all_files(mypath):
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return onlyfiles

def combine_all_reports(files):
    import os
    write_file = open('Symantec_reports_processed_technical_description_all.txt','w+',encoding='utf-8')
    for filename in files:
        processed_data = ''
        with open(os.path.join('symantec',filename),'r',encoding='utf-8') as temp_file:
            report_test = temp_file.read()
            processed_data += '-'*200 + '\n' + filename + '\n'

            technical_description_count = report_test.count('Technical Description')
            report_test = report_test.split('\n')
            for data in report_test:
                if 'Recommendations' in data:
                    break
                if 'SUBMITTING A SAMPLE TO SYMANTEC SECURITY RESPONSE' in data:
                    break
                if len(data) < 2:
                    continue
                if 'Technical Description' in data:
                    technical_description_count -= 1
                if technical_description_count < 1:
                    processed_data += data + '\n'
                    # write_file.write(data+'\n')

            processed_data += '-' * 200 + '\n'

            write_file.write(processed_data)
    write_file.close()
    return


def find_redundant_reports(files):
    import os
    redundant_file_list = list()
    write_file = open('Symantec_reports_processed_technical_description_!_is a heuristic detection.txt','w+',encoding='utf-8')
    for filename in files:
        if '!' in filename:
            processed_data = ''
            with open(os.path.join('symantec',filename),'r',encoding='utf-8') as temp_file:
                report_test = temp_file.read()
                if 'is a heuristic detection' in report_test:
                    print(filename)
                    processed_data += '-'*200 + '\n' + filename + '\n'
                    # write_file.write("-" * 200)
                    # write_file.write('\n')
                    # write_file.write(filename + '\n')

                    technical_description_count = report_test.count('Technical Description')
                    report_test = report_test.split('\n')
                    for data in report_test:
                        if 'Recommendations' in data:
                            break
                        if 'SUBMITTING A SAMPLE TO SYMANTEC SECURITY RESPONSE' in data:
                            break
                        if len(data) < 2:
                            continue
                        if 'Technical Description' in data:
                            technical_description_count -= 1
                        if technical_description_count < 1:
                            processed_data += data + '\n'
                            # write_file.write(data+'\n')

                    processed_data += '-' * 200 + '\n'
                    # write_file.write("-" * 200)
                    # write_file.write('\n')
                    if 'is a heuristic detection' in processed_data:
                        redundant_file_list.append(filename)
                        write_file.write(processed_data)
    write_file.close()
    return redundant_file_list

def word_analysis(files, directory, words):
    import os
    redundant_report_count = 0
    redundant_reports_list = list()
    for filename in files:
        with open(os.path.join(directory, filename), 'r', encoding='utf-8') as temp_file:
            report_test = temp_file.read()
            if words[0] in report_test or words[1] in report_test:
                # print(filename)
                redundant_report_count += 1
            else:
                # print(filename+'\n\n')
                # print(report_test)
                redundant_reports_list.append(filename)
    print(redundant_report_count)
    return redundant_report_count, redundant_reports_list

def only_technical_description(old_location, new_location):
    '''

    :param old_location: Directiory of the old reports which will be processed.
    :param new_location: Directory of the new location where the preprocessed reports will be saved.
    :return: nothing. just save the preproccessed files to the new location.
    '''

    # files = get_all_files(old_location)
    files = [
        'symantec_processed_new/Backdoor.Lapadin.2014-081311-0417-99.processed',
        # 'symantec_processed_new/Backdoor.Ehdoor.2016-092906-5002-99.processed',
        # 'symantec_processed_new/3b Trojan.2000-122110-3336-99.processed'
    ]
    for filename in files:
        processed_data = ''
        print(filename)
        # with open(os.path.join(old_location,filename),'r',encoding='utf-8') as temp_file:
        with open(filename,'r',encoding='utf-8') as temp_file:
            report_test = temp_file.read()
            # processed_data += '-'*200 + '\n' + filename + '\n'

            technical_description_count = report_test.count('Technical Description')
            report_test = report_test.split('\n')
            for data in report_test:
                if 'Recommendations' in data:
                    break
                if 'SUBMITTING A SAMPLE TO SYMANTEC SECURITY RESPONSE' in data:
                    break
                if len(data.strip()) == 0:
                    continue
                if 'Technical Description' in data:
                    technical_description_count -= 1
                    continue
                if technical_description_count < 1:
                    processed_data += data + '\n'
                    # write_file.write(data+'\n')

            # processed_data += '-' * 200 + '\n'
        # with open(os.path.join(new_location, filename), 'w', encoding='utf-8') as write_file:
        with open(filename, 'w', encoding='utf-8') as write_file:
            write_file.write(processed_data)
    return

def move_file(files, old_location, new_location):
    import os
    if not os.path.isdir(new_location):
        try:
            print(os.getcwd())
            print()
            os.mkdir(new_location)
        except OSError:
            print("Creation of the directory %s failed" % new_location)
        else:
            print("Successfully created the directory %s " % new_location)
    for file in files:
        os.rename(os.path.join(old_location,file), os.path.join(new_location,file))

def preprocess_reports():
    with open('symantec/W32.Beagle.AW@mm.2004-102910-4447-99.txt','r') as file:
        data = file.read()
        print(data.count('Technical Description'))

def html_tag_remover(raw_html):
    import re
    # print(raw_html)
    cleanr = re.compile(r'<!--(.|\n)*?-->')
    cleantext = re.sub(cleanr, '\n', str(raw_html))
    # cleanr = re.compile(r'<li>.*?</li>')
    # print(re.findall(cleanr, cleantext))
    # cleantext = re.sub(cleanr, '\n', cleantext)
    cleanr = re.compile(r'<.*?>')
    cleantext = re.sub(cleanr, '\n', cleantext)
    # print(cleantext)
    temp_str = ''
    for __ in cleantext.split('\n'):
        if __.strip() != '':
            temp_str+=__.strip()+'\n'
    # print(temp_str)
    return temp_str

if __name__=='__main__':
    # pass
    # get_all_files('symantec_html')
    # scrape_html()
    # only_technical_description('symantec_processed','symantec_only_descryption')
    only_technical_description('symantec_processed_new/Backdoor.Lapadin.2014-081311-0417-99.processed','symantec_processed_new')
    # only_technical_description('symantec_processed_new','symantec_processed_new_1')
    # str__ = ''
    # with open('symantec_html/Bloodhound.PDF.12.2009-050109-1000-99.arff','r') as file:
    #     str__ = file.read()
    # print(process_html(str__))
    # test_link = 'https://www.symantec.com/security-center/writeup/2015-040108-2018-99'
    # res = symantec_report_scrape(test_link,'temp.txt')
    # # write_to_file({'data':'ruhani'},'temp.txt')
    # write_to_file(res,'temp.txt')
    # html_tag_remover(test_str)
    # scrape_all('symantec_html')
    # ghaith_reports_directory = 'C:\\Users\\rrahman3\\Google Drive\\Study UNCC\\TTPDrill Takeover\\Raw Data\\SymantecThreatReports\\all-symantec-reports\\not-useful'
    # ghaith_reports_directory_new = 'C:\\Users\\rrahman3\\Google Drive\\Study UNCC\\TTPDrill Takeover\\Raw Data\\SymantecThreatReports\\all-symantec-reports\\not-useful\\others'
    # reports = 'only_description'
    # files = get_all_files(reports)
    # print(len(files))
    # redundant_files = find_redundant_reports(files)
    # move_file(redundant_files,'symantec','redundant')
    # combine_all_reports(files)
    # preprocess_reports()
    # only_technical_description(files,'symantec','only_description')
    # a, b = word_analysis(files, reports, ['is a detection','is a heuristic detection'])
    # move_file(b, reports, 'is_a_detection')
    # import re
    # text = 'Files that are detected as Trojan.Bamital.B!inf2 are considered  malicious. We suggest that any files you believe are incorrectly  detected be submitted to Symantec Security Response. For instructions on  how to do this using Scan and Deliver, read Submit Virus Samples'
    # regex = r'^Files'
    # print(re.search(text, regex))



