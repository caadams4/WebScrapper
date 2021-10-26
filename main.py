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
    print(description)


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


  course = {
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

  return course
courses=[]
#while i < 275300:
while i < 270872:
  jsonScrape = scrape(i)

  if jsonScrape :
    courses += jsonScrape.items()

  i+=1
  
x = json.dumps(courses)
print(x)

file = open('courseData.json', 'w')
file.write(x)
file.close()