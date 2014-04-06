import time
import requests
#from BeautifulSoup import BeautifulSoup

from pyquery import PyQuery
 
import threading
import libxml2

#import socket
#socket.setdefaulttimeout(10)

web = 'https://www.vk.com/catalog.php'
vk = 'https://www.vk.com/'
selection = 'catalog.php?selection='

def get_html_page(reference_to_vk):
    request_to_vk = requests.get(reference_to_vk)
    if request_to_vk.status_code != 200:
        print request_to_vk.headers
        print reference_to_vk
        return None
    html_page = PyQuery(request_to_vk.text)
    return html_page

def search_of_sing_page(html_page):
    for link in html_page.find('a'):
        if link.get('href').startswith('catalog.php?selection'):
            last_reference = link.get('href')
        if link.get('href').startswith('id'):
            last_reference = link.get('href')
            return last_reference
    return last_reference

def get_intervals(count_of_thread, million):
    previouse_value = 0
    intervals = []
    intervals.append(previouse_value)
    size_of_interval = int(million)/count_of_thread
    for i in range(count_of_thread-1):
        previouse_value += size_of_interval
        intervals.append(previouse_value)
        i += 1
    intervals.append(int(million))
    return intervals

def search_of_last_page(reference_to_vk):
    value_for_catalog = 'catalog.php'
    value_for_vk = reference_to_vk.replace(value_for_catalog,'')
    while not search_of_sing_page(get_html_page(reference_to_vk)).startswith('id'):
        last_id = search_of_sing_page(get_html_page(reference_to_vk))
        reference_to_vk = value_for_vk + search_of_sing_page(get_html_page(reference_to_vk))
    return last_id

def parse_of_last_id(last_id):
    pages = last_id.replace(selection, '')
    return int(pages.split('-')[0]), int(pages.split('-')[1]), int(pages.split('-')[2])

def get_ids(interval_beg, interval_end, million, thousand, hundred, file_name):
    
    file_for_id = open(file_name, 'w')
    
    if million == interval_end:
        limit_for_million = million
    else:
        limit_for_million = interval_end - 1

    limit_for_thousand = 99
    limit_for_hundred = 99

    million_counter = interval_beg
    
    while million_counter != limit_for_million + 1:
        
        if million_counter == million:
            limit_for_thousand = thousand
        thousand_counter = 0
        
        while thousand_counter != limit_for_thousand + 1:
        
            if thousand_counter == thousand:
                limit_for_hundred = hundred
            hundred_counter = 0
            
            while hundred_counter != limit_for_hundred + 1:
                
                try:
                    catalog_code = str(million_counter) + '-' + str(thousand_counter) + '-' + str(hundred_counter) 
                    page_addr = vk + selection + catalog_code
                  
                    #html = get_html_page(page_addr)
                
#                     if html != None:
#                         file_for_id.write(catalog_code + "\n")
#                         file_for_id.flush()
#                         hundred_counter += 1
#                     else:
#                         print "Invalid page: '" + page_addr + "'"
                            
                except requests.ConnectionError:
                    print "Connection error at '" + page_addr + "'"
                                            
            thousand_counter += 1
        million_counter += 1
        
    file_for_id.close()

def multithreading(count_of_thread):
    
    #million, thousand, hundred = parse_of_last_id(search_of_last_page(web))
    
    million  = 99
    thousand = 99
    hundred  = 99
    
    current_count_of_thread = 0
    
    list_of_threads = []
    list_of_files   = []
    
    while current_count_of_thread != count_of_thread:
        
        file_name = 'id' + str(current_count_of_thread) + '.txt'
        
        list_of_files.append(file)
        
        intervals = get_intervals(count_of_thread, million)
        int_beg = intervals[current_count_of_thread];
        int_end = intervals[current_count_of_thread + 1];
        
        print int_beg, int_end, million, thousand, hundred, file_name
             
        thread = threading.Thread(target=get_ids, args=(int_beg, int_end, million, thousand, hundred, file_name))
        thread.start()
        
        list_of_threads.append(thread);
        current_count_of_thread += 1

    all_is_alive = True
    
    while all_is_alive:
        for thread in list_of_threads:
            print "Thread '" + thread.getName() + "' is alive: " + str(thread.isAlive())
            all_is_alive = all_is_alive or thread.isAlive()
        time.sleep(30)
        
    return list_of_files

def save_ids_in_one_file(count_of_thread):
        
    list_of_files = multithreading(count_of_thread); 
    final_file    = open('final_file.txt', 'w')
    
    for file_name in list_of_files:
        file_from_list = open(str(file_name), 'r')
        line = file_from_list.readline()
        while line:
            line = file_from_list.readline()
            final_file.write(str(line))
        file_from_list.close()
    final_file.close()
    return final_file

save_ids_in_one_file(4)
# request_to_vk = requests.get('https://www.vk.com/catalog.php')
# request_to_vk = ' v'
# #print request_to_vk.status_code
# print BeautifulSoup(request_to_vk.text)
