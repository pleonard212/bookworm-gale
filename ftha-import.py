from bs4 import BeautifulSoup
import HTMLParser
h = HTMLParser.HTMLParser()
import json
from os import listdir
from os.path import isfile, join
alltext = open('alltext.txt', 'w')
jsoncatalog = open('jsoncatalog.txt', 'w')

# Get a list of all the XML files, one per issue (roughly 36k for The Financial Times 1888-2010)
thexmlfiles = [ file for file in listdir('FTXML') if isfile(join('FTXML',file))]

for thisxmlfile in thexmlfiles:
	print('Now Processing: ' + join('FTXML',thisxmlfile))
	xmlfile = open(join('FTXML',thisxmlfile), 'r')
	soup = BeautifulSoup(xmlfile)
	for article in soup.find_all('article'):
		for id in article.find_all('id'):
			thisid = id.string
			print("Found Article #" +  thisid)
		alltext.write(thisid + '\t')

		for link in article.find_all('permalink'):
			thispermalink =  link.string
			print("http://find.galegroup.com/ftha/infomark.do?docType=LTO&docLevel=FASCIMILE&prodId=FTHA&tabID=T003&searchType=AdvancedSearchForm&type=multipage&version=1.0&userGroupName=29002&docPage=article&docId=HS" + thispermalink + "&contentSet=LTO&source=gale")


		for headline in article.find_all('ti'):
			if headline.text:  #Test for empty headlines
				thisheadline = headline.string
			else:
				thisheadline = "Untitled"
			print("Its headline is " +  thisheadline)

		thissubhead = ''
		for subhead in article.find_all('ta'):
			if subhead.text:  #Test for empty subheadlines
				thissubhead += " &mdash; " + subhead.string
		print("Its subhead is " +  thissubhead)

		for category in article.find_all('ct'):
			thiscategory = category.string
			print("Categorized as " + thiscategory)
		metadata = { 'filename' : thisid, 'searchstring' : '<a target="_blank" href="http://find.galegroup.com/ftha/infomark.do?docType=LTO&docLevel=FASCIMILE&prodId=FTHA&tabID=T003&searchType=AdvancedSearchForm&type=multipage&version=1.0&userGroupName=29002&docPage=article&docId=HS' + thispermalink + '&contentSet=LTO&source=gale">' + thisheadline + thissubhead + '</a>', 'category' : thiscategory }
		json.dump(metadata, jsoncatalog)

		for section in article.find_all('text.cr'):
			for word in section.find_all('wd'):
				if word.text:  #Test for empty words, which do exist and cause the de-entity-izer to freak
					unescapedword = h.unescape(word.string)
					alltext.write(unescapedword.encode('utf-8')+' ')
		alltext.write('\n')
	xmlfile.close()
jsoncatalog.close()
alltext.close()
