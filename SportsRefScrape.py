#This is a scraping functions file!


#Importing the packages
import pandas as pd
import requests
from bs4 import BeautifulSoup, Comment


#Functions I needLink 
def PlayerNameToLink(FullName):
    '''
    Parameters
    ----------
    string : string
        A player's full name.
    Returns : Link
        A player's Link
    -------
    '''
    FullName = FullName.lower()
    #So first things first I need to replaces the name's spaces with -
    FullName = FullName.replace(" ", "-") 
    #Now I will just take out special characters
    if "'" in FullName:
        FullName = FullName.replace("'", "") 
    if "." in FullName:
        FullName = FullName.replace(".", "") 
    if "-jr" in FullName:
        FullName = FullName.replace("-jr", "jr") 
    if "-iv" in FullName:
        FullName = FullName.replace("-iv", "iv") 
    if "-iii" in FullName:
        FullName = FullName.replace("-iii", "iii") 
    if "-ii" in FullName:
        FullName = FullName.replace("-ii", "ii") 
    #This should be better done to account for edge cases
    Link = "https://www.sports-reference.com/cbb/players/"+FullName+ "-1.html" #Now this means duplicate players are not gonna work but I doubt that is an issue
    
    #Stupid Edge Cases;
    if Link == 'https://www.sports-reference.com/cbb/players/jordan-brown-4-1.html':
        Link = 'https://www.sports-reference.com/cbb/players/jordan-brown-4.html'   
    if Link == 'https://www.sports-reference.com/cbb/players/branden-johnson-2-1.html':
        Link = 'https://www.sports-reference.com/cbb/players/branden-johnson-2.html'
    if Link == 'https://www.sports-reference.com/cbb/players/kevin-easleyjr-1.html':
        Link = 'https://www.sports-reference.com/cbb/players/kevin-easley-2.html'
    if Link == 'https://www.sports-reference.com/cbb/players/justice-sueing-1.html':
        Link = 'https://www.sports-reference.com/cbb/players/justice-sueing-2.html'
    if Link == 'https://www.sports-reference.com/cbb/players/chris-clarke-1.html':
        Link = 'https://www.sports-reference.com/cbb/players/chris-clarke-2.html'
    if Link == 'https://www.sports-reference.com/cbb/players/james-banks-1.html':
        Link = 'https://www.sports-reference.com/cbb/players/james-banksiii-1.html'
    return Link

def TeamNameToLink_basic(TeamName, Season):
    '''
    Parameters
    ----------
    string : 2 strings
        A TeamName and a season
    Returns : id
        A TeamName's Link
    -------
    '''
    TeamName = TeamName.lower()
    #So first things first I need to replaces the name's spaces with -
    TeamName = TeamName.replace(" ", "-")
    Link = "https://www.sports-reference.com/cbb/schools/"+TeamName+"/"+Season[:2]+Season[-2:]+".html" #Now this means duplicate players are not gonna work but I doubt that is an issue
    if "-/oo" in Link:
        Link = 'unknown'
        raise ValueError('Unknown team name')
    Link = ValidateUrl(Link, TeamName, Season)[0]
    return Link

def TeamName_to_historyLink(TeamName):
    TeamName = TeamName.lower()
    #So first things first I need to replaces the name's spaces with -
    TeamName = TeamName.replace(" ", "-")
    link = 'https://www.sports-reference.com/cbb/schools/'+TeamName+'/'
    #Validate 
    response = requests.get(link)
    link = link
    if(response.status_code != 200):
        print("Url for "+TeamName+" does not exist. Please fix it: ")
    return link

