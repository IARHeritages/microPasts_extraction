##### Extract the completed projects from the micropast website####
#This code was developed for microPasts project by mkrzyzanska
#It downlaods all the completed projects from microPasts throught the Pybossa API
#Fragments of the code are based on: https://github.com/Scifabric/pybossa/issues/1260, accessed on 18.07.2017

#Set working directory
os.chdir('path_to_directory')

#Get the libraries:
         
import json
import csv
import os
import requests
import time


#Get the list of all the completed tasks

#Set up a list to append the extracted tasks to
tasks = []

#Extract and append first 100 tasks (100 is a maximum throught the API
res = requests.get('http://crowdsourced.micropasts.org/api/task?state=completed&limit=100')
data = res.json()
tasks.extend(data)

#Loop to extract all the remaining task

while(len(data)!=0):
         print (len(tasks))
         lid=tasks[len(tasks)-1]["id"]
         res = requests.get('http://crowdsourced.micropasts.org/api/task?state=completed&limit=50&last_id='+str(lid))
         data = res.json()
         tasks.extend(data)

###If there are errors with getting the las id try:
         lid=tasks[len(tasks)-1][0]["id"]

###Save the tasks as json
with open('tasks.json', 'w') as outfile:
    json.dump(tasks, outfile)
    
###To load the tasks from json file:
    
with open('tasks.json') as data_file:    
    tasks = json.load(data_file)


# To write as csv:

taskList = open('tasks.csv', 'w')

# create the csv writer object

csvwriter = csv.writer(taskList)

count = 0

i=0
j=len(tasks)
while(i<j):

      if i == 0:

             header = tasks[0].keys()

             csvwriter.writerow(header)

             count += 1

      csvwriter.writerow(tasks[i].values())
      i=i+1

taskList.close()


###Extract all the taskruns:

t = []
i=0
j=len(tasks)
while(i<j):
    print (i)
    task_id=tasks[i]["id"]
    data = [1,2]
    offset=0
    while (len(data)>0):
        res = requests.get('http://crowdsourced.micropasts.org/api/taskrun?task_id='+str(task_id)+'&limit=1&offset='+str(offset))
        if int(res.headers['X-RateLimit-Remaining']) < 10:
            time.sleep(300) # Sleep for 5 minutes
        else:

            data = res.json()
            t.extend(data)
            offset=offset+1
    i=i+1
###Save the task runs:

        ###Save the tasks as json
with open('tasksRuns.json', 'w') as outfile:
    json.dump(t, outfile)
    
###To load the tasks from json file:
    
with open('tasksRuns.json') as data_file:    
    t = json.load(data_file)


# To write as csv:

taskRuns = open('taskRuns.csv', 'w')

# create the csv writer object

csvwriter = csv.writer(taskRuns)

count = 0

i=0
j=len(t)
while(i<j):

      if i == 0:

             header = t[0].keys()

             csvwriter.writerow(header)

             count += 1

      csvwriter.writerow(t[i].values())
      i=i+1

taskRuns.close()
