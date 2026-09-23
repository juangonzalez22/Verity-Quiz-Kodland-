import os
import discord
from discord.ext import commands, tasks
from services.trivia import get_question
from services.giphy import update_gif_cache
from utils.helpers import (
    LETTERS,
    ANSWER_TIMEOUT,
    record_answer,
    load_scores,
    build_question_embed,
    build_result_embed,
)

GIPHY_API_KEY = os.getenv("GIPHY_API_KEY")

class AnswerButton(discord.ui.Button):
    def __init__(self, letter):
        super().__init__(label=letter, style=discord.ButtonStyle.primary)
        self.letter = letter

    async def callback(self, interaction):
        await self.view.handle_answer(interaction, self.letter)

class QuizView(discord.ui.View):
    def __init__(self, author, question):
        super().__init__(timeout=ANSWER_TIMEOUT)
        self.author = author
        self.question = question
        self.message = None

        for letter in LETTERS[: len(question["options"])]:
            self.add_item(AnswerButton(letter))

    async def interaction_check(self, interaction):
        if interaction.user != self.author:
            await interaction.response.send_message(
                "This quiz belongs to someone else. Type `!quiz` to start your own!",
                ephemeral=True,
            )
            return False
        return True

    def reveal_answer(self, chosen=None):
        for button in self.children:
            button.disabled = True
            if button.letter == self.question["correct"]:
                button.style = discord.ButtonStyle.success
            elif button.letter == chosen:
                button.style = discord.ButtonStyle.danger
            else:
                button.style = discord.ButtonStyle.secondary

    async def handle_answer(self, interaction, letter):
        is_correct = letter == self.question["correct"]
        status = "correct" if is_correct else "wrong"
        entry = record_answer(interaction.user, is_correct)

        self.reveal_answer(chosen=letter)
        self.stop()
        await interaction.response.edit_message(
            embed=build_result_embed(self.question, status, entry), view=self
        )

    async def on_timeout(self):
        entry = record_answer(self.author, False)
        self.reveal_answer()
        if self.message:
            await self.message.edit(
                embed=build_result_embed(self.question, "timeout", entry), view=self
            )

class QuizCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        if GIPHY_API_KEY and not self.refresh_gifs.is_running():
            self.refresh_gifs.start()

    def cog_unload(self):
        if self.refresh_gifs.is_running():
            self.refresh_gifs.cancel()

    @tasks.loop(hours=1)
    async def refresh_gifs(self):
        await update_gif_cache()

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!")

    @commands.command()
    async def quiz(self, ctx):
        question = await get_question()
        if not question:
            await ctx.send("Could not load questions from API or local file.")
            return

        view = QuizView(ctx.author, question)
        view.message = await ctx.send(embed=build_question_embed(question), view=view)

    @commands.command()
    async def points(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        entry = load_scores().get(str(member.id))

        if not entry:
            await ctx.send(f"{member.display_name} hasn't played yet. Type `!quiz`!")
            return

        accuracy = round(entry["correct"] / entry["answered"] * 100)
        embed = discord.Embed(
            title=f"📊 Stats for {member.display_name}",
            color=discord.Color.blurple(),
        )
        embed.add_field(name="Points", value=str(entry["points"]))
        embed.add_field(name="Correct", value=f"{entry['correct']}/{entry['answered']}")
        embed.add_field(name="Accuracy", value=f"{accuracy}%")
        embed.set_thumbnail(url=member.display_avatar.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def ranking(self, ctx):
        scores = load_scores()
        if not scores:
            await ctx.send("No scores yet. Be the first with `!quiz`!")
            return

        top = sorted(scores.values(), key=lambda e: e["points"], reverse=True)[:10]
        medals = ["🥇", "🥈", "🥉"]

        lines = []
        for position, entry in enumerate(top):
            prefix = medals[position] if position < 3 else f"**{position + 1}.**"
            lines.append(f"{prefix} {entry['name']} — {entry['points']} pts")

        embed = discord.Embed(
            title="🏆 Leaderboard",
            description="\n".join(lines),
            color=discord.Color.gold(),
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(QuizCog(bot))