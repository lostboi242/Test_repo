import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

link = 'https://docs.google.com/document/d/e/2PACX-1vSZ1vDD85PCR1d5QC2XwbXClC1Kuh3a4u0y3VbTvTFQI53erafhUkGot24ulET8ZRqFSzYoi3pLTGwM/pub'

def decoding_unicode(link):

	#This function is meant to take a link to a google document, look for all tables with in the document, and graph their contents onto a plot.

	#link - The url for the google document in use. Make sure settings are set to public
	
	#Take the link and convert it into a BeautifulSoup object
	doc = requests.get(url=link)

	#Note: Need to use .text as BeatifulSoup needs str
	soup_doc = BeautifulSoup(doc.text, 'html.parser')
	
	table = soup_doc.find_all('table')

	#Convert table into a dataframe
	df = pd.read_html(str(table))[0]

	#Remove the fake column headers and replace with first row.
	df.columns=df.iloc[0]
	df = df[1:]

	#Convert x and y coordinates into integers
	df['x-coordinate'] = pd.to_numeric(df['x-coordinate'] , downcast = 'integer')
	df['y-coordinate'] = pd.to_numeric(df['y-coordinate'] , downcast = 'integer')

	#Get max and min values for setting up plot axis
	ymax = df['y-coordinate'].max()
	ymin = df['y-coordinate'].min()
	xmax = df['x-coordinate'].max()
	xmin = 	df['x-coordinate'].min()
	
	plt.figure(figsize=(6,1))
	#Loop Through each row in the dataframe
	for index, rows in df.iterrows():
		
		#Find coordinates and unicode character from each row
		x = int(rows[0]) 
		y = int(rows[2])
		uni = rows[1]

		#Plot the unicode characters
		ax = plt.gca()
		ax.text(x, y, uni)
		ax.set_xlim([xmin, xmax])
		ax.set_ylim([ymin, ymax])
		ax.axis('on')
		plt.show()


decoding_unicode(link)