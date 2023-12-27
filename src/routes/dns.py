from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request, status, File, UploadFile
from fastapi.responses import JSONResponse
from models.dns import DnsRecordList
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

@dns_router.get("/list")
async def GetDnsRecord():
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