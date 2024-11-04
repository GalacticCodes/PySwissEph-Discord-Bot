import os
import discord
import swisseph as swe
import pytz
from datetime import datetime
from discord.ext import commands

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
if not TOKEN:
    print("Error: Bot token not found. Please set it as an environment variable.")
    exit(1)

# Configure bot and intents
intents = discord.Intents.default()
intents.messages = False
bot = commands.Bot(command_prefix='!', intents=intents)

# Temporary storage for user data collection in steps
user_data = {}

# Start command to initiate the DM process
@bot.command(name='start')
async def start(ctx):
    """Start the birth detail input process in DM."""
    user = ctx.author
    await user.send("Hello! Let's get your birth details to calculate current transits.")
    await user.send("What is your birth date? (Format: YYYY-MM-DD)")
    user_data[user.id] = {'step': 'birth_date'}  # Start with birth date collection

# Handling messages in DMs
@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    # Check if the message is a DM
    if isinstance(message.channel, discord.DMChannel):
        user_id = message.author.id

        # Check if the user is in the process of providing data
        if user_id in user_data:
            if user_data[user_id]['step'] == 'birth_date':
                user_data[user_id]['birth_date'] = message.content
                user_data[user_id]['step'] = 'birth_time'
                await message.author.send("Got it! Now, what is your birth time? (Format: HH:MM, use 24-hour format)")
            elif user_data[user_id]['step'] == 'birth_time':
                user_data[user_id]['birth_time'] = message.content
                user_data[user_id]['step'] = 'birth_place'
                await message.author.send("Great! Finally, where were you born? (City, Country)")
            elif user_data[user_id]['step'] == 'birth_place':
                user_data[user_id]['birth_place'] = message.content
                await message.author.send("Thank you! Calculating your current transits...")

                # Calculate and send current transits
                birth_date = user_data[user_id]['birth_date']
                birth_time = user_data[user_id]['birth_time']
                birth_place = user_data[user_id]['birth_place']
                transit_message = calculate_current_transits(birth_date, birth_time, birth_place)
                await message.author.send(transit_message)

                # Clear user data after use
                del user_data[user_id]
        else:
            # If the user is not in the process, ignore
            await message.author.send("Please start by using the `!start` command in a server channel.")
    await bot.process_commands(message)

# Function to calculate transits using Swiss Ephemeris
def calculate_current_transits(birth_date, birth_time, birth_place):
    now = datetime.now(pytz.utc)
    julian_day = swe.julday(now.year, now.month, now.day, now.hour + now.minute / 60.0)

    # Example transit calculation
    transit_details = f"**Current Transits for {now.strftime('%Y-%m-%d %H:%M UTC')}**\n"
    for name, planet_id in PLANETS.items():
        lon, lat, dist = swe.calc_ut(julian_day, planet_id)
        zodiac_sign = int(lon // 30)  # Determine zodiac sign
        degree_in_sign = lon % 30     # Degree within the sign

        # Zodiac sign mapping
        signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", 
                 "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        sign_name = signs[zodiac_sign]
        
        transit_details += f"{name}: {degree_in_sign:.2f}° {sign_name}\n"

    return transit_details

# Example Swiss Ephemeris setup
swe.set_ephe_path('/path/to/ephemeris/files')  # Update this to the actual path of ephemeris files
PLANETS = {
    'Sun': swe.SUN,
    'Moon': swe.MOON,
    'Mercury': swe.MERCURY,
    'Venus': swe.VENUS,
    'Mars': swe.MARS,
    'Jupiter': swe.JUPITER,
    'Saturn': swe.SATURN,
    'Uranus': swe.URANUS,
    'Neptune': swe.NEPTUNE,
    'Pluto': swe.PLUTO
}

bot.run(TOKEN)
