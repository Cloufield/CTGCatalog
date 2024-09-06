import sys
import os
import shutil
import pandas as pd

def cite(x):
    pmid = x["PMID"]
    try:
        authors_list = x["Authors"].split(",")
        if len(authors_list) < 5:
            authors_string =  ", ".join( [ author  for author in authors_list])
        else:
             authors_string = ", ".join( authors_list[0:4] + ["...&"]  + [authors_list[-1]] )
    
        authors = authors_string
    except:
        authors=""
    try:
        title = x["TITLE"]
    except:
        title=""
    try:
        journal = x["ISO"]
    except:
        journal=""
    try:
        page = x["PAGE"]
    except:
        page=""
    if x["DOI"] is not None:
        doi = "doi:{}.".format(x["DOI"])
    else:
        doi=""
    try:
        year =  x["YEAR"]
    except:
        year = ""
    try:
        volume = x["VOLUME"]
    except:
        volume = ""
    try:
        issue = "({})".format(x["ISSUE"])
    except:
        issue = ""
    citation = "{authors}. ({year}) {title} {journal}, {volume} {issue} {page}. {doi} PMID {pmid}".format(authors=authors,
                                                                                                               year=year,
                                                                                                               title=title,
                                                                                                               journal=journal,
                                                                                                               volume=volume,
                                                                                                               issue=issue,
                                                                                                               page=page,
                                                                                                               doi=doi,
                                                                                                               pmid=pmid)
    return citation