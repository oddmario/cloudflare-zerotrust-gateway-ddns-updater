import requests
import socket
import time
import json

CONFIG = {
    "CLOUDFLARE": {
        "EMAIL": "", # Cloudflare account email address here
        "API_TOKEN": "", # Cloudflare API token here (this one can be generated through the dashboard)
        "API_KEY": "", # Your Cloudflare global API key here
        "LOCATION_NAME": "Home" # The Cloudflare ZT Gateway location name
    },
    "HOSTNAME": "myhostname.ddns.net",
    "UPDATER_INTERVAL": 120 # in seconds
}

def main():
    cf_account_id = ""
    location_uuid = ""
    location_name = ""
    location_is_default = False
    
    while True:
        try:
            req = requests.get(
                f"https://api.cloudflare.com/client/v4/accounts",
                headers={
                    "Content-Type": "application/json",
                    "Authorizarion": "Bearer " + str(CONFIG['CLOUDFLARE']['API_TOKEN']),
                    "X-Auth-Key": str(CONFIG['CLOUDFLARE']['API_KEY']),
                    "X-Auth-Email": str(CONFIG['CLOUDFLARE']['EMAIL'])
                }
            )
            res = json.loads(req.text)
            cf_account_id = res['result'][0]['id']
            break
        except Exception as e:
            time.sleep(3)
            continue
    
    while True:
        try:
            req = requests.get(
                f"https://api.cloudflare.com/client/v4/accounts/{cf_account_id}/gateway/locations",
                headers={
                    "Authorizarion": "Bearer " + str(CONFIG['CLOUDFLARE']['API_TOKEN']),
                    "X-Auth-Key": str(CONFIG['CLOUDFLARE']['API_KEY']),
                    "X-Auth-Email": str(CONFIG['CLOUDFLARE']['EMAIL'])
                }
            )
            res = json.loads(req.text)
            for location in res['result']:
                if location['name'].strip() == CONFIG['CLOUDFLARE']['LOCATION_NAME'].strip():
                    location_uuid = location['id']
                    location_name = location['name']
                    location_is_default = location['client_default']
                    break
            break
        except Exception as e:
            time.sleep(3)
            continue
    
    while True:
        try:
            req = requests.put(
                f"https://api.cloudflare.com/client/v4/accounts/{cf_account_id}/gateway/locations/{location_uuid}",
                headers={
                    "Authorizarion": "Bearer " + str(CONFIG['CLOUDFLARE']['API_TOKEN']),
                    "X-Auth-Key": str(CONFIG['CLOUDFLARE']['API_KEY']),
                    "X-Auth-Email": str(CONFIG['CLOUDFLARE']['EMAIL'])
                },
                json={
                    "name": location_name,
                    "networks": [
                        {
                            "network": str(socket.gethostbyname(CONFIG['HOSTNAME'])) + "/32"
                        }
                    ],
                    "client_default": location_is_default
                }
            )
        except Exception as e:
            time.sleep(3)
            continue
        time.sleep( int(CONFIG['UPDATER_INTERVAL']) )

if __name__ == '__main__':
    main()
