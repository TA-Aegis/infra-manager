from typing import List

from models.dns import GetDnsRecord


def sanitizeDnsList(json_content: dict) -> List[GetDnsRecord]:
    try:
        # Extract the "result" key, which contains the list of DNS records
        dns_records_json = json_content.get("result", [])

        # Convert each DNS record JSON into a DnsRecord instance
        dns_records = [GetDnsRecord(**record) for record in dns_records_json]

        return dns_records

    except ValueError as e:
        # Handle JSON parsing errors
        print(f"Error parsing JSON: {e}")
        return []

    except Exception as e:
        # Handle other exceptions
        print(f"Error processing DNS records: {e}")
        return []