import os
import discord
from traceback import print_exc
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
    self.counter=0
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
    try:
      if (self.channel is None):
        self.channel=self.get_channel(self.channel_id)
      if (self.country_code==""):
        raise Exception()
      now = datetime.now()
      current_time = now.strftime("%H:%M:%S")
      await (self.channel).send("Current Time ="+ current_time+'\n'+"The news at the moment are:\n")
      self.counter+=1
      the_news=getLatestNews(self.country_code, self.api_key)
      new_news=the_news
      if (self.counter==1):
        self.latest_news=the_news
      else:
        new_news=list()
        for (artic) in (the_news):
          if (artic not in self.latest_news):
            self.latest_news.append(artic)
            new_news.append(artic)
      for (i, art) in enumerate(new_news):
        await (self.channel).send("Article #"+str(i)+'\n'+printArticle(art))

      # Reset latest_news if it's a new day
      self.counter%=24
      if (self.counter==0):
        self.latest_news.clear()
  
    except:
      print_exc()
      await (self.channel).send("Please update country code")
      
  @getLatest.before_loop
  async def before_getLatest(self):
    await self.wait_until_ready()

client = News_Bot_Client(api_key, int(channel_id), "co")
keep_alive()
client.run(bot_token)