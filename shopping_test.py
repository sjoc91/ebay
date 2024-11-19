import os
from ebaysdk.shopping import Connection as Shopping
from ebaysdk.finding import Connection as Finding
from dotenv import load_dotenv

load_dotenv()

APPID = os.getenv("APPID")
Finding(appid=APPID, config_file=None)

api = Shopping(domain='svcs.sandbox.ebay.com', appid="APPID")
response = api.execute('FindPopularItems', {'QueryKeywords': 'Python'})
print(response.dict())