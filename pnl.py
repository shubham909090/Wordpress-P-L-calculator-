from woocommerce import API
from datetime import datetime,timedelta
import json

yesterday =""
today=""
data =[]
newdata=[]
payTm_and_phonePay =0
razerpay=0
i=0

wcapi = API(
    url="https://fotovilla.in/",
    consumer_key="ck_0a3246450ebf788069af634d2ca099b17b9f2fac",
    consumer_secret="cs_566eea81414c838f11258a5fab67fcc98b7b567a",
    version="wc/v3"
)
if datetime.now().hour>10:
    yesterday = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
    print(f"from time ->{yesterday}")
    today= datetime.now().replace(hour=23, minute=59, second=59, microsecond=0).isoformat()
    print(f"to time ->{today}")
    data =wcapi.get("orders?per_page=100", params={"after": yesterday,"before":today}).json()
else:
    yesterday = (datetime.now()-timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
    print(f"from time ->{yesterday}")
    today= (datetime.now()-timedelta(days=1)).replace(hour=23, minute=59, second=59, microsecond=0).isoformat()
    print(f"to time ->{today}")
    data =wcapi.get("orders?per_page=100", params={"after": yesterday,"before":today}).json()

  
for item in data:
  if item["status"] =="processing" or item["status"] =="processed" or item["status"] =="dailychecking":
    newdata.append({"id":item["id"],"status":item["status"],"total":item["total"],"payment_method":item["payment_method"]})
    if item["payment_method"]=="PhonePe Payment Solutions" or item["payment_method"]=="paytm":
       payTm_and_phonePay+= float(item["total"])
    if item["payment_method"]=="razorpay":
       i+=1
       print((item["status"],item["total"],i))
       razerpay+= float(item["total"])



print(f"Razerpay -> {razerpay}")
print(f"Paytm + Phonepay -> {payTm_and_phonePay}")

with open("outputbig.json", "w") as f:
  json.dump(data, f, indent=4)

with open("output.json", "w") as f:
  json.dump(newdata, f, indent=4)




