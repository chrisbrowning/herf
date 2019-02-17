from bs4 import BeautifulSoup
import urllib
import csv
import re

aaaa

titles = [['Body:=','body'],['Size:','size'],['Ring Gauge:','size'],
        ['Length:','length'],['Filler:','filler'],['Binder:','binder'],
        ['Wrapper:','wrapper'],['Issue:','issue'],['Price:','price']]

fieldnames = ['cigar_name','score','taste_note','body','size','ring', 'length',
            'filler', 'binder', 'wrapper', 'issue', 'price']
cigars = []
xmin = 1000
xmax = 19400
s = ''

def open_page(target):
    r = urllib.urlopen(target).read()
    soup = BeautifulSoup(r,"html.parser")
    if soup is not None:
        if soup.title.string != "Page Not Found":
            return soup

def clean_html_tags(raw):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw)
    return cleantext

def get_cigar_name(soup):
    raw_cigar_name = soup.find_all("div", class_="tn-title")[0].get_text()
    cigar_name = raw_cigar_name.split("|")[1].strip().encode('utf-8')
    return cigar_name

def get_attrs(text):
    attrs = dict()
    attr_list = text[0].find_all("ul", "list-inline")[0]
    for title in titles:
        attrs[title[1]] = ''
        if title[0] in str(attr_list):
            offset = len(title[0] + "</strong>")
            attr_idx = str(attr_list).find(title[0])
            raw = str(attr_list)[attr_idx+offset:]
            clean = raw.split("</li>")[0]
            attrs[title[1]] = clean
    return attrs

def write_csv(cigars,xmin,xmax):
    with open(str(xmin) + '_' + str(xmax-1) + '_cigars.csv', 'wb') as datafile:
        writer = csv.DictWriter(datafile, fieldnames=fieldnames)
        writer.writeheader()
        for c in cigars:
            writer.writerow(c)

def scrape(target):
    cigar = dict()
    soup = open_page(target)
    if soup is None:
        return None
    cigar_name = get_cigar_name(soup)
    cigar['cigar_name'] = cigar_name
    score = soup.find_all("div", class_="tn-extras_score-number")[0].get_text()
    cigar['score'] = score
    text = soup.find_all("div", class_="tn-text")
    taste_note = clean_html_tags(str(text[0].find_all("p")[0])).split(':')[1].strip()
    cigar['taste_note'] = taste_note
    attrs = get_attrs(text)
    cigar.update(attrs)
    return cigar




for x in range(xmin,xmax):
    try:
        s = scrape('http://www.cigaraficionado.com/cigars/detail/source/search/note_id/' + str(x))
    except (RuntimeError, TypeError):
        pass
    if s is None:
        continue
    cigars.append(s)
write_csv(cigars,xmin,xmax)
