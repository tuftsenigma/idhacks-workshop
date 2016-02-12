"""
	IDHacks 2016 Workshop - Visualize Tufts Graduate Outcomes:

	Takes .csv data parsed from career page, calculate some 
	basic statistics, and reformat data into a json to be ready to visualize. (2/3)

"""

import  json
import	pandas			as pd
import	sys


#% ===== parsing packages 

try:
	import pandas		 as pd  		# data analysis package 
except ImportError:
	print "** It looks like the `pandas' package is not installed..."
	print "** \t - try installing it using pip via the command `pip install pandas'."
	sys.exit()


#% ===== metadata (in `real life', consider putting this in a diferent file!)

US_STATES = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}


#% ===== parsing functions

def well_formed(val):
        # check for 'pandas null' 
        if pd.isnull(val):
                return "N/A"
        else:
                return val


def get_all_summary_statistics(output_file):

	domestic_stats 		= {}
	df = pd.read_csv("raw_jobs_data.csv")

	for i, state in enumerate(US_STATES.keys()):

		if (i % 10 == 0):
			# progress
			print "** parsed %i/%i locations" % (i, len(US_STATES.keys()))


                # get most common (mode) attributes for each state
		state_stats = df[df["state"] == state].mode()
		number_of_graduates = df[df["state"] == state].count()[1]

		try:
			domestic_stats[state] = {
				"most popular company" 	: well_formed(state_stats["company"][0]),
				"most popular city" 	: well_formed(state_stats["city"][0]),
				"most popular title" 	: well_formed(state_stats["title"][0]),
				"number of graduates"	: well_formed(number_of_graduates),
				"fillKey"	: get_fill_category(number_of_graduates)
			}
		except:
                        # if there is no data, just output a blank entry
                        domestic_stats[state] = {
                                "most popular company"  : "N/A",
                                "most popular city"     : "N/A",
                                "most popular title"    : "N/A",
                                "number of graduates"   : "N/A",
                                "fillKey"               : "0"
                        }

			continue

	with open(output_file, "w+") as outfile:
		json.dump(domestic_stats, outfile, indent=4)
		print "** wrote formatted summary statistics to `%s'" % output_file



def get_fill_category(number_of_graduates):
        # a color key for our D3 visualization
	if number_of_graduates in range(1,10):
	    return "1-9"
	elif number_of_graduates in range(11,20):
	    return "10-19"   
	elif number_of_graduates in range(21,50):
	    return "20-49"
	elif number_of_graduates in range(51,100):
	    return "50-99"	
	elif number_of_graduates > 100:
	    return "100+"
        else:
            return "0"



#% ===== execute script

if __name__ == '__main__':
	
	get_all_summary_statistics(output_file="final_jobs_data.json")

