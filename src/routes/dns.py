from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request, status, File, UploadFile
from fastapi.responses import JSONResponse
from models.dns import GetDnsRecord, AddDnsRecord
from random import choice, randint
from fastapi import FastAPI, File, UploadFile
from PIL import Image
import io
import os
import pytz
from datetime import datetime, timedelta
import requests
import json
from services.sanitizer import sanitizeDnsList
from dotenv import load_dotenv, dotenv_values

dns_router = APIRouter(
    tags=["DNS"]
)

from fastapi import HTTPException

load_dotenv()
config = dotenv_values(".env")

zone_id = config["CLOUDFLARE_ZONE_ID"]
auth_key = config["CLOUDFLARE_KEY"]

@dns_router.get("/")
async def getDnsRecord():
    try:
        url = "https://api.cloudflare.com/client/v4/zones/"+zone_id+"/dns_records"

        header = {
            "Content-Type": "application/json",
            "X-Auth-Email": "devops.econolab@gmail.com",
            "X-Auth-Key": auth_key
        }

        response = requests.request("GET", url, headers=header)

        # Extract JSON content from the response
        json_content = response.json()

        return sanitizeDnsList(json_content)

    except ValueError as e:
        return JSONResponse(status_code=401, content={"message": str(e), "data": {}})

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e), "data": {}})

@dns_router.post("/")
async def addDnsRecord(request: AddDnsRecord):
    try:
        url = "https://api.cloudflare.com/client/v4/zones/"+zone_id+"/dns_records"

        header = {
            "Content-Type": "application/json",
            "X-Auth-Email": "devops.econolab@gmail.com",
            "X-Auth-Key": auth_key
        }

        payload = {
            "content": request.content,
            "name": request.name,
            "proxied": False,
            "type": request.type,
            "comment": "",
            "tags": [],
            "ttl": 3600
        }

        response = requests.request("POST", url, json=payload, headers=header)
        print(response.text)

    except ValueError as e:
        return JSONResponse(status_code=401, content={"message": str(e), "data": {}})

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e), "data": {}})