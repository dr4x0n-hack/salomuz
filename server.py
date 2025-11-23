from flask import Flask, request
import subprocess, os, json
import exifread
import requests

app = Flask(__name__)

@app.post("/run")
def run():
    cmd = request.json.get("command")

    # -----------------------------------
    # HELP
    # -----------------------------------
    if cmd == "help":
        return """Available OSINT commands:
- exif <file>
- reverse-image <file>
- whois <domain>
- geo-lookup <lat,lon>
- help"""

    # -----------------------------------
    # EXIF
    # -----------------------------------
    if cmd.startswith("exif "):
        filename = cmd.split(" ",1)[1]
        if not os.path.exists(filename):
            return "File not found"
        with open(filename, "rb") as f:
            tags = exifread.process_file(f)
        return json.dumps({k:str(v) for k,v in tags.items()}, indent=2)

    # -----------------------------------
    # WHOIS (safe)
    # -----------------------------------
    if cmd.startswith("whois "):
        domain = cmd.split(" ",1)[1]
        r = requests.get(f"https://whois.internic.net/cgi/whois?domain={domain}")
        return r.text[:1500]

    # -----------------------------------
    # GEO LOOKUP (safe)
    # -----------------------------------
    if cmd.startswith("geo-lookup "):
        coords = cmd.split(" ",1)[1]
        lat, lon = coords.split(",")
        url = f"https://api.bigdatacloud.net/data/reverse-geocode-client?latitude={lat}&longitude={lon}&localityLanguage=en"
        data = requests.get(url).json()
        return json.dumps(data, indent=2)

    # -----------------------------------
    # REVERSE IMAGE (MOCK – safe)
    # -----------------------------------
    if cmd.startswith("reverse-image "):
        file = cmd.split(" ",1)[1]
        return f"""
Mock reverse image search result:
File: {file}
This feature requires a real API key (Google Vision, Bing API).
"""

    return "Unknown command. Type 'help'"
