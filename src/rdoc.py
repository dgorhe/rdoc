#!/usr/bin/python
# encoding: utf-8

import sys
import json
from workflow import Workflow3, web

with open("./rdoc.json", "r") as f:
    rdoc = json.load(f)

__version__ = '0.1'

def main(wf):
    def search(query):
        if (len(query)):
            url = create_url(query)
            desc = rdoc[query[0]][query[1]]["description"]
            formatted = rdoc[query[0]][query[1]]["formatted_function"]

            wf.add_item(desc, "Description", largetext=desc)
            wf.add_item(formatted, "Formatted Function", copytext=formatted)
            wf.add_item("See more", url, arg=url, valid=True)
        else:
            print("Query not correct")
            
        wf.send_feedback()
        return url

    def create_url(query):
        package = query[0]
        version = latest_versions[query[0]]
        function = query[1]
        url = "https://rdocumentation.org/"
        url += "packages/" + package + "/"
        url += "versions/" + version + "/"
        url += "topics/" + function

        return url
    
    # TODO: Give results in Alfred with various options
    
    search(wf.args)


if __name__ == u'__main__':
    wf = Workflow3(libraries=['./lib'])
    sys.exit(wf.run(main))
