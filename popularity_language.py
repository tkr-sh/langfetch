# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib.request as urllib2
import urllib.parse as parse
from tqdm import tqdm
from json import dumps, loads



def remove_popularity():

    """ Remove the popularity from the file """

    # Get the content of the file
    with open("src/languages.json", "rt") as FILE_JSON:
        LANGUAGES_JSON = loads(FILE_JSON.read())

    for k,data in LANGUAGES_JSON.items():
        if "popularity" in LANGUAGES_JSON[k]:
            del LANGUAGES_JSON[k]["popularity"]

    # Write that to the file
    with open("src/languages.json", "wt") as FILE_JSON:
        FILE_JSON.write(dumps(LANGUAGES_JSON, indent=4))




def get_nb_traduction(title: str):

    """ Get the number of traductions for the title """

    URL = f'http://en.wikipedia.org/wiki/{parse.quote(title)}'
    file = BeautifulSoup(urllib2.urlopen(URL), 'html.parser').prettify().splitlines()

    tot = sum(map(lambda l: "interlanguage-link interwiki" in l, file))

    return tot




corr = {
    "sass": "scss",
    "typescript": "TypeScript",
    "ghc": "Glasgow Haskell Compiler",
    "gcc": "GNU Compiler Collection",
    "deno": "Deno (software)"
}



def add_popularity():

    """ Add the popularity field for each languages by getting the number of traductions """

    # Get the content of the JSON
    with open("src/languages.json", "rt") as FILE_JSON:
        LANGUAGES_JSON = loads(FILE_JSON.read())

    # Get the number of traduction for each languages
    for k,data in tqdm(LANGUAGES_JSON.items()):
        n = 0

        try:
            n = get_nb_traduction(k.replace("#", " Sharp") + " (programming language)")
        except Exception:
            try:
                n = get_nb_traduction(corr.get(k,k).replace("#", " Sharp"))
            except Exception:
                pass

        LANGUAGES_JSON[k]["popularity"] = n

    LANGUAGES_JSON = {k:v for k,v in sorted(LANGUAGES_JSON.items(), key=lambda e:e[0])}

    # Print the languages:
    print("\033[36m>\033[0m Here is the list of the languages sorted by popylarity:")
    for k,v in sorted(LANGUAGES_JSON.items(), key=lambda e: -e[1]["popularity"]):
        print(f"-> {k}: {v['popularity']}")

    # Write them to the file
    with open("src/languages.json", "wt") as FILE_JSON:

        try:
            FILE_JSON.write(dumps(LANGUAGES_JSON, indent=4))
            print("\033[32m+\033[0m Popularity wrote to the file.")
        except Exception as e:
            print("\033[31m-\033[0m An error occured while trying to store the languages in the file.")
            raise Exception(e)

add_popularity()
