import requests, bs4, csv, json, time

CONTEST_ID = 1
TARGET_PROBLEM = 'Theatre Square'
TARGET_LANGUAGE = 'GNU C'
start = 1
count = 100

OK = 0
WRONG_ANSWER = 0
COMPILATION_ERROR = 0
OTHER = 0

while OK < 3950:
    
    url = 'http://codeforces.com/api/contest.status?contestId={}&from={}&count={}'.format(CONTEST_ID, start, count) 
    start += count
    
    res = requests.get(url)

    try:
        res.raise_for_status()
    except Exception as exc:
        print("There was a problem: {}".format(exc))

    soup = bs4.BeautifulSoup(res.text,"html.parser")

    newDictionary=json.loads(str(soup))

    print("Chunk: {}".format(start))
    
    for r in newDictionary['result']:
                      
        if r['problem']['name'] == TARGET_PROBLEM and r['programmingLanguage'] == TARGET_LANGUAGE:
            #time.sleep(0.1)
            if r['verdict'] == 'OK':
                OK += 1
                with open('codeforces/submission_ids_OK.csv', 'a', encoding='utf-8', newline='') as f:
                    f.write("{},{}\n".format(r['id'],r['verdict']))
            elif r['verdict'] == 'WRONG_ANSWER':
                WRONG_ANSWER += 1
                with open('codeforces/submission_ids_WA.csv', 'a', encoding='utf-8', newline='') as f:
                    f.write("{},{}\n".format(r['id'],r['verdict']))
            elif r['verdict'] == 'COMPILATION_ERROR':
                COMPILATION_ERROR += 1
                with open('codeforces/submission_ids_CE.csv', 'a', encoding='utf-8', newline='') as f:
                    f.write("{},{}\n".format(r['id'],r['verdict']))
            else:
                OTHER += 1
                with open('codeforces/submission_ids_OTHR.csv', 'a', encoding='utf-8', newline='') as f:
                    f.write("{},{}\n".format(r['id'],r['verdict']))
            print("OK: {}, WA: {}, CE: {}, OTHR: {}".format(OK, WRONG_ANSWER,COMPILATION_ERROR,OTHER))
    

    
