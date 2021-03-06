#IDHack 2016 Demo ![Brought to you by Tufts Enigma][logo]
[logo]: imgs/logo.png
## Visualizing Tufts Graduate Outcomes    
   




Greetings hackers! In this technical demo, we're going to show you how to create a map visualization - from web mining to data processing to visualization - using a bunch of different tools.

If you've **done some sort of web development work** and you're somewhere in the **beginner** to **intermediate** skill level for Python, and Javascript (ideally both, but one or the other is fine too), then you'll probably get the most of this demo. If not, this tutorial is still worth looking at!

The table of contents gives you a good idea as to what kind of pipeline we're going to write:

## Table of Contents
1. ### [Introduction](#introduction)
2. ### [Context](#context)
3. ### [Setup](#setup)
4. ### [Web Scraping with BeautifulSoup](#web-scraping-with-beautifulsoup)
5. ### [Data Cleaning / Processing with Pandas](#data-cleaning--processing-with-pandas)
6. ### [Visualizing with d3.js](#visualizing-with-d3js)


## Introduction

Here are some technical concepts that we touch on in this demo:

1.	creating a simple web scraping script (**Python**)
2.	basic data parsing / processing (**Python**)
3.	creating an interactive data visualization (**Javascript**) 

The final product will look something like:

![alt text](imgs/preview.png)

## Context

