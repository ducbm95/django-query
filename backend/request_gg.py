from bs4 import BeautifulSoup
import urllib2
from urllib import urlencode
from pyvi.pyvi import ViTokenizer

# class for enriching data from Google
class RequestGG:

  def __init__(self,vn=True):
    if vn == True:
      self.url = 'http://www.google.com.vn/search?'
    else:
      self.url = 'http://www.google.com/search?'

    self.opener = urllib2.build_opener()
    self.opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.517.41 Safari/534.7')]

  def getStandardName(self, name):
    query = self.url + urlencode({'q': name.encode('utf-8')})
    html = self.opener.open(query).read().decode('utf-8')
    soup = BeautifulSoup(html, "html5lib")

    tags = soup.find_all("div", {"class": "rc"})
    data = [
      (tag.find("h3", {"class": "r"}).text if tag.find("h3", {"class": "r"}) != None else "")  + " " +
      (tag.find("span", {"class": "st"}).text if tag.find("span", {"class": "st"}) != None else "")
      for tag in tags]
    result = ", ".join(data)
    return result
