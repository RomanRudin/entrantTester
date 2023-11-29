from bs4 import BeautifulSoup
import requests

class Parser():
    def __init__(self, url='', file_name='') -> None:
        self.content = self.__set_content(file_name)
        self.soup = BeautifulSoup(self.content, 'lxml')

        self.me = 0
        self.full_search_mode = False
        self.place = 0

        self.unique = self.__get_unique()

        
    def set_me(self, number):
        self.me = number
        
    def set_place(self, number):
        self.place = number


    def __get_content(self, url):
        return requests.get(url).text

    def __set_content(self, file_name):
        with open(f'{file_name}.html', encoding='utf-8') as file:
            return file.read()


    def clear_unique(self):
        with open('unique_entrants.txt', 'w') as file:
            file.write('')
            self.unique = []


    def save_unique(self):
        with open('unique_entrants.txt', 'a') as file:
            file.write('\n'.join(self.unique))

    
    def __get_unique(self):
        with open('unique_entrants.txt', 'r') as file:
            return file.read().splitlines()

        
    def start(self):
        info_table = self.soup.find(id='info-table')
        entrants_tags = info_table.find_all('tr')
        entrants_tags.pop(0)
        entrants = []
        original_entrants = []
        pool = []
        if self.full_search_mode:
            max_order = 5
        for entrant in entrants_tags:
            data = list(entrant.find_all('span'))
            needed_data = {
                'order':  int(data[2].get_text().lstrip().rstrip()),
                'document': data[1].get_text().lstrip().rstrip(),
                'points': int(data[8].get_text().lstrip().rstrip()),
                'service': data[12].get_text().lstrip().rstrip(),
                'is_original': any(data[i].get_text().lstrip().rstrip() == 'Да' for i in (10, 11))
            }
            if not needed_data['document'] in self.unique:
                pool.append(needed_data)
            if needed_data['document'] == self.me and not self.full_search_mode: 
                max_order = needed_data['order']
                break
        flag = True
        for index_order in range(1, max_order + 1):
            if flag:
                for entrant in pool:
                    if entrant['order'] == index_order:
                        entrants.append(entrant)
                        if entrant['is_original']:
                            original_entrants.append(entrant)
                        if entrant['document'] == self.me:
                            flag = False
                            break
            else: break
        for i in range(min(self.place, len(pool))):
            self.unique.append(pool[i]['document'])
        return [len(entrants), entrants], [len(original_entrants), original_entrants]