In 2015, The Tufts Independent Data Journal wrote an article that looked to answer a simple question using data - [where do Tufts graduates mostly end up?](http://tuftsenigma.org/where-exactly-do-tufts-graduates-go/) Like anyone who ever asks an interesting question, we decided to do a little research. With a little noodlin' and googlin', we quickly found out that Tufts Career Center itself posts graduate outcomes right on its [website](http://students.tufts.edu/career-center/explore-careers-and-majors/outcomes-major)!

![alt text](imgs/site.png)

This is our data. Let's make something with it.

## Setup

Before we dive in, here's a rundown of some of the technical tools in this demo and how to get them set up:

* **Python (v2.7)** - the main programming language we will be using to work with our data.

* **[Requests](http://docs.python-requests.org/en/master/) (v3.2.1)** - easily make HTTP requests in Python. Download this package using [pip](https://pypi.python.org/pypi/pip):

	```pip install requests==2.9.1```

* **[BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/) (v3.2.1)** - a web / text scraping package in Python that we'll use to parse the careers page; most easily installed using pip:

	```pip install BeautifulSoup==3.2.1```

* **[Pandas](http://pandas.pydata.org/) (v0.16.2)** - a data analysis package in Python allowing for easy manipulation, querying, and reformatting of our parsed data; again, most easily installed using pip:

	```pip install Pandas==0.16.2```

* **[D3.js](https://d3js.org/) (v3.5.3)** - *another* data manipulation package in javascript, primarily used for creating interactive web visualizations; we'll be using this to make our final map visualization. D3 uses the following script tag (we'll go over where to put that eventually):

	```<script src="//cdnjs.cloudflare.com/ajax/libs/d3/3.5.3/d3.min.js"></script>```

* **[TopoJSON.js](https://github.com/mbostock/topojson) (v1.6.9)** - a javascript library that encodes topology (don't worry about what that means); we'll use this as a helper script in our map visualization. TopoJSON uses the following script tag:

	```<script src="//cdnjs.cloudflare.com/ajax/libs/topojson/1.6.9/topojson.min.js"></script>```

* **[DataMaps.js](http://datamaps.github.io/)** - the final javascript library we'll be using to conveniently generate our actual map. This one you'll need to download and place in your project directory from `https://raw.githubusercontent.com/markmarkoh/datamaps/master/dist/datamaps.usa.min.js`.

It's worth glancing at the docs for each of these packages, but by no means do you need to be a pro at any of these tools for this tutorial.

Ready to go?

## Web Scraping with BeautifulSoup

The first thing we want to do is *scrape* all the data from the page. Luckily for us, the source code for the website is nicely formatted in a static html table. On inspection, each row corresponds to a job entry:

![alt text](imgs/code-vs-site.png)

We'll write a script called `parse_career_page.py` that will hit this url and output a nicely formatted .csv file with all this jobs data.

Using BeautifulSoup, we can pretty easily extract the entries from these tables and throw them into a **Pandas dataframe**. The fields we care about from each entry in the table are *company*, *title*, *city*, and *state* - so we initialize our dataframe with these columns:

```python 
df = pd.DataFrame([], columns=["company", "title", "city", "state"])
```

In one line, we can make a request to the career page url to get a response with the html source:

```python
html = requests.get(url).content
```

And in the next line, we can create a 'soup' of all the parsed html elements in the page (including tables):

```python
soup = bs.BeautifulSoup(html)
```

We can then search for tables in our 'soup' and extract all the rows that correspond to job entries:

```python
job_entries = list(soup.findAll("tr"))
```

Then we want to append each of these entries to our dataframe (check out the script to see how this is done). To save our dataframe to a .csv file, it's yet another simple one-liner:

```python
df.to_csv("raw_jobs_data.csv")
```

Check out the resulting .csv file - each row should look something like:

``` 0,Eastdil Secured,Analyst,New York,NY ```

## Data Cleaning / Processing with Pandas

There are around 2000 rows of job entries in our csv file! Before we can throw this data onto a map, we want to *summarize* the data and *format* it to fit the expected input format for the **DataMaps API**. Now, we *could* just take our raw .csv data and write a javascript to reformat it 'real-time' *on* our web page, but we'd rather not have our web page work that hard. Instead, we're going to let Python do the heavy lifting just once and produce a clean .json file to directly plug into our web page.

So in this step, we're going to write another Python script called `get_stats.py` that's going to calculate some basic summary statistics about our data that we can then visualize. Primarily, we want to know **what the most common institution, job title, and city is for Tufts graduates in each U.S. state**.

We're again going to use a Pandas dataframe to do all our data manipulation. First things first, we import our .csv file into a dataframe:

```python
df = pd.read_csv("raw_jobs_data.csv")
```

Then the *key* line of code in this script is getting these summary statistics for each state, which we can do by **filtering by state** and then **getting the mode value of each column**. This looks like:

```python
MA_stats = df[df["state"] == "MA"].mode()
```

Populating a Python dictionary with our data, we then dump it to a .json file which is the following line at the end of our function:

```python
json.dump(domestic_stats, output_file, indent=4)
```

So now, a nicely formatted state-by-state summary of our data can be found in ```final_jobs_data.json```. Here's the entry for Washington:

![alt text](imgs/summary-stats.png)

Looks like Jumbos are doing alright out there!


## Visualizing with d3.js

*Finally*, we're at a place where we can create our map!


### A speed introduction to D3

D3 (data-driven documents) is a javascript library that does one thing: take data and *bind* it to HTML objects. Sounds simple right? In reality, turns out that D3 is kind of, sort of really hard to work with.

But that's okay! Here are two key elements of D3, which are pretty much all you need to know for this demo:

- **to make visualizations, we inject [SVG elements](http://www.w3schools.com/svg/) into our HTML code.**

- **to make *interactive* visualizations, we write (asynchronous) functions that tell our HTML elements how to react when users do things.**

Given that super high level overview... let's dig into this!

### Setting up the visualization directory

Right now with your scripts and data files, your directory structure should look like this:

``` ruby
idhacks-workshop/
+-- parse_career_page.py
+-- get_statts.py
+-- raw_jobs_data.csv
+-- final_jobs_data.json
```

Let's create a directory `/visualization` to put all our visualization code. 

The first thing we want to do is copy the file with our summary data - `final_jobs_data.json` - into the `/visualization` directory. This is after all, what we'll be basing our map visualization off of!

Next, let's create two new files - `index.html` and `visualize_data.js`. Our file `index.html` is what the visualization is going to directly be *injected into*. On the other hand, `visualize_data.js` is the script that's going to actually create our map visualization and do the injecting.

Finally, if you recall from earlier, we want to download the DataMap API - a *really* useful javascript library that's basically going to be doing all the work for us in rendering this map. You can download the single file from `https://raw.githubusercontent.com/markmarkoh/datamaps/master/dist/datamaps.usa.min.js` and drag into our directory as well.

Whew! To recap, our directory should now look like *this*:

``` ruby
idhacks-workshop/
+-- parse_career_page.py
+-- get_stats.py
+-- raw_jobs_data.csv
+-- final_jobs_data.json
+-- visualization/
	+-- datamaps.usa.min.js
	+-- final_jobs_data.json
	+-- visualize_data.js
	+-- index.html
```

### Building the viz - *index.html*

Let's start with easy stuff first.

The main thing our HTML page `index.html` is going to do is *call* our javascripts. For this, we need to include 'script tags' to our three libraries : **D3**, **TopoJSON**, and **DataMaps**.

Oh, and we also want our viz to look pretty, so we're going to include a sexy Google Font in a css tag.

`index.html` so far:

```html
<!-- css -->
<link rel="stylesheet" type="text/css" href="http://fonts.googleapis.com/css?family=Roboto+Condensed">

<!-- javascript -->
<script src="//cdnjs.cloudflare.com/ajax/libs/d3/3.5.3/d3.min.js"></script>
<script src="//cdnjs.cloudflare.com/ajax/libs/topojson/1.6.9/topojson.min.js"></script>
<script src="datamaps.usa.min.js"></script>


<style>
    body {
        font: "Roboto Condensed", Helvetica, sans-serif;
    } 
</style>

```

Finally we're going to add two div tags. One that we're going to **inject the title into**:

```html
<div id="title" style="width: 1000px; height: 5px; font-family: 'Roboto Condensed';"></div>
```

And another that we're going to **inject the map** itself into:

```html
<div id="container" style="position: relative; left: -100px; width: 800px; height: 600px; font-family: 'Roboto Condensed';"></div>
```

Altogeher now, here's `index.html`:

```html
<!-- css -->
<link rel="stylesheet" type="text/css" href="http://fonts.googleapis.com/css?family=Roboto+Condensed">

<!-- javascript -->
<script src="//cdnjs.cloudflare.com/ajax/libs/d3/3.5.3/d3.min.js"></script>
<script src="//cdnjs.cloudflare.com/ajax/libs/topojson/1.6.9/topojson.min.js"></script>
<script src="datamaps.usa.min.js"></script>


<style>
    body {
        font: "Roboto Condensed", Helvetica, sans-serif;
    } 
</style>


<!-- d3 tags -->
<div id="title" style="width: 1000px; height: 5px; font-family: 'Roboto Condensed';"></div>
<div id="container" style="position: relative; left: -100px; width: 800px; height: 600px; font-family: 'Roboto Condensed';"></div>


<script src="visualize_data.js"></script>
```


### Building the viz - *visualize_data.js*

Finally, the meat of the visualization is going to go in `visualize_data.js`.

First, we want to create a stylish title for our visual. We can do that in a chain of function calls as follows:


```javascript
d3.select("#title").append("svg")
            .attr("width", 900)
            .attr("height", 50)
            .append("text")
            .attr("x", 100)
            .attr("y", 40)
            .style("font-size", "24px")
            .text("Jumbo Graduates in the United States");
```

What this does is it *selects* the `title` div tag we created in `index.html` and injects our text... with width, height and position attributes. Whoa!

We can, in fact, do this again to tag on a little subtitle to our div tag:

```javascript
d3.select("#title").append("svg")
            .attr("width", 900)
            .attr("height", 50)
            .append("text")
            .attr("x", 100)
            .attr("y", 20)
            .attr("fill", "#989898")
            .style("font-size", "14px")
            .text("Domestic first outcomes of Tufts graduates (hover for statistics)");
```

Now for the grand finale, we make a call to the [DataMap API](http://datamaps.github.io/) (which if you remember, we downloaded to our directory and included as a script tag in `index.html`). Basically how we do this is we *pass in a dictionary* with a bunch of arguments to tell our map to behave a certain way. Things like *where* to inject our map:

```javascript
  element: document.getElementById('container'),
```

what *kind* of map we want:

```javascript
  scope: 'usa',
```

where to get our *data*:

```javascript
dataUrl : "final_jobs_data.json",
```

how to *fill in* our map from the data:

```javascript
	fills: {
        "0" : "#EAE7E6",
        "1-9": '#C1B7B2',
        "10-19": '#988780',
        "20-49": '#6E574D',
        "50-99": '#593F33',
        "100+": '#300F00',
        defaultFill: '#EAE7E6'
    },
```

AND what kind of html to display when we *hover over states*:

```javascript
  popupTemplate: function(geography, data) { 
    // html for a hovering tooltip 
    return '<div style="border-radius:10px; padding: 10px; position: relative; top: -50px; right: -50px; opacity: 0.85;" class="hoverinfo"><b><div style="font-size:20px">' + geography.properties.name + '</div></b>' + "<br>" + 
    '<b>Reported # of grads:</b> &#09;' +  data["number of graduates"] + '<br>' +        
    '<b>Most popular position:</b> &#09;' +  data["most popular title"] + '<br>' +
    '<b>Most popular destination:</b> &#09;' +  data["most popular city"] + '<br>' +
    '<b>Most popular institution:</b> &#09;' +  data["most popular company"] + '<br>';
    }
},
```

Finally, at the end, we include a little legend for our map with the following call:

```javascript
map.legend();
```
And voilà, we have our script to create a map viz!

```javascript
d3.select("#title").append("svg")
            .attr("width", 900)
            .attr("height", 50)
            .append("text")
            .attr("x", 100)             
            .attr("y", 40)
            .style("font-size", "24px")
            .text("Jumbo Graduates in the United States");

d3.select("#title").append("svg")
            .attr("width", 900)
            .attr("height", 50)
            .append("text")
            .attr("x", 100)             
            .attr("y", 20)
            .attr("fill", "#989898")
            .style("font-size", "14px")
            .text("Domestic first outcomes of Tufts graduates (hover for statistics)");

var map = new Datamap({
  element: document.getElementById('container'),
  scope: 'usa',
  geographyConfig: {
  popupTemplate: function(geography, data) { 
    // html for a hovering tooltip 
    return '<div style="border-radius:10px; padding: 10px; position: relative; top: -50px; right: -50px; opacity: 0.85;" class="hoverinfo"><b><div style="font-size:20px">' + geography.properties.name + '</div></b>' + "<br>" + 
    '<b>Reported # of grads:</b> &#09;' +  data["number of graduates"] + '<br>' +        
    '<b>Most popular position:</b> &#09;' +  data["most popular title"] + '<br>' +
    '<b>Most popular destination:</b> &#09;' +  data["most popular city"] + '<br>' +
    '<b>Most popular institution:</b> &#09;' +  data["most popular company"] + '<br>';
    }
},
  fills: {
        "0" : "#EAE7E6",
        "1-9": '#C1B7B2',
        "10-19": '#988780',
        "20-49": '#6E574D',
        "50-99": '#593F33',
        "100+": '#300F00',
        defaultFill: '#EAE7E6'
    },
dataUrl : "final_jobs_data.json",

});
map.legend();
```

Now you're left wondering one (probably among many) question - how the hell do I actually *see* my visualization?

### Displaying your viz using SimpleHTTPServer

We've finished our visualization - now let's mount it on a server to see it in action!

Time to whip out a handy **terminal**. First, `cd` into our `visualization/` directory:

```bash
cd visualization/
```

Using Python's `SimpleHTTPServer` module, we're going to *serve this entire directory*:

```bash
python -m SimpleHTTPServer
```

Drum-roll please...

If we open up a browser window and hit `localhost:8000`, behold our visualization in its full glory!

![alt text](imgs/served.png)


### Hosting and sharing your viz using GithubPages

Oh man, oh man, we made it! Now for the final important step - sharing our viz. 

To do this we're going to use [github pages](https://pages.github.com/) to host our served directory. 

You can find out how to best do that [here](https://help.github.com/articles/creating-project-pages-manually/). 

Check out the final visualization hosted on our github page right [here](http://tuftsenigma.github.io/idhacks-workshop/visualization/)!








