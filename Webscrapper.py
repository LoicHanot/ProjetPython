from bs4 import BeautifulSoup
import time
import re
import os
import logging
import requests
import urllib
import urllib.request
from urllib.parse import urlparse, urljoin
from bs4.element import Comment
from datetime import datetime

internal_urls = set()
external_urls = set()

class repo_init:
    def __init__(self):
        # Obtain timestamp of execution
        date_exec = datetime.now().strftime("%Y%m%d%H%M%S")
        print("date time = ", date_exec)

        # Create necessary directories
        self.path = os.getcwd() + '\\' + date_exec + "_exec"
        try:
            os.mkdir(self.path)
            # LOG_FILENAME = path + '\\' + date_exec + '.log'
            # logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
            #
            # logging.debug("This is the debug logging")
            # os.mkdir(path + "\\images")
            os.mkdir(self.path + "\\texts")
            # os.mkdir(path + "\\misc")
        except OSError:
            logging.debug("Creation of the directory %s failed" % self.path)
        else:
            logging.debug("Successfully created the directory %s " % self.path)

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)

def scrapper(url, img, misc, depth):
    if depth == 0:
        return
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    #html = urllib.request.urlopen(URL).read()
    #print("text from html = " + text_from_html(html))
    text = soup.find_all(text=True)
    print(urlparse(url))
    file = open(repo.path+"\\texts\\" + repo.path +".txt", "w+")
    file.write = soup.get_text()
    print("get text = "+soup.get_text())

    if img == 'Y':
        #get images
        print("récupération des images")
    if misc == 'Y':
        #get misc
        print("récupération du reste")

    #print(get_allwebsite_links(url))
    for link in get_allwebsite_links(url):
        scrapper(link, img, misc, depth-1)
    #Récupère une liste des liens présents dans une page
    #response = requests.get(url)
    #liste_liens = []
    #for ligne in response:
    #    liste_liens.append(ligne.attrs.get('href'))
    #for lien in liste_liens:
    #    return scrapper(lien, img, misc, depth-1)

def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_allwebsite_links(url):
    urls = set()
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # href empty tag
            continue
        # join the URL if it's relative (not absolute link)
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        # remove URL GET parameters, URL fragments, etc.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not is_valid(href):
            # not a valid URL
            continue
        if href in internal_urls:
            # already in the set
            continue
        if domain_name not in href:
            # external link
            if href not in external_urls:
                external_urls.add(href)
            continue
        urls.add(href)
        internal_urls.add(href)
    return urls

if __name__ =="__main__":
    #URL = input("Veuillez entrer l'adresse à aspirer au format HTTP://WWW.ADRESSE.COM : ")

    #try:
    #    response = requests.get(URL)
    #    print(URL + " est valide et existe.")
    #except requests.ConnectionError as exception:
    #    print(URL + " n'existe pas sur internet.")

    repo = repo_init()
    print(repo.path)
    img = input("Voulez-vous récupérer les images [Y/N] ? ")
    misc = input("Voulez-vous récupérer le reste [Y/N] ? ")
    depth = int(input("A quelle profondeur voulez vous aller [1-9]: "))
    scrapper("https://www.zoho.com/fr/writer/", img, misc, depth)


    #for i in range(0,depth):
    #    for l in liste_liens:
    #        scrapper(l)