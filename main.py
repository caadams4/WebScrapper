import requests
from bs4 import BeautifulSoup
import json

i = 270867
global courseID


def getID(i):
    URL = "https://catalog.udel.edu/preview_course.php?coid=" + str(i)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find("td", class_="block_content_popup")

    #Title
    try:
        title = results.find(id="course_preview_title")
        courseTitle = title.text
    except Exception:
        return

    #CourseID -- parsed from title
    courseID = title.text[:8]
    return courseID


def scrape(i):

    URL = "https://catalog.udel.edu/preview_course.php?coid=" + str(i)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find("td", class_="block_content_popup")
    strResults = str(results)

    #Title
    try:
        title = results.find(id="course_preview_title")
        courseTitle = title.text
    except Exception:
        return

    #CourseID -- parsed from title
    courseID = title.text[:8]

    #Credits(s):
    startSearch = strResults.find('Credit(s):')
    credits = strResults[startSearch + 20:startSearch + 21]

    #Component:
    startSearchTmp = strResults.find('Component:', startSearch)
    endSearch = startSearch
    if startSearchTmp != -1:
        startSearch = startSearchTmp
        endSearch = strResults.find('<', startSearch + 11)
        component = strResults[startSearch + 20:endSearch]
    else:
        component = "Lecture"

    #description
    startSearchTmp = strResults.find('br', startSearch + 3)
    cutoff = strResults.find('<strong>', startSearch + 3)
    endSearchTmp = strResults.find('<br', startSearchTmp + 1)

    if startSearchTmp != -1 or cutoff > startSearchTmp:
        startSearch = startSearchTmp
        endSearch = endSearchTmp
        description = strResults[startSearch + 4:endSearch]
    else:
        description = "None"

    #Repeatable for credit:
    rfc = 'Repeatable for Credit:'
    startSearchTmp = strResults.find('Repeatable for Credit:', startSearch)
    endSearchTmp = strResults.find('<strong>', startSearch)
    if startSearchTmp != -1:
        startSearch = startSearchTmp
        endSearch = endSearchTmp
        repeatable = strResults[startSearch + len(rfc) + 10:endSearch]
    else:
        repeatable = "unspecified"

    #Allowed Units:
    au = 'Allowed Units:'
    startSearch = strResults.find('Allowed Units:', startSearch)
    endSearch = strResults.find('</strong>', startSearch)
    allowedUnits = strResults[startSearch + len(au) + 10:endSearch]

    #Multiple Term Enrollment:
    startSearch = strResults.find('Multiple Term Enrollment:', startSearch)
    endSearch = strResults.find('</strong>', startSearch)
    multTermEnrollment = strResults[startSearch + len(au) + 21:endSearch]

    #Search for crosslisted
    crosslist = []
    if strResults.find('Crosslisted:') != -1:
        while startSearch != -1:
            foundCrosslist = strResults.find('</a>', startSearch)
            crosslistEnd = strResults.find('. ', foundCrosslist)
            if foundCrosslist > crosslistEnd or foundCrosslist == -1:
                break
            startSearch = foundCrosslist
            crosslist += [strResults[startSearch - 8:startSearch]]
            startSearch += 1

    #Search for PREREQs:
    prereqs = []
    startSearchTmp = strResults.find('PREREQ:', startSearch)
    if startSearchTmp != -1:
        startSearch = startSearchTmp
        while startSearch != -1:
            foundPrereq = strResults.find('</a>', startSearch)
            prereqEnd = strResults.find('<hr', startSearch)
            if foundPrereq > prereqEnd or foundPrereq == -1:
                break
            startSearch = foundPrereq
            prereqs += [strResults[startSearch - 8:startSearch]]
            startSearch += 1

    univBreadth = ""
    startSearchTmp = strResults.find('University Breadth:', startSearch)
    if startSearchTmp != -1:
        startSearch = startSearchTmp
        foundUB = strResults.find('<strong>', startSearch+2)
        univBreadth += strResults[startSearch + 28:foundUB-1]

    engineeringBreadth = ""
    startSearchTmp = strResults.find('College of Engineering Breadth:', startSearch)
    if startSearchTmp != -1:
        startSearch = startSearchTmp
        foundEB = strResults.find('<strong>', startSearch+2)
        engineeringBreadth += strResults[startSearch + 39:foundEB-1]


    course = {  
       courseID : {
          "courseID": courseID,
          "title" : courseTitle,
          "credits": credits,
          "description": description,
          "component": component,
          "repeatable": repeatable,
          "allowedUnits": allowedUnits,
          "multTermEnrollment": multTermEnrollment,
          "prereqs": prereqs,
          "crosslisted": crosslist,
          "University Breadth": univBreadth,
          "Engineering Breadth": "",
          "URL": URL
      }  
    }
    return course


