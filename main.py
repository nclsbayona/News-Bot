import os
import discord
from discord.ext import tasks
from getNews import getLatestNews, printArticle
from datetime import datetime
from web_alive import keep_alive

api_key = os.environ['NEWS_API_KEY']

channel_id = os.environ['CHANNEL_ID']

bot_token = os.environ['BOT_TOKEN']

class News_Bot_Client(discord.Client):
  def __init__(self, api_key, channel_id:int, country_code="us", *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.channel_id=channel_id
    self.channel=None
    self.country_code=country_code
    self.api_key=api_key
    self.latest_news=list()
    self.getLatest.start()
  
  async def on_ready(self):
    print(f'Logged in as {self.user} (ID: {self.user.id})')
    print('------')

  @tasks.loop(hours=1) 
  async def getLatest(self):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    try:
      if (self.channel is None):
        self.channel=self.get_channel(self.channel_id)
      if (self.country_code==""):
        raise Exception()
      await (self.channel).send("Current Time ="+ current_time)
      the_news=getLatestNews(self.country_code, self.api_key)
      if (len(self.latest_news)==0):
        self.latest_news=the_news
        for (msg) in (the_news):
          await (self.channel).send(printArticle(msg))
      elif (the_news!=self.latest_news):
        new_news=list()
        for (art) in (the_news):
          if (art not in self.latest_news):
            new_news.insert(0, art)
            self.latest_news.insert(0, art)
            if (len(self.latest_news)>1):
              self.latest_news.pop()
        for (msg) in (new_news):
          await (self.channel).send(printArticle(msg))
        await (self.channel).send('\n')
  
    except:
      await (self.channel).send("Please update country code")
      
  @getLatest.before_loop
  async def before_getLatest(self):
    await self.wait_until_ready()

client = News_Bot_Client(api_key, int(channel_id), "co")
keep_alive()
client.run(bot_token)