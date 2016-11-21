#!/usr/bin/env python2
"""Usage: ./parse.py (search-term)

Example: ./parse.py Smith
Example Output:
Smith-Hester, Marla J msmith-hester@unomaha.edu
Smith-Howell, Deborah S dsmith-howell@unomaha.edu
St Pierre Smith, Valerie vstpierresmith@unomaha.edu
Zardetto-Smith, Andrea M azardettosmith@unomaha.edu
"""


import requests
from bs4 import BeautifulSoup
import sys

URL = "http://www.unomaha.edu/search/employee-directory.php"

def search(search_term):
    hmtl = requests.post(URL, {"searchTerms": search_term}).text

    soup = BeautifulSoup(hmtl, 'html.parser')
    names = [x.text for x in soup.select("h5#name")]
    emails = [x.text for x in soup.select("li#email a")]

    return zip(names, emails)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)

    term = sys.argv[1]
    for name, email in search(term):
        print("%s,%s" % (name, email))
