import csv
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

browser = webdriver.Chrome('chromedriver.exe')




def diseases_names():
    # get names of diseases from link of disease names A-Z
    for i in range(1):
        matched_elements = browser.get("https://dph.illinois.gov/topics-services/diseases-and-conditions/diseases-a-z-list.html")
    html = browser.page_source
    soup = BeautifulSoup(html)
    # all the div with class names: "cmp_text" include disease names
    all_cmp = soup.find_all("div", {'class': lambda x: x and 'cmp-text' in x.split(" ")})
    result = []
    for i in all_cmp:
        a = i.find_all("a")
        for j in a:
            # add name to the list of diseases names
            result.append(" "+j.text.lower()+" ")
    # get more names of diseases from the database that i use for the header model
    diseases = pd.read_csv('./dataset/training_data.csv')
    # get the names of diseases
    diseases=diseases['prognosis'].unique()
    diseases=[" "+x+" " for x in diseases]
    # concatenation the two list together
    result.extend(diseases)
    return result


# make dataset of diseases names to Integrity check
if __name__ == '__main__':
    # get list of disease names
    diseases=diseases_names()
    # make the dataset rows
    rows = []
    for i in range(len(diseases)):
        rows.append({'diseases':diseases[i]})
    fieldnames=["diseases"]
    # write to the dataset
    with open('word_classification2.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f,fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)