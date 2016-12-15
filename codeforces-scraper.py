import requests, bs4, csv

#dicts to hold submission ids
submission_ids = []

PROBLEM_NUMBER = '282'
PROBLEM_LETTER = 'A'
SUBMISSION_LANGUAGE = 'Python 3'

#gets data from page
res = requests.get('http://codeforces.com/problemset/status/'+PROBLEM_NUMBER+'/problem/'+PROBLEM_LETTER+'/page/1?order=BY_PROGRAM_LENGTH_ASC')

#check if the download succeeded 
try:
    res.raise_for_status()
except Exception as exc:
    print('There was a problem: {}'.format(exc))

#turn the context (res.text) into a BeautifulSoup object
site_content = bs4.BeautifulSoup(res.text, "html.parser")

#gets the number of the last page, used for looping through
elems = site_content.select('div > ul > li > span[class=page-index]')

num_pages = int(elems[-1].getText())

for i in range(1,num_pages+1):
    
    #gets data from page
    res = requests.get('http://codeforces.com/problemset/status/'+PROBLEM_NUMBER+'/problem/'+PROBLEM_LETTER+'/page/'+str(i)+'?order=BY_PROGRAM_LENGTH_ASC')

    #check if the download succeeded 
    try:
        res.raise_for_status()
    except Exception as exc:
        print('There was a problem: {}'.format(exc))

    #turn the context (res.text) into a BeautifulSoup object
    site_content = bs4.BeautifulSoup(res.text,"html.parser")

    #want every table row (tr) element with a data-submission-id attribute
    elems = site_content.select('tr[data-submission-id]')

    #iterate over every element grabbing the submission ids
    #only grabs the submissions from the desired language
    for j in range(len(elems)):
        if SUBMISSION_LANGUAGE in elems[j].getText():
                submission_ids.append(elems[j].attrs['data-submission-id'])
                
    print("page {}/{}, total submissions found: {}".format(i,num_pages,len(submission_ids)))

#opening a csv file for submissions to be written to
csvfile = open('codeforces/submissions'+PROBLEM_NUMBER+PROBLEM_LETTER+SUBMISSION_LANGUAGE.replace(" ", "")+'.csv','w+',encoding='utf-8',newline='')
csvwriter = csv.writer(csvfile)

#loop through list of submission ids, get the actual submission text and write to csv file
for i in range(len(submission_ids)):
    
    #open submission page
    res = requests.get('http://codeforces.com/contest/'+PROBLEM_NUMBER+'/submission/'+str(submission_ids[i]))
    
    #check if the download succeeded 
    try:
        res.raise_for_status()
    except Exception as exc:
        print('There was a problem: {}'.format(exc))
        
    #turn the context (res.text) into a BeautifulSoup object
    site_content = bs4.BeautifulSoup(res.text,"html.parser")
    
    #actual submission inside denoted by the <pre class="prettyprint program-source".
    elems = site_content.find_all("pre", { "class" : "prettyprint program-source" })
    
    print("writing submission {}/{}, submission_id = {}".format(i+1,len(submission_ids),submission_ids[i]))
    
    #write to csv file with start and end markers
    csvwriter.writerow(["~~start~~"+elems[0].getText()+"~~end~~"])

#close the csv file
csvfile.close()