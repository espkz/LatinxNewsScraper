# LatinxNewsScraper
This is a web scraper designated to scrape news articles associate with a key word from Google News, then parse through the articles, trying to find the most common collocates around said key word.

# To Get Started
Attached is a txt file of requirements. To install through pip, type in the terminal as so:

pip install -r requirements.txt

# Results
The results of the keywords gets exported into a csv file called results.csv. As a note, running the program multiple times will cause the file to be overwritten, so it might be good to move the csv files away before running the program.

Each keyword is a row, with its column denoting the key word tested, the number of articles found (usually 100), and the number of articles that was able to be parsed with the program. The subsequent columns list out the top n number of collocates found in the news, in a tuple format of (word, frequency).

# Possible Issues and Improvements
 - Being able to extract 100+ articles
 - Issues parsing about 10-20% of the articles (this might be because the format of all newspaper articles online are different, and thus the package is inadequate to parse certain articles)
 - Exporting the results into a better visualization of data (wordcloud?)
