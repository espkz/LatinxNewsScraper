import requests as r
from bs4 import BeautifulSoup
import spacy, re, csv
from collections import Counter
from newspaper import Article

# tried to make a wordcloud but it's still more or less in progress
# from wordcloud import WordCloud
# import matplotlib.pyplot as plt


def extractData(key):
    """
    determines the top n number of collocates surrounding a corresponding key word
    1) Download Google News articles with key word search
    2) Parse each article to filter out stop words and punctuation
    3) Determine the top number of common collocates from the words
    :param key: key word to be tested
    Appends results to a csv file, along with the number of articles that were actually parsed to determine if there is too small of a sample size as needed
    """
    collective_data = {"Key Word" : key, "Articles Found" : None, "Articles Successfully Parsed" : None, "Top Collocates" : None}
    keywords = []
    skipcount = 0
    # top number of words goes here
    n = 15

    print("On key word: " + key)

    # get news articles from Google News
    gnresults = r.get('https://news.google.com/search?q=' + key + '%20when%3A1y&hl=en-US&gl=US&ceid=US%3Aen')
    soup = BeautifulSoup(gnresults.text, 'html.parser')
    articles = soup.select('article .DY5T1d.RZIKme')
    links = []
    base_url = 'https://news.google.com'
    for i in soup.select('article .DY5T1d.RZIKme'):
        ss = base_url + i.get('href')[1:]
        links.append(ss)
    collective_data["Articles Found"] = len(links)

    # get each article to parse
    for link in links:
        print("On article number " + str(links.index(link)+1))
        a = Article(url=link)
        try:
            a.download()
        except:
            print('Article ' + str(links.index(link)+1) + " not downloaded, skipping.")
            skipcount += 1
        try:
            a.parse()
        except:
            print('Article ' + str(links.index(link)+1) + " unable to be parsed, skipping.")
            skipcount += 1
        data = a.text

        # strip punctuation and white space and things
        article = re.sub(r'[^\w\s]','', data)
        new_article = " ".join(article.split())
        # print(new_article)

        # strip stop words and get general words
        nlp = spacy.load("en_core_web_sm")
        tag = ['PROPN', 'ADJ', 'NOUN']
        data = nlp(new_article.lower())
        for token in data:
            if (token.text in nlp.Defaults.stop_words):
                continue
            if token.pos_ in tag:
                keywords.append(token.text)

    # compile results
    collective_data["Articles Successfully Parsed"] = len(links) - skipcount
    top_keywords = Counter(keywords).most_common(n)

    # creating a wordcloud (scrapped for now)
    # compiled_keywords = " ".join(keywords)
    # wordcloud = WordCloud().generate(compiled_keywords)
    # plt.imshow(wordcloud)
    # # plt.axis("off") , interpolation='bilinear'
    # plt.show()
    # plt.imsave(key + '.jpg', wordcloud)


    for i in range(len(top_keywords)):
        collective_data[i] = top_keywords[i]

    # export top keywords into csv file
    with open("results.csv", 'a') as f:
        writer = csv.writer(f)
        writer.writerow(collective_data.values())

    f.close()
    print(top_keywords)



def main():
    """
    main function for iterating through keywords and downloading related news
    """
    # insert keywords here
    testing = ["hispanics", "latinos", "latinas", "latinx", "chicanos", "mexican americans", "puerto rican", "cubans"]


    columns = ["Key Word", "Articles Found", "Articles Successfully Parsed"]

    # initialize csv file for results
    with open("results.csv", 'w') as f:
        writer = csv.writer(f)
        writer.writerow(columns)
    f.close()

    # iterate through words to extract data
    # extractData(testing[0])
    for word in testing:
        extractData(word)


if __name__ == "__main__":
    main()


"""
Extra code that was attempted to use but it kind of failed so I'll just leave it here just in case

        # download article
        # try:
        #     news = r.get(link)
        # except:
        #     print("Cannot get link, skipping " + link + ", index number " + str(links.index(link)))
        #     continue
        # newssoup = BeautifulSoup(news.text, 'html.parser')
        # words = newssoup.findAll('p')
        # with open('news/article' + str(links.index(link)) + '.txt', 'a') as f:
        #     for line in words:
        #         f.write(line.get_text())
        # f.close()
        # article = ""
        # with open('news/article' + str(links.index(link)) + '.txt', 'r') as f:
        #     article = f.read()
        # f.close()
        # # os.remove('news/article.txt')
"""