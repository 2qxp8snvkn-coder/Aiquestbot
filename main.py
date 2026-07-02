import discord
from discord.ext import commands
import sqlite3

# Discord Bot Setup
intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix="!", intents=intents)

# SQLite Database Setup
conn = sqlite3.connect("tokens.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS tokens (
    token TEXT,
    owner TEXT,
    balance INTEGER DEFAULT 0,
    PRIMARY KEY (token)
)
""")
conn.commit()


def validate_token(token):
    c.execute("SELECT * FROM tokens WHERE token=?", (token,))
    return c.fetchone() is not None


quests_available = {
    "quest1": "Easy Quest",
    "quest2": "Medium Quest",
    "quest3": "Hard Quest"
}


class QuestSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label=quests_available["quest1"],
                value="quest1",
                emoji="🌟"
            ),
            discord.SelectOption(
                label=quests_available["quest2"],
                value="quest2",
                emoji="💪"
            ),
            discord.SelectOption(
                label=quests_available["quest3"],
                value="quest3",
                emoji="⚔️"
            )
        ]

        super().__init__(
            placeholder="Select a quest...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        selected_quest = self.values[0]

        user_data = c.execute(
            "SELECT * FROM tokens WHERE owner=?",
            (interaction.user.name,)
        )

        row = user_data.fetchone()

        if row and row[2] > 0:
            print(f"Executing {selected_quest} for {interaction.user.name}")

            c.execute(
                "UPDATE tokens SET balance=balance-1 WHERE owner=?",
                (interaction.user.name,)
            )
            conn.commit()

            await interaction.response.send_message(
                f"Quest '{selected_quest}' executed successfully!"
            )
        else:
            await interaction.response.send_message(
                "Insufficient credits or invalid request."
            )


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")


@bot.command()
async def connect(ctx, token: str):
    """Links your Discord account with an external token."""
    if validate_token(token):
        await ctx.send("Token already registered!")
    else:
        c.execute(
            "INSERT INTO tokens VALUES (?, ?, ?)",
            (token, ctx.author.name, 10)
        )
        conn.commit()
        await ctx.send("Token submitted! You have 10 credits.")


@bot.command()
async def do_quests(ctx):
    """Executes quests using stored credits."""

    view = discord.ui.View(timeout=None)
    select_menu = QuestSelect()

    view.add_item(select_menu)

    await ctx.send(
        "Which quest would you like to execute?",
        view=view
   )
import os

TOKEN = os.getenv("TOKEN")

bot.run(TOKEN)   
