import	sys


"""
	IDHacks 2016 Workshop - Visualize Tufts Graduate Outcomes:

	A simple script to scrape the Tufts University career page and parse it into
	a csv file. (1/3)

"""


#% ===== scraping / parsing packages 

try:
	import requests		    		# make HTTP requests
except:
	print "** It looks like the `requests' package is not installed..."
	print "** \t - try installing it using pip via the command `pip install requests'."
	sys.exit()

import 	requests

try:
	import pandas		 as pd 		# data analysis package
except:
	print "** It looks like the `pandas' package is not installed..."
	print "** \t - try installing it using pip via the command `pip install pandas'."
	sys.exit()

try:
	import BeautifulSoup as bs 		# web scraping package
except:
	print "** It looks like the `BeautifulSoup' package is not installed..."
	print "** \t - try installing it using pip via the command `pip install BeautifulSoup'."
	import BeautifulSoup as bs
	sys.exit()



#% ===== scraping / parsing functions 

def parse_tufts_career_page(output_file):

	# input dataframe
	df = pd.DataFrame([], columns=["company", "title", "city", "state"])

	# request + parse html
	url = "http://students.tufts.edu/career-center/explore-careers-and-majors/outcomes-major"
	html = requests.get(url).content
	soup = bs.BeautifulSoup(html)

	# grab every table row (job entry)
	job_entries = list(soup.findAll("tr"))

	for i, entry in enumerate(job_entries):

		if (i % 100 == 0):
			# progress
			print "** parsed %i/%i job entries" % (i, len(job_entries))

		# now parse every cell (job attribute)
		job_attributes = entry.findAll("td")

		# parse every relevant attribute that exists
		job_company = None if len(job_attributes) < 1 else job_attributes[0].text.encode('ascii', 'ignore') 
		job_title   = None if len(job_attributes) < 2 else job_attributes[1].text.encode('ascii', 'ignore')
		job_city    = None if len(job_attributes) < 3 else job_attributes[2].text.encode('ascii', 'ignore')
		job_state   = None if len(job_attributes) < 4 else job_attributes[3].text.encode('ascii', 'ignore')

		# append to dataframe
		df.loc[len(df)] = [job_company, job_title, job_city, job_state]

	# save as csv file
	df.to_csv(output_file)
	print "** saved to '%s'" % output_file



#% ===== execute script

if __name__ == '__main__':
	parse_tufts_career_page(output_file="raw_jobs_data.csv")



