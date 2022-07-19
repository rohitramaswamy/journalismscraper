from numpy import fix
import pandas as pd
import io
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import requests
from bs4 import BeautifulSoup
import json
import sys

class Website:
  URL=""
  TextToParse=""
  ParsedText=""
  printScrapeData=0
  websiteFlag=""

  def ParseJSonInputFile(self):
    # Opening JSON file
    f = open('data.json')
    
    # returns JSON object as
    # a dictionary
    data = json.load(f)
    
    # Iterating through the json
 
    print("Received JSON string = ", data)

    # Parsing the json file

    if(data['website']=="nytimes"):
      self.websiteFlag="nytimes"
      self.URL="http://www.nytimes.com"

    if(data['website']=="foxnews"):
      self.websiteFlag="foxnews"
      self.URL="http://www.foxnews.com"
    

    if(data['showscrape']=="true"):
      self.printScrapeData=1
    
    # Closing json file
    f.close()

  def GetHTMLData(self):
    
    # use requests class to getthe page data

    self.page = requests.get(self.URL)

    # use BeautifulSoup class to parse the data to text (BeautifulSoup is a library to parse websites)

    self.soup = BeautifulSoup(self.page.text)

     # use store the text data
    self.TextToParse=self.page.text
  
  def DownLoadNLTK(self):
    nltk.download([
    "names",
    "stopwords",
    "state_union",
    "twitter_samples",
    "movie_reviews",
    "averaged_perceptron_tagger",
    "vader_lexicon",
    "punkt",
    ])

  def NLTKProcessData(self):
    #Create a corpus of all Stop Words
    stopwords = nltk.corpus.stopwords.words("english")

    #convert all words in text to lower case
    self.df[0]=self.df[0].str.lower()

    #Remove special characters by using character matching on Dataframe
    self.df['Text_Letters_Only'] = self.df[0].str.replace(r'[^a-zA-Z ]\s?',r'',regex=True)

    #Remove stop words with lambda function from Dataframe
    self.df['Text_without_stopwords'] = self.df['Text_Letters_Only'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stopwords)]))

    #create a text string from all rows in datagram
    text_without_stopwords =""
    i=0

    for row in self.df.Text_without_stopwords:
        text_without_stopwords = text_without_stopwords + self.df.Text_without_stopwords[i]
        i=i+1

    print(self.printScrapeData)
    #store the scraped data in a file if flag is set via HTML input
    if(self.printScrapeData==1):
      print(text_without_stopwords)
      f = open("scrape.txt", "w")
      f.write("<br>")
      f.write("<H2> SCRAPE DATA </H2>")
      f.write(text_without_stopwords)
      f.write("<br>")
      f.close()     

    words_without_stopwords = nltk.word_tokenize(text_without_stopwords)

    #compute the frequency distrbution of key words

    fd = nltk.FreqDist(words_without_stopwords)

    #store top words in file called topwords.txt, iterate through the list
    f = open("topwords.txt", "w")
    f.write("<br>")
    f.write("<H2> TOP 100 WORDS </H2>")
    str2=" "
    for x in fd.most_common(100):
      str2=str2+ x[0] + " "
    f.write(str2)
    f.write("<br>")
    f.close()     
    print(fd.most_common(100))
    print(fd.tabulate(100))
   
   #Sentiment analysis with nltk library
    sia = SentimentIntensityAnalyzer()

    #store sentiment in a file 
    f = open("sentiment.txt", "w")
    f.write("<br>")
    f.write("<H2> SENTIMENT SCORES </H2>")
    #iterate over a dictionary that contains the sentiment values
    str2=" "
    for key in sia.polarity_scores(text_without_stopwords):
      str2=str2+key+": "+str(sia.polarity_scores(text_without_stopwords)[key]) +" "
    f.write(str2)
    f.write("<br>")
    f.close()     

    print(sia.polarity_scores(text_without_stopwords))
   

  def CreateDataFrame(self):
    #store the parsed data in a DataFrame (PANDAS) for easy manipulation, Dataframe is a 2 dimensional data store
    self.data = io.StringIO(self.ParsedText)
    self.df=pd.DataFrame(self.data)
    
  #define NTYTimes class that inherits from parent class Website
   
class NYTimes(Website):
  
  #Polymorphism in the ParseHTML method
  def ParseHTML(self):
    
    #logic to parse text based on custom tags
    str1=""
    for h in self.soup.find_all( "a"):
      str1= str1 + " " + h.getText() +" "

    self.ParsedText = str1
    
#define FoxNews class that inherits from parent class Website

class FoxNews(Website):
  #Polymorphism in the ParseHTML method
  def ParseHTML(self):
     #logic to parse text based on custom tags

    str1=""
    for z in self.soup.find_all(class_=  "info-header"):
      print(z.getText())
      str1= str1 + " " + z.getText() +" "
    self.ParsedText = str1



#create the main website object
obj_website = Website()

#Parse the JSON file for configuration
obj_website.ParseJSonInputFile()

#initiailize the Natural Language processing libraries
obj_website.DownLoadNLTK()

#Process for NYTimes object

if(obj_website.websiteFlag == "nytimes"):
  obj_nytimes = NYTimes()

  #Set Flags
  obj_nytimes.URL=obj_website.URL
  obj_nytimes.printScrapeData=obj_website.printScrapeData
  
  obj_nytimes.GetHTMLData() 
  obj_nytimes.ParseHTML()
  obj_nytimes.CreateDataFrame()  
  obj_nytimes.NLTKProcessData()

#Process for FoxNews object

if(obj_website.websiteFlag == "foxnews"):
  obj_foxnews = FoxNews()

  #Set Flags
  obj_foxnews.URL=obj_website.URL
  obj_foxnews.printScrapeData=obj_website.printScrapeData
  
  obj_foxnews.GetHTMLData() 
  obj_foxnews.ParseHTML()
  obj_foxnews.CreateDataFrame()  
  obj_foxnews.NLTKProcessData()


