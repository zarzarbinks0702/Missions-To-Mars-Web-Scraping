# web-scraping-challenge

Web scraping project focusing on using BeautifulSoup, Splinter, and Python to scrape the internet for information about Mars. 06/1/221.

-------------------------------------------------------------

Used BeautifulSoup to scrape https://mars.nasa.gov/news/ for the latest news title and summary.
Used Splinter to search https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html for the url of the full-size featured image.
Used Pandas to scrape https://space-facts.com/mars/ for the table of Mars facts, then convert that table to a dataframe to clean and return as an HTML table.
Used BeautifulSoup to scrape https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars for full size images of Mars's four hemispheres.

Used flask to create an app to run the above processes automatically, save the results to MongoDB, then return the results to a webpage.
