import time, network, machine
import urequests as requests
import settingsService
import json
import logger
import epaperService


def getTasks():
    token = settingsService.get("token")
    tasksUrl = settingsService.get("tasksUrl")
    header_data = { 
        "content-type": 'application/json; charset=utf-8', 
        "Authorization": token,
        "devicetype": '1'
        }
    header_data["token"] = token
    res = requests.get(tasksUrl, headers = header_data)
    text = res.text
    logger.info("Tasks:" + text)
    r = json.loads(text)
    return r

def displayTasks():
    items = getTasks()
    for item in items:
        logger.info("Task:" + item["title"])
        item.row = 1


def getFirstTask(val): 
    for value in val:
        logger.info("Task:" + value["content"])
        return value

def getTaskItem():
    items = getTasks()
    item = getFirstTask(items)