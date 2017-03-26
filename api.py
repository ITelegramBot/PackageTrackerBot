# coding=utf-8
import requests

PROVIDER_URL = "http://www.kuaidi100.com"
HEADERS = {
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Package Tracker Bot/0.1",
    "Accept-Encoding": "gzip, deflate, sdch"
}


class TrackerApi(object):
    """ API 使用快递100的API """

    def __init__(self):
        pass

    @staticmethod
    def getPackageProvider(packageID):
        req = requests.post(PROVIDER_URL + "/autonumber/autoComNum?text=" + str(packageID), headers=HEADERS)
        if not req.json()["auto"]:
            raise ValueError("Invalid Package Number!")
        else:
            return req.json()["auto"][0]["comCode"]

    @staticmethod
    def getPackageInformation(packageID, packageProvider=""):
        if not packageProvider:
            packageProvider = TrackerApi.getPackageProvider(packageID)
        req = requests.post(PROVIDER_URL + "/query?type=%s&postid=%s&valicode=" % (
            packageProvider, packageID
        ), headers=HEADERS)
        if "status" in req.json() and req.json()["status"] == "201":
            return {
                "status": 0,
                "data": []
            }

        if req.json()["state"] == "1" and req.json()["state"] == "5":
            statusCode = 1
        elif req.json()["state"] == "3":
            statusCode = 2
        else:
            statusCode = 3

        data = []

        for item in req.json()["data"]:
            data.append({
                "data": item["context"],
                "time": item["time"]
            })

        return {
            "status": statusCode,
            "data": data
        }

    @staticmethod
    def getLastMessage(packageID, packageProvider=""):
        info = TrackerApi.getPackageInformation(packageID, packageProvider)
        if info["data"]:
            return info["data"][0]["data"]
        else:
            return "Unknown"


def getStatusFromCode(code):
    if code == 0:
        return "Unknown"
    elif code == 1:
        return "Sending"
    elif code == 2:
        return "Delivered"
    else:
        return "Trouble"
