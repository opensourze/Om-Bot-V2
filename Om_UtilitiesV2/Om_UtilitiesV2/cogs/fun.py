import os
import random
from asyncio import sleep
from urllib.parse import quote

import discord
import requests
import xkcd
from discord.ext import commands
from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_option
from pyfiglet import Figlet


class Fun(commands.Cog, description="Some fun commands - who doesn't want fun?"):
    def __init__(self, client):
        self.client: commands.Bot = client
        self.emoji = "<:fun:911380380089745408> "

    async def discord_together(self, ctx, option):
        try:
            author_vc = ctx.author.voice.channel.id
            link = await self.client.dt.create_link(author_vc, option)

            await ctx.send(
                f"Click the **link itself** to start the activity. Your friends can then click the play button to join.\n\n(Expires in 24 hours)\n"
                + str(link)
            )

        except AttributeError:
            await ctx.send("❌ You need to be in a voice channel to use this command.")

    # xkcd command
    @commands.command(help="Get the latest/random xkcd comic")
    async def xkcd(self, ctx, *, type="latest"):
        if type.lower() == "random":
            comic = xkcd.getRandomComic()
        elif type.lower() == "latest":
            comic = xkcd.getLatestComic()
        else:
            return await ctx.send(
                "❌ Please use `random` or `latest`! Leaving it blank will give you the latest comic."
            )

        embed = discord.Embed(
            title=f"Comic {comic.number}: {comic.title}",
            url=comic.link,
            colour=self.client.colour,
            description=f"[Click here if you need an explanation]({comic.getExplanation()})",
        )
        embed.set_footer(text=comic.getAltText())
        embed.set_image(url=comic.getImageLink())

        await ctx.send(embed=embed)

    @cog_ext.cog_slash(
        name="xkcd",
        description="Get the latest/random xkcd comic",
        options=[
            create_option(
                name="type",
                description="Whether to get a random comic or the latest one. Default is latest",
                required=False,
                option_type=3,
                choices=["Random", "Latest"],
            )
        ],
    )
    async def xkcd_slash(self, ctx: SlashContext, *, type="Latest"):
        await ctx.defer()
        await self.xkcd(ctx, type=type)

    # dog command
    @commands.command(help="Get a random dog image", aliases=["doggo"])
    async def dog(self, ctx):
        json = requests.get("https://some-random-api.ml/img/dog").json()

        embed = discord.Embed(title="Here's a doggo", colour=self.client.colour)
        embed.set_image(url=json["link"])

        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="dog", description="Get a random dog image")
    async def dog_slash(self, ctx: SlashContext):
        await self.dog(ctx)

    # cat command
    @commands.command(help="Get a random cat image", aliases=["kitty"])
    async def cat(self, ctx):
        json = requests.get("https://some-random-api.ml/img/cat").json()

        embed = discord.Embed(title="Here's a kitty", colour=self.client.colour)
        embed.set_image(url=json["link"])

        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="cat", description="Get a random cat image")
    async def cat_slash(self, ctx: SlashContext):
        await self.cat(ctx)

    # Bean
    @commands.command(help="A fake ban command")
    @commands.guild_only()
    async def bean(self, ctx, member: commands.MemberConverter, *, reason=None):
        embed = discord.Embed(
            title="✅ Member beaned",
            colour=self.client.colour,
            description=f"{member.mention} was beaned by {ctx.author.mention}",
        ).add_field(name="Reason", value=reason)

        await ctx.send(embed=embed)

    @cog_ext.cog_slash(
        name="bean",
        description="A fake ban command",
        options=[
            create_option(
                name="member",
                description='The member to "bean"',
                required=True,
                option_type=6,
            ),
            create_option(
                name="reason",
                description='Why you want to "bean" this member',
                required=False,
                option_type=3,
            ),
        ],
    )
    @commands.guild_only()
    async def bean_slash(self, ctx: SlashContext, member, *, reason=None):
        await self.bean(ctx, member, reason=reason)

    # Warm
    @commands.command(help="A fake warn command")
    @commands.guild_only()
    async def warm(self, ctx, member: commands.MemberConverter, *, reason: str):
        embed = discord.Embed(
            title="✅ Member warmed",
            description=f"{member.mention} has been warmed by {ctx.author.mention}",
            colour=self.client.colour,
        )
        embed.add_field(name="Reason", value=reason)

        await ctx.send(embed=embed)

    @cog_ext.cog_slash(
        name="warm",
        description="A fake warn command",
        options=[
            create_option(
                name="member",
                description='The member to "warm"',
                required=True,
                option_type=6,
            ),
            create_option(
                name="reason",
                description='Why you want to "warm" this member',
                required=True,
                option_type=3,
            ),
        ],
    )
    @commands.guild_only()
    async def warm_slash(self, ctx: SlashContext, member, *, reason=None):
        await self.warm(ctx, member, reason=reason)

    # YouTube Together
    @commands.command(
        brief="Watch YouTube together with friends",
        help="Connect to a voice channel and run this command to watch YouTube together with other server members without streaming!",
        aliases=["yt"],
    )
    @commands.guild_only()
    async def youtube(self, ctx):
        await self.discord_together(ctx, "youtube")

    @cog_ext.cog_slash(
        name="youtube_together",
        description="Watch YouTube together in a voice channel",
    )
    async def yt_slash(self, ctx: SlashContext):
        await self.youtube(ctx)

    # Chess
    @commands.command(
        brief="Play chess with friends in a voice channel",
        help="Connect to a voice channel and run this command to play chess together with other server members directly in the channel!",
        aliases=["chesstogether"],
    )
    @commands.guild_only()
    async def chess(self, ctx):
        await self.discord_together(ctx, "chess")

    @cog_ext.cog_slash(
        name="chess_together",
        description="Play chess with friends in a voice channel",
    )
    async def chess_slash(self, ctx: SlashContext):
        await self.chess(ctx)

    # Betrayal.io
    @commands.command(
        brief="Play Betrayal.io with friends in a voice channel",
        help="Connect to a voice channel and run this command to play Betrayal.io with other server members directly in the channel!",
        aliases=["betrayalio"],
    )
    @commands.guild_only()
    async def betrayal(self, ctx):
        await self.discord_together(ctx, "betrayal")

    @cog_ext.cog_slash(
        name="betrayalio_together",
        description="Play Betrayal.io with friends in a voice channel",
    )
    async def betrayal_slash(self, ctx: SlashContext):
        await self.betrayal(ctx)

    # Dad joke command
    @commands.command(help="Get a random dad joke")
    async def dadjoke(self, ctx):
        r = requests.get(
            url="https://icanhazdadjoke.com/",
            headers={
                "Accept": "application/json",
                "User-Agent": "OmUtilities (a Discord Bot) - https://OmUtilities.netlify.app | email: opensourze@protonmail.com",
            },
        )

        if not r.ok:
            return await ctx.send(
                "❌ The dad joke API has returned an error. Please try again later."
            )

        json = r.json()

        await ctx.send(json["joke"])

    @cog_ext.cog_slash(name="dadjoke", description="Get a random dad joke")
    async def dadjoke_slash(self, ctx: SlashContext):
        await self.dadjoke(ctx)

    # Bored command
    @commands.command(help="Gives you something to do if you're bored")
    async def bored(self, ctx):
        r = requests.get("https://www.boredapi.com/api/activity?participants=1&price=0")

        if r.status_code != 200:
            await ctx.send(
                "❌ The Bored API has returned an error. Please try again later."
            )
            return

        json = r.json()
        await ctx.send(json["activity"])

    @cog_ext.cog_slash(name="bored", description="Get something to do if you're bored")
    async def bored_slash(self, ctx: SlashContext):
        await ctx.defer()
        await self.bored(ctx)

    # Reddit/meme command
    @commands.command(
        help="Get a random meme from Reddit (optionally provide any subreddit)",
        brief="Get a random meme from Reddit",
        aliases=["reddit"],
    )
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def meme(self, ctx, subreddit=None):
        if subreddit:
            json = requests.get(
                f"https://meme-api.herokuapp.com/gimme/{subreddit}"
            ).json()
        else:
            json = requests.get(f"https://meme-api.herokuapp.com/gimme").json()

        try:
            if json["code"]:
                await ctx.send(
                    json["message"]
                )  # Send the error message if there is an error code
                return
        except KeyError:
            if json["nsfw"] == False:
                title = (
                    json["title"][:253] + "..."
                    if len(json["title"]) > 256
                    else json["title"]
                )
                meme_embed = discord.Embed(
                    title=title,
                    colour=self.client.colour,
                    url=json["postLink"],
                    description=f"r/{json['subreddit']}",
                )
                meme_embed.set_image(url=json["url"])
                await ctx.send(embed=meme_embed)

        if json["nsfw"]:
            await ctx.send(f"❗ Warning: NSFW post!\n\n<{json['postLink']}>")

    @cog_ext.cog_slash(
        name="reddit",
        description="Get a random post from meme subreddits, optionally provide a custom subreddit",
        options=[
            create_option(
                name="subreddit",
                description="Subreddit to get a post from (optional)",
                required=False,
                option_type=3,
            )
        ],
    )
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def reddit_slash(self, ctx: SlashContext, subreddit: str = None):
        await self.meme(ctx, subreddit=subreddit)

    # GIF command
    @commands.command(
        help="Search for GIFs (filtered) on Tenor",
        brief="Search for GIFs on Tenor",
        aliases=["tenor"],
    )
    async def gif(self, ctx, *, query):
        json = requests.get(
            f"https://g.tenor.com/v1/search?q={quote(query)}&contentfilter=medium&key={os.environ['TENORKEY']}"
        ).json()

        # Send first result
        try:
            await ctx.send(json["results"][0]["url"])
        except IndexError:
            await ctx.send("❌ Couldn't find any matching GIFs.")

    @cog_ext.cog_slash(name="gif", description="Search for GIFs (filtered) on Tenor")
    async def gif_slash(self, ctx: SlashContext, *, query):
        await self.gif(ctx, query=query)

    # 8ball command
    @commands.command(
        help="Ask the magic 8-ball a question", name="8ball", aliases=["eightball"]
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def eightball(self, ctx, *, question: str):
        # responses from wikipedia
        responses = [
            # Affirmative
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes, definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            # Non-committal
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not to tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            # Negative
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful.",
        ]
        random_response = random.choice(responses)

        message = await ctx.send(
            f'Your question was: "{question}"\n\n:8ball: *The magic 8-ball says...*',
            allowed_mentions=discord.AllowedMentions(users=False),
        )
        await sleep(2)
        # Edit message and add response after two seconds
        await message.edit(
            content=f'Your question was: "{question}"\n\n:8ball: *The magic 8-ball says...*\n**{random_response}**',
            allowed_mentions=discord.AllowedMentions(users=False),
        )

    @cog_ext.cog_slash(
        name="8ball",
        description="Ask the magic 8-ball a question",
        options=[
            create_option(
                name="question",
                description="What do you want to ask?",
                required=True,
                option_type=3,
            )
        ],
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def eightball_slash(self, ctx: SlashContext, question):
        await self.eightball(ctx, question=question)

    # Coin flip command
    @commands.command(help="Flip a coin", aliases=["coinflip", "flipcoin"])
    async def flip(self, ctx):
        if random.randint(1, 10) <= 5:
            await ctx.send("I flipped a coin for you, it's **heads**!")
        else:
            await ctx.send("I flipped a coin for you, it's **tails**!")

    @cog_ext.cog_slash(name="coinflip", description="Flip a coin")
    async def flip_slash(self, ctx: SlashContext):
        await self.flip(ctx)

    # Figlet/ASCII command
    @commands.command(help="Return text in ASCII art", aliases=["ascii"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def figlet(self, ctx, *, text):
        if len(text) >= 16:
            return await ctx.send(
                "❌ Your text is too long, please use text that is lesser than 16 characters."
            )

        ascii_text = Figlet(font="small").renderText(text)

        await ctx.send(f"```\n{ascii_text}\n```")

    @cog_ext.cog_slash(name="ascii", description="Return text in ASCII art")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def figlet_slash(self, ctx, *, text):
        await self.figlet(ctx, text=text)

    @commands.command(help="Play a simple game of slots")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def slots(self, ctx):
        responses = [
            "🍋",
            "🍊",
            "🍉",
            "7️⃣",
        ]
        embed = discord.Embed(
            title="🎰 Slot Machine 🎰",
            description="[ "
            + f"{random.choice(responses)} {random.choice(responses)} {random.choice(responses)}"
            + " ]",
            colour=self.client.colour,
        )
        if embed.description != "[ 7️⃣ 7️⃣ 7️⃣ ]":
            embed.set_footer(text="You need triple 7's to win.")
        else:
            embed.add_field(
                name="🎉 You win! Congrats!",
                value="It's pretty hard to win this!",
            )

        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="slots", description="Play a simple game of slots")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def slots_slash(self, ctx):
        await self.slots(ctx)

    # Mock text command
    @commands.command(help="Mock text (alternating upper and lower case)")
    async def mock(self, ctx, *, text):
        mock_text = "".join(
            [char.upper() if i % 2 else char.lower() for i, char in enumerate(text)]
        )

        await ctx.send(mock_text, allowed_mentions=discord.AllowedMentions(users=False))

    @cog_ext.cog_slash(
        name="mock",
        description="Mock text (alternating upper and lower case)",
    )
    async def mock_slash(self, ctx: SlashContext, *, text):
        await self.mock(ctx, text=text)


# Add cog
def setup(client):
    client.add_cog(Fun(client))
