import os
import discord
from discord.ext import tasks
from getNews import getLatestNews, printArticle, getXataka_GenbetaNews
from datetime import datetime
from web_alive import keep_alive

api_key = os.environ['NEWS_API_KEY']

general_channel_id = os.environ['CHANNEL_ID']

bot_token = os.environ['BOT_TOKEN']

tech_channel_id = os.environ['TECH_CHANNEL_ID']

class News_Bot_Client(discord.Client):
  def __init__(self, api_key, general_channel_id:int, tech_channel_id:int, country_code="us", *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.counter=0
    self.channel_id=general_channel_id
    self.tech_channel_id=tech_channel_id
    self.tech_channel=None
    self.channel=None
    self.country_code=country_code
    self.api_key=api_key
    self.latest_news=list()
    self.tech_news=list()
    self.getLatest.start()
  
  async def on_ready(self):
    print(f'Logged in as {self.user} (ID: {self.user.id})')
    print('------')

  @tasks.loop(hours=2) 
  async def getLatest(self):
    try:
      if (self.country_code==""):
        raise Exception()
      now = datetime.now()
      current_time = now.strftime("%H:%M:%S")
      await (self.channel).send("Current Time ="+ current_time+'\n'+"The news at the moment are:\n")
      self.counter+=1
      # Reset latest_news if it's a new day
      self.counter%=24
      if (self.counter==0):
        self.latest_news=await self.getTech()
        # Delete all messages
        await (self.channel).purge(limit=100000)
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
        await (self.channel).send("Article #"+str(i+1)+'\n'+printArticle(art))
  
    except:
      await (self.channel).send("Please update country code")

  async def getTech(self):
    await (self.tech_channel).purge(limit=100000)
    now = datetime.date(datetime.now()).today()
    the_news=getXataka_GenbetaNews(self.api_key)
    await (self.tech_channel).send("Current Day ="+ str(now)+'\n'+"The {} tech news at the moment are:\n".format(len(the_news)))
    for (i, art) in enumerate(the_news):
      await (self.tech_channel).send("Article #"+str(i+1)+'\n'+printArticle(art))
    return the_news

  @getLatest.before_loop
  async def before_getLatest(self):
    await self.wait_until_ready()
    self.channel=self.get_channel(self.channel_id)
    await (self.channel).purge(limit=100000)
    self.tech_channel=self.get_channel(self.tech_channel_id)
    await (self.tech_channel).purge(limit=100000)
    self.latest_news=await self.getTech()

client = News_Bot_Client(api_key, int(general_channel_id), int(tech_channel_id), "co")
keep_alive()
client.run(bot_token)