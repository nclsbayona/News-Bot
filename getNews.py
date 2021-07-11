import requests
import os

def getLatestNews(country_code: str, api_key: str) -> list:
    the_news = requests.get(
        "https://newsapi.org/v2/top-headlines?country={}&apiKey={}".format(
            country_code, api_key
        )
    ).json()
    return list(the_news.get("articles"))


def printArticle(article: dict) -> str:
    ret="\n"
    ret+="From:"+ str(article.get("source").get("name"))+"\n"
    ret+="Author:"+ str(article.get("author"))+"\n"
    ret+="Title:"+ str(article.get("title"))+"\n"
    ret+="Description:"+ str(article.get("description"))+"\n"
    ret+="Url:"+ str(article.get("url"))+"\n"
    ret+="Publish date:"+ str(article.get("publishedAt"))+"\n"
    return ret


news = getLatestNews("co", os.environ["NEWS_API_KEY"])

if __name__=="__main__":
  for art in news:
    print(printArticle(art))