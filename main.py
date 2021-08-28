import requests
from bs4 import BeautifulSoup
import re
from requests_html import HTML
from requests_html import HTMLSession
import urllib

def get_source(url): 
        session = HTMLSession()
        response = session.get(url)
        return response

def scrape_google(query):

    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.co.uk/search?q=" + query)

    links = list(response.html.absolute_links)
    google_domains = ('https://www.google.', 
                      'https://google.', 
                      'https://webcache.googleusercontent.', 
                      'http://webcache.googleusercontent.', 
                      'https://policies.google.',
                      'https://support.google.',
                      'https://maps.google.')

    for url in links[:]:
        if url.startswith(google_domains):
            links.remove(url)

    return links


def comment_remover(text):
    def replacer(match):
        s = match.group(0)
        if s.startswith("/"):
            return " "
        else:
            return s

    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE,
    )
    return re.sub(pattern, replacer, text)

URL = scrape_google('palindrome number program java geeksforgeeks')
print(URL[0])
r = requests.get(URL[0])
soup = BeautifulSoup(r.content, "html.parser")

table = soup.find("div", attrs={"class": "code-container"})
sp = re.compile("[@$///*\;}{]")
print("--------------------------------")
output = ""
for row in table.findAll("code"):
    if (sp.search(row.text) == None):
        output += row.text +" "
    else:
        output += row.text+'\n'

print(comment_remover(output))
