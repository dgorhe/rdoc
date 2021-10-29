#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import json


# In[2]:


# TODO: Automatically get latest versions of all packages


# In[3]:


latest_versions = {
    "ggplot2": "3.3.5",
    "dplyr": "0.7.8",
    "stringr": "1.4.0",
    "tidyverse": "1.3.1",
    "tibble": "3.1.5",
    "odbc": "3.3.5",
    "foreign": "3.3.5",
    "tidyr": "1.1.4",
    "htmlwidgets": "1.5.4",
    "vcd": "1.4-9",
    "xml": "3.99-0.8",
    "jsonlite": "1.7.2",
    "httr": "1.4.2",
    "devtools": "2.4.2",
}


# In[4]:


# Make an array of all package urls based on latest_version
base = "https://www.rdocumentation.org/packages/"
version = "versions/"
urls = [base + key + "/" + version + value for (key, value) in latest_versions.items()]

# GET request for all packges from 
docs = [requests.get(url) for url in urls]

# Parsing and extracting the html
soups = [BeautifulSoup(doc.text, "html.parser") for doc in docs]


# In[5]:


divs = [soup.find_all('div', class_ = "font-bold truncate") for soup in soups]

# Creating dictionary of function names by package
functions = {}
count = 0

for div in divs:
    s = {}
    
    for item in div: 
        f = {}
        
        function = item.find('span').text
        function_url = urls[count] + "/topics/" + function
        sections = BeautifulSoup(requests.get(function_url).text, 'html.parser').find_all('section', class_="")
        function_info = (function, function_url, sections)
        
        if (len(sections) >= 3):
            # Getting function's description
            f["description"] = sections[0].p.text.replace("\n", "")
        
            # Formatting function arguments into string
            args = [x.span.text + " = "  for x in sections[2].find_all('div', class_="font-mono font-bold truncate md:w-3/12 lg:w-2/12")]
            args = ", ".join(args)
            f["formatted_function"] = function + "(" + args + ")"
            
        s[function] = f
        
    functions[list(latest_versions.keys())[count]] = s
    count += 1


# In[6]:


output = json.dumps(functions)

with open("rdoc.json", "w") as f:
    f.write(output)