def ScrapeSportsRefWebPage(Link):
    '''
    Parameters
    ----------
    Link : String
        The Link to the webpage
    Returns
    -------
    tables : List of DFs
        A list of all the tables on the webpage
    '''
    page = Link
    try:
        headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"}
        page = Link
        pageTree = requests.get(page, headers=headers)
        pageSoup = BeautifulSoup(pageTree.content, 'html.parser')
        comments = pageSoup.find_all(string=lambda text: isinstance(text, Comment))
        
        tables = []
        for each in comments:
            if 'table' in each:
                try:
                    tables.append(pd.read_html(each)[0])
                    #In the df delete the last line
                except:
                    continue
                
        tables.append(pd.read_html(page)[0])
    except:
        headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"}
        page = input("There was an error with this link: "+page+" Please enter a working link and hard code the name if necessary: ")
        pageTree = requests.get(page, headers=headers)
        pageSoup = BeautifulSoup(pageTree.content, 'html.parser')
        comments = pageSoup.find_all(string=lambda text: isinstance(text, Comment))
        
        tables = []
        for each in comments:
            if 'table' in each:
                try:
                    tables.append(pd.read_html(each)[0])
                    #In the df delete the last line
                except:
                    continue
                
        tables.append(pd.read_html(page)[0])
    return tables

def TransferStatus(ListOfDFs):
    '''
    Parameters
    ----------
    ListOfDFs : List
        It is a list of all the DFS scraped off the player page
    Returns
    -------
    list
        Has in order the last seasson, new season, last school, new school
    '''
    df = ListOfDFs[0]
    Season = df["Season"].tolist()
    School = df["School"].tolist()
    for i in range(1, len(School)):
        if(School[i]!=School[i-1]):
            lastSzn = Season[i-1]
            newSzn = Season[i]
            lastSchool = School[i-1]
            newSchool = School[i]
            break
    try:
        return [lastSzn, newSzn, lastSchool, newSchool]
    except UnboundLocalError:
        return 'Not appropriate call for function'
def GetGameLog(FullName):
    FullName = FullName.lower()
    #So first things first I need to replaces the name's spaces with -
    FullName = FullName.replace(" ", "-")
    Link = "https://www.sports-reference.com/cbb/players/"+FullName+"-1/gamelog/"
    if Link == 'https://www.sports-reference.com/cbb/players/jordan-brown-1/gamelog/':
        Link = 'https://www.sports-reference.com/cbb/players/jordan-brown-4/gamelog/l'   
    if Link == 'https://www.sports-reference.com/cbb/players/branden-johnson-1/gamelog/':
        Link = 'https://www.sports-reference.com/cbb/players/branden-johnson-2/gamelog/'
    if Link == 'https://www.sports-reference.com/cbb/players/kevin-easleyjr-1/gamelog/':
        Link = 'https://www.sports-reference.com/cbb/players/kevin-easley-2/gamelog/'
    if Link == 'https://www.sports-reference.com/cbb/players/justice-sueing-1/gamelog/':
        Link = 'https://www.sports-reference.com/cbb/players/justice-sueing-2/gamelog/'
    if Link == 'https://www.sports-reference.com/cbb/players/chris-clarke-1/gamelog/':
        Link = 'https://www.sports-reference.com/cbb/players/chris-clarke-2/gamelog/'
    if Link == 'https://www.sports-reference.com/cbb/players/james-banks-1/gamelog/':
        Link = 'https://www.sports-reference.com/cbb/players/james-banksiii-1/gamelog/'
    df = pd.read_html(Link)[0]
    df.drop(df[df["Date"]=="Date"].index, inplace = True)
    df = df[:-1]
    return df

def ValidateUrl(link, obj, szn):
    i = 0
    works = False
    while(works == False):
        if(i>0):
            link = input("Enter the fixed link: ")
            obj = input("Enter adjusted name(Helpful when uploading data): ")
        response = requests.get(link)
        link = link
        if(response.status_code != 200):
            print("Url for "+obj+"("+str(szn)+") does not exist. Please fix it: ")
            i += 1
            continue
        break
    return [link, obj]
    
 
player = 'James Banks'
l = PlayerNameToLink(player)
n = ScrapeSportsRefWebPage(l)[3]
row = n[n['School'] == 'Texas'].values[-1].tolist()[19]
'''
szn = '2017-18'
l = TeamNameToLink_basic('penn state', szn)
n =  ScrapeSportsRefWebPage(l)[0]
row = n[n['Player'] == 'School Totals']
possG = ((row['FGA']-row['ORB'])+row['TOV']+0.44*row['FTA'])/row['G']
possG = possG.tolist()[0]
'''  
