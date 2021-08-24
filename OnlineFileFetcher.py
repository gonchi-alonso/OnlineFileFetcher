#IMPORT PACKAGES AND MODULES
#to get pdf files 
import requests
#for tree traversal scraping in webpage
from bs4 import BeautifulSoup
#to download the files
import urllib.request
#to store the files with date
import time
#to create directories
import os
import glob
import pdfkit 
import shutil
import pandas as pd
 


# =============================================================================
# This program is used to download all files from a specific website. In order
# to run it, you will need to put a valid adress into the strFiles, and input
# the desired URL. Some websites were provided to use as a test run.
# =============================================================================

#input below the desired location for the files
strFiles = r'input here the complete path for your folder location where you want the files stored'
 
#MAIN BODY
#choose url to fetch
#url = "https://weeklyjoys.wordpress.com/category/phys-241/"
#url = "https://www.ohio.edu/mechanical/thermo/property_tables/H2O/"
url = 'http://markets.cboe.com/us/futures/notices/margin_updates'


#FUNCTION DEFINITIONS
#to shorten urls to concatenate with shortcuts
def shortenurl(url):
    test_url = str(url)
    counter = 0
    while counter == 0:
        if test_url.endswith('/'):
            counter = 1
        else:
            test_url = test_url.rstrip(test_url[-1])    
    print(url)
    return(test_url)    
 
 
 
def html2PDF(date_string, count):    
    #Create a path for the executable file
    path_wkhtmltopdf = r"D:\wkhtmltopdf\bin\wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    dirName = 'Files/pdf_{}'.format(date_string)
    # Create target directory & all intermediate directories if don't exists
    os.makedirs(dirName, exist_ok=True)
    #Create an empty list to use later in the loop
    newList=[]

    for filename in glob.iglob(strFiles + '\html_{}\*.html'.format(date_string)):
        newList.append(filename)
        pdfkit.from_file(newList, strFiles + '\pdf_{}\pdf{}.pdf'.format(date_string, count), configuration=config)
    shutil.rmtree(strFiles + '\html_{}'.format(date_string))
 
 
 
def csv2PDF(date_string, count): 
    csv_file = pd.read_csv(strFiles + '\csv_{}\csv.csv'.format(date_string))
    # to save as html file
    dirName = 'Files/html_{}'.format(date_string)
    # Create target directory & all intermediate directories if don't exists
    os.makedirs(dirName, exist_ok=True)
    csv_file.to_html(strFiles + '\html_{}\trip.html'.format(date_string))
    html2PDF(date_string, count)
    shutil.rmtree(strFiles + '\csv_{}'.format(date_string))
 
 
 
#parse website opening all "a" tags
def getpdfs(url):    
    #to get url from requests.get
    read = requests.get(url)
    #full html content
    html_content = read.content
    #parse html
    soup = BeautifulSoup(html_content, "html.parser")
    #to save with date and time
    date_string = time.strftime("%m_%d_%Y")
    #aesthetics for record
    print("\n")
    print("Website to fetch from:\n")
    #call of shortening function
    test_url = shortenurl(url)
    #aesthetics for record
    print("\n")
    #to keep track of number documents
    count = 0
    #to count every document type independently
    count_pdf = 0
    count_csv = 0
    count_html = 0
    #aesthetics for record 
    print("Downloading and Archiving the following files: \n")
    #initialize variable
    typelink = str(".")
    #parse website opening all "a" tags
    for link in soup.find_all('a'):
        #stores one link per iteration
        link_store = str(link.get('href'))
        #print('{}'.format(link_store))
        #finds if link is one of the desired formats
        if link_store.endswith('.pdf'):
            typelink = str("pdf")
        elif link_store.endswith('.html'):
            typelink = str("html")
        elif link_store.endswith('.csv'):
            typelink = str("csv")
        else:
            typelink = str(".noneexist")
        #finds hyperlinks with pdf/csv/html files
        if link_store.endswith(".{}".format(typelink)):
            #identifies if the urls have been shortened
            if link_store.startswith('http'):
                link_store = link_store
            #fixes shortcut urls
            else:
                link_store = (test_url + link_store)
            #counts total number of documents
            count = count + 1
            #prints the selectted files' urls
            print(link_store)
            #downloads and stores urls sorting by type
            if link_store.endswith(".pdf"):
                dirName = 'Files/{}_{}'.format(typelink, date_string)
                # Create target directory & all intermediate directories if don't exists
                os.makedirs(dirName, exist_ok=True)  
                urllib.request.urlretrieve('{}'.format(link_store), strFiles + '\{}_{}\{}_{}'.format(typelink, date_string, typelink, count_pdf)+ ".{}".format(typelink))
                count_pdf = count_pdf + 1
            elif link_store.endswith(".csv"):
                dirName = 'Files/{}_{}'.format(typelink, date_string)
                # Create target directory & all intermediate directories if don't exists
                os.makedirs(dirName, exist_ok=True) 
                urllib.request.urlretrieve('{}'.format(link_store), strFiles + '\{}_{}\{}'.format(typelink, date_string, typelink)+ ".{}".format(typelink))
                csv2PDF(date_string, count)
                count_csv = count_csv + 1
            elif link_store.endswith(".html"):
                dirName = 'Files/{}_{}'.format(typelink, date_string)
                # Create target directory & all intermediate directories if don't exists
                os.makedirs(dirName, exist_ok=True) 
                urllib.request.urlretrieve('{}'.format(link_store), strFiles + '\{}_{}\{}_{}'.format(typelink, date_string, typelink, count_html)+ ".{}".format(typelink))
                html2PDF(date_string, count)
                count_html = count_html + 1

       # else: 
           # if link_store.startswith(url):
            #    getpdfs(link_store)
    print("\n{} Documents downloaded and stored:".format(count))
    print("   -{} PDFs ".format(count_pdf))
    print("   -{} CSVs ".format(count_csv))
    print("   -{} HTMLs ".format(count_html))
 

#time process
start_time = time.time()
#function call
getpdfs(url)
#print timer results
print("\nElapsed time: %s seconds" % (time.time() - start_time))