import threading

from bs4 import BeautifulSoup
import requests
import time
from selenium.webdriver.chrome.service import Service
from selenium import webdriver


# class to object with details
class list_object:
    def __init__(self, item):
        self.item = item
        self.details=False
        self.type=False
    def search(self):
        search = search_object( 'detail', 'text').search_text(self.item)
        self.type, self.details = search.type, search.result

    # convert to json type
    def toJSON(self):
        dict = {"item": self.item,
                "details": self.details,
                "type": self.type}
        return dict


class search_object:
    # init object
    def __init__(self, kind, type):
        # open browser
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        s = Service('chromedriver.exe')
        self.browser = webdriver.Chrome(service=s, options=option)
        self.kind = kind
        self.type = type
        self.result=False

    # convert to json type
    def toJSON(self):
        dict = {"kind": self.kind,
                "type": self.type,
                "result": self.result}
        return dict

    # serch in google search
    def search(self, search_str):
        search_string = search_str.replace(' ', '+')
        self.browser.get("https://www.google.com/search?q=" + search_string)
        html = self.browser.page_source
        # convert to BeautifulSoup type
        return BeautifulSoup(html,features="html.parser")

    # search text by take the text in the header of google search page that apear if the query is accurate
    def search_text(self, search_str):
        query = search_str
        soup = self.search(query)
        # I try to find results 3 times
        for i in range(3):
            # yp1CPe is class name of Summary The first search result from the Internet
            all_yp1CPe = soup.find_all('div', {'class': lambda x: x and 'yp1CPe' in x.split()})
            if (len(all_yp1CPe) > 0):
                # wDYxhc is the text that include the Summary of The first search result from the Internet
                all_wDYxhc = all_yp1CPe[0].select('.wDYxhc')
                if (len(all_wDYxhc) > 0):
                    # check if the text is list
                    all_li = all_wDYxhc[0].find_all('li')
                    if (len(all_li) > 0):
                        list_li = []
                        t = []
                        num = 0
                        for i in all_li:
                            list_li.append(list_object(i.text))
                            t.append(threading.Thread(target=list_li[num].search))
                            t[num].start()

                            num += 1
                            # add details to all the object in the list
                        for tr in t:
                            tr.join()
                        result = []
                        for i in list_li:
                            result.append(i.toJSON())

                        self.type, self.result = 'list', result

                        return self
                    # check if the text is a table
                    all_td = all_wDYxhc[0].find_all('td')
                    if (len(all_td) > 0):
                        dict_td = dict()
                        i = 0
                        num = 0
                        while i < len(all_td):
                            i = i + 1
                            t = []
                            if (all_td[i + 1].text in dict_td):
                                j = 1
                                while all_td[i + 1].text + ' ' + str(j) in dict_td:
                                    j += 1
                                # add details to all the object in the table

                                dict_td[all_td[i + 1].text + ' ' + str(j)] = list_object(all_td[i].text)
                                t.append(
                                    threading.Thread(target=dict_td[all_td[i + 1].text + ' ' + str(j)].search, arg=()))
                                t[num].start()
                                num += 1
                            else:
                                # add details to all the object in the table
                                dict_td[all_td[i + 1].text] = list_object(all_td[i].text)

                                t.append(threading.Thread(target=dict_td[all_td[i + 1].text].search(), arg=()))
                                t[num].start()
                                num += 1

                            i = i + 2
                        for tr in t:
                            tr.join()
                        for i in dict_td:
                            i = i.toJSON()
                        self.type, self.result = 'dict', dict_td
                        return self
                    # check if the text is a text that represented by span
                    all_span = all_wDYxhc[0].find_all('span')
                    if (len(all_span) > 0):
                        all_text = ''
                        text = all_span
                        for info in text:
                            all_text += " " + info.text
                        self.type, self.result = 'text', all_text
                        return self

                    # check if the text is a text that represented by div
                    all_div = all_wDYxhc[0].find_all('div')
                    if (len(all_div) > 0):
                        all_text = ''
                        text = all_div
                        for info in text:
                            all_text += " " + info.text
                        self.type, self.result = 'text', all_text
                        return self

            # Wt5Tfe is query that close to the meaning of the orginal query
            all_Wt5Tfe = soup.find_all('div', {'class': lambda x: x and 'Wt5Tfe' in x.split()})
            if (len(all_Wt5Tfe) > 0 and len(all_Wt5Tfe[0].select('.wQiwMc')) > 0):
                # query is the new search
                query = all_Wt5Tfe[0].select('.wQiwMc')[0].select('span')[0].text
                # search the new query
                soup = self.search(query)
            else:
                break
        # if the program did not found results
        self.type, self.result = False, False
        return self

    # search images by google image search
    def search_image(self, search_query):
        search_url = f"https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&q={search_query}"
        images_url = []
        # open browser and begin search
        self.browser.get(search_url)

        html = self.browser.page_source
        soup = BeautifulSoup(html)

        elements = soup.find_all('img', {'class': lambda x: x and 'rg_i' in x.split()})
        count = 0
        # find maximoom 5 image and return
        for e in elements:
            images_url.append(e['src'])
            count += 1
            if count == 5:
                break
        self.type, self.result = 'image', images_url
        return self

    # search link by googleSearch tool
    def search_links(self, search_str):
        from googlesearch import search
        query = search_str
        my_results_list = []
        # find 10 first links
        for i in search(query,  # The query you want to run
                        tld='com',  # The top level domain
                        lang='en',  # The language
                        num=10,  # Number of results per page
                        start=0,  # First result to retrieve
                        stop=10,  # Last result to retrieve
                        pause=2.0,  # Lapse between HTTP requests
                        ):
            my_results_list.append(i)
        if (len(my_results_list) > 0):
            self.type, self.result = 'link', my_results_list
            return self
        self.type, self.result = False, False
        return self

    # search defination by google search and wikipedia
    def search_defination(self, query):
        # search wikipedia for the any term
        wikipedia_api_link = "https://en.wikipedia.org/w/api.php?format=json&action=query&list=search&srsearch="
        search_term = query
        url = wikipedia_api_link + search_term
        # get the url of the first article that the search provides
        r = ''
        while r == '':
            try:
                r = requests.get(url)
                break
            except:
                print("Connection refused by the server..")
                print("Let me sleep for 5 seconds")
                print("ZZzzzz...")
                time.sleep(5)
                print("Was a nice sleep, now let me continue...")
                continue
        json_output = r.json()
        # if block by netfree
        if ("blockByNetFree" in json_output):
            dict = {"item": self.search_text(query).result,
                    "details": False,
                    'type': 'text'}
            self.type, self.result = 'list', [dict]
            return self
        if not json_output['query']['search']:
            dict = {"item": self.search_text(query).result,
                    "details": False,
                    'type': 'text'}
            self.type, self.result = 'list', [dict]
            return self
        article_title = json_output['query']['search'][0]['title']
        article_title = article_title.replace(' ', '_')
        wikipedia_link_article = "https://en.wikipedia.org/wiki/" + article_title

        # scrape the HTML content from the page
        def request_webpage(url):
            res = ''
            while res == '':
                try:
                    res = requests.get(url)
                    break
                except:
                    print("Connection refused by the server..")
                    print("Let me sleep for 5 seconds")
                    print("ZZzzzz...")
                    time.sleep(5)
                    print("Was a nice sleep, now let me continue...")
                    continue

            try:
                res.raise_for_status()
            except:
                print('There is a problem with the request')
            return res

        page = request_webpage(wikipedia_link_article)
        bs_page = BeautifulSoup(page.text, 'html.parser')
        # get only specific HTML tags
        tags = bs_page.find_all(["h1", "h2", "p"])
        # extract the text from these tags
        text = ''
        for tag in tags:
            text += tag.getText()
        # sanitation
        import re
        # replace new lines
        text = text.replace('\n', ' ').replace('\r', ' ')
        # remove non-ascii characters
        import string
        printable = set(string.printable)
        ''.join(filter(lambda x: x in printable, text))
        # use regex to remove '[x]' -
        # reference links in the wikipedia text
        text = re.sub(r'\[\d+?\]', '', text)
        # separate into list of sentences
        text = re.sub(r'[.\?!]', "#eos#", text)
        sentences = text.split('#eos#')
        sentences = [item.strip() + '.' for item in sentences]

        # limit the len to 400 words
        MAX_LEN = 400

        paragraphs = ['']
        x = 0
        for sentence in sentences:
            sentence_len = len(sentence.split())
            paragraph_len = len(paragraphs[x].split())
            if (paragraph_len + sentence_len) <= MAX_LEN:
                paragraphs[x] += ' ' + sentence
            else:
                paragraphs.append(sentence)
                x += 1
        paragraphs = ' '.join(paragraphs)
        # convert to json type
        dict = {"item": self.search_text(query).result,
                "details": paragraphs,
                'type': 'text'}
        self.type, self.result = 'list', [dict]
        return self
