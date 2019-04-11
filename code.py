import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import base64
import ssl
#import re

""""
Developer mode - source: https://www.pcstore.com.tw/css/search_main.js?t=18
function completeCallback(response) {
    var data = response.content.split('\n');
    if(data[0].match(/COUNT:/) && data.length > 3){
      var newstr="相關商品：";
      for(var i=1 ; i < data.length; i ++) {
        var detal = new Array();
        detal = data[i].split("\t", 3);
        if(detal.length != 3) continue;
        if(detal[2].trim() == custom.input) continue;
        newdata = encodeURI(detal[2]).base64_encode();
        newstr += "<a href='/adm/psearch.htm?store_k_word="+newdata+"&slt_k_option=1'
"""
serviceurl = "https://www.pcstore.com.tw/adm/psearch.htm?"

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Forming URL
s = input("輸入搜尋字串:")
surl= urllib.parse.quote(s)
search = base64.b64encode(bytes(surl, "utf-8")).decode("ascii")
parms = dict()
parms["store_k_word"] = search
parms["slt_k_option"] = 1
url = serviceurl + urllib.parse.urlencode(parms)
print("Retrieving", url)

html = urllib.request.urlopen(url, context=ctx).read()

# Using BeautifulSoup
soup = BeautifulSoup(html,"html.parser")
results = soup.find_all("div", {"class": "pic2t pic2t_bg"})

for line in results:
    link = line.a.attrs["href"]
    title = line.a.text
    print(title, link)

""""
# Using RegEx to find link 
for line in results:
    temp = line.decode().strip()

    link = re.findall("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", temp)
    print("URL:", link)
"""