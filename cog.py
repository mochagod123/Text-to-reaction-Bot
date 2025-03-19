import discord
from discord.ext import commands, tasks
import pykakasi
import asyncio

class Cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def add_reactions_from_text(self, message, text):
        kakasi = pykakasi.kakasi()
        result = kakasi.convert(text)
        
        error_moji = 0

        def text_to_discord_emoji(text):
            emoji_map = {chr(97 + i): chr(0x1F1E6 + i) for i in range(26)}
            num_emoji_map = {str(i): f"{i}️⃣" for i in range(10)}
            return [emoji_map[char.lower()] if char.isalpha() else num_emoji_map[char] if char.isdigit() else None for char in text if char.isalnum()]
        
        romaji_text = "".join(item["kunrei"] for item in result if "kunrei" in item)
        emojis = text_to_discord_emoji(romaji_text)
        
        for e in emojis:
            if e:
                try:
                    await message.add_reaction(e)
                    await asyncio.sleep(1)
                except Exception as err:
                    error_moji += 1
                    continue
        return error_moji

    @commands.command()
    @commands.cooldown(2, 30, type=commands.BucketType.guild)
    async def emoji_art(self, ctx: commands.Context, message: discord.Message, text: str):
        await self.add_reactions_from_text(message, text)
        await ctx.message.add_reaction("✅")

async def setup(bot):
    await bot.add_cog(Cog(bot))
