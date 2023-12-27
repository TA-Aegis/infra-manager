from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field, validator

class DnsType(str, Enum):
    A = "A"
    CNAME = "CNAME"

class GetDnsRecord(BaseModel):
    id: str
    type: DnsType
    name: str
    content: str

class AddDnsRecord(BaseModel):
    type: DnsType
    name: str
    content: str