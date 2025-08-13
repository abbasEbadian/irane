from fastapi import FastAPI, Response
import ipaddress
import json
from pathlib import Path

app = FastAPI()

json_path = Path(__file__).parent / "ip_list.json"
with open(json_path, "r") as f:
    ip_ranges = json.load(f)
    networks = [ipaddress.ip_network(cidr) for cidr in ip_ranges]

@app.get("/{ip:path}")
async def get_ip(ip: str):
    try:
        ip_addr = ipaddress.ip_address(ip)
    except ValueError:
        return {"error": "Invalid IP address"}

    for net in networks:
        if ip_addr in net:
            return Response(content="IR", status_code=200)
    return Response(content="NIR", status_code=418)