courses=[]
while i < 275300:
#while i < 270899: 
  jsonScrape = scrape(i)
  courseID = getID(i)
  if jsonScrape :
    courses += jsonScrape.values()
  print(i)
  i+=1


x = json.dumps(courses)
file = open('courseData.json', 'w')
file.write(x)
file.close()




"""
import requests
from bs4 import BeautifulSoup
import json

i = 270867

def scrape(i):

  URL = "https://catalog.udel.edu/preview_course.php?coid=" + str(i)
  page = requests.get(URL)
  soup = BeautifulSoup(page.content, "html.parser")
  results = soup.find("td",class_="block_content_popup")
  strResults = str(results)

  #Title
  try:
    title = results.find(id="course_preview_title")
    courseTitle = title.text
  except Exception:
    return

  #CourseID -- parsed from title
  courseID = title.text[:8]

  #Credits(s): 
  startSearch = strResults.find('Credit(s):')
  credits = strResults[startSearch+20:startSearch+21]


  #Component:
  startSearch = strResults.find('Component:',startSearch)
  endSearch = strResults.find('<b',startSearch)
  component = strResults[startSearch+20:endSearch]
 

  #description
  startSearchTmp = strResults.find('<br>', endSearch+3, endSearch+25)
  endSearchTmp = strResults.find('."<',startSearch)

  if startSearchTmp != -1:
    description = strResults[startSearch+4:endSearch]
    startSearch = startSearchTmp
    endSearch = endSearchTmp
   


  #Repeatable for credit:
  rfc = 'Repeatable for Credit:'
  startSearch = strResults.find('Repeatable for Credit:',startSearch)
  endSearch = strResults.find('<s',startSearch)
  print(endSearch)
  repeatable = strResults[startSearch+len(rfc)+10:endSearch]


  #Allowed Units:
  au = 'Allowed Units:'
  startSearch = strResults.find('Allowed Units:',startSearch)
  endSearch = strResults.find('<s',startSearch)
  allowedUnits = strResults[startSearch+len(au)+10:endSearch]


  #Multiple Term Enrollment:
  startSearch = strResults.find('Multiple Term Enrollment:',startSearch)
  endSearch = strResults.find('<s',startSearch)
  multTermEnrollment = strResults[startSearch+len(au)+21:endSearch]


  #PREREQ:
  prereqs = []
  ender = strResults.find('. ',startSearch)
  if strResults.find('PREREQ') != -1:
    while startSearch != -1: 
      foundPrereq = strResults.find('</a>',startSearch,ender)
      startSearch = foundPrereq
      if startSearch == -1:
        break
      prereqs += [strResults[startSearch-8:startSearch]]
      startSearch+=1


  course = {     #build course JSON
    courseID : {
      'title' : courseTitle,
      "credits" : credits,
      "component" : component,
      "repeatable" : repeatable,
      "allowedUnits" : allowedUnits,
      "multTermEnrollment" : multTermEnrollment,
      "prereqs" : prereqs,
      "crosslisted" : "",
      "University Breadth" : "",
      "Engineering Breadth" : "",
      "URL" : URL
    }
  }
  print(course)
  return course
#courses=[]
#while i < 275300:
#while i < 270872: test
#  jsonScrape = scrape(i)
#  print(i)
#  if jsonScrape :
#    courses += jsonScrape.items()

#  i+=1
scrape(i)
x = json.dumps(courses)
print(i)

file = open('courseData.json', 'w')
file.write(x)
file.close()
"""
