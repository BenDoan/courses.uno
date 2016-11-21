## unomaha-teacher-directory-parser

Parses the api at [http://www.unomaha.edu/search/employee-directory.php](http://www.unomaha.edu/search/employee-directory.php). Given a search term, the script will output to stdout a csv of matching teachers with a name and email.

```
Usage: ./parse.py (search-term)

Example: ./parse.py Smith
Example Output:
Smith-Hester, Marla J msmith-hester@unomaha.edu
Smith-Howell, Deborah S dsmith-howell@unomaha.edu
St Pierre Smith, Valerie vstpierresmith@unomaha.edu
Zardetto-Smith, Andrea M azardettosmith@unomaha.edu
```
