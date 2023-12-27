import json
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class DnsRecordList(BaseModel):
    id: str
    type: str
    name: str
    content: str