from typing import List

from models.dns import DnsRecordList


def sanitizeDnsList(json_content: dict) -> List[DnsRecordList]:
    try:
        # Extract the "result" key, which contains the list of DNS records
        dns_records_json = json_content.get("result", [])

        # Convert each DNS record JSON into a DnsRecord instance
        dns_records = [DnsRecordList(**record) for record in dns_records_json]

        return dns_records

    except ValueError as e:
        # Handle JSON parsing errors
        print(f"Error parsing JSON: {e}")
        return []

    except Exception as e:
        # Handle other exceptions
        print(f"Error processing DNS records: {e}")
        return []