import sys
import json
import logging
import re
import subprocess

def Projects():
    f = open("projects.txt", 'r')
    content = f.read()
    content = content.split('\n')
    projectIDs = []
    projectNames = []
    content.pop(0)
    for i in range(0, len(content)):
        temp = content[i].split(' ')
        count = 0
        for element in temp:
            if len(element) <=  1:
                continue
            else:
                if count == 0:
                    projectIDs.append(element)
                elif count == 1:
                    projectNames.append(element)
                count += 1
    f.close()
    print("projectIDs: ", projectIDs)
    print("projectNames: ", projectNames)
    return [projectIDs, projectNames]

def getServiceAccountEmail():
    f = open("service-account.txt", 'r')
    content = f.read()
    print("content: ",content)
    content = content.split('\n')
    data = []
    content.pop(0)
    for i in range(0, len(content)):
        temp = content[i].split(' ')
        print("temp: ",temp)
        for element in temp:
            if len(element) <=  1:
                continue
            else:
                data.append(element)
    print("email: ",data[len(data) -2])
    return data[len(data) -2]


if __name__ == '__main__':
    ret = getServiceAccountEmail()
