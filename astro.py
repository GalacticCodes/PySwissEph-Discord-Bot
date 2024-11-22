import os
import discord
import swisseph as swe
import pytz
import numpy as np  
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from discord.ext import commands
from dotenv import load_dotenv
import sqlite3
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from math import pi, cos, sin
from matplotlib import transforms

# Load environment variables
load_dotenv()

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))

if not TOKEN:
    print("Error: Bot token not found. Please set it as an environment variable.")
    exit(1)
if not CHANNEL_ID:
    print("Error: Channel ID not found. Please set it as an environment variable.")
    exit(1)

# Configure bot and intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


# Dictionary of planets with Unicode symbols
PLANETS = {
    'Sun': (swe.SUN, '☉'),
    'Moon': (swe.MOON, '☽'),
    'Mercury': (swe.MERCURY, '☿'),
    'Venus': (swe.VENUS, '♀'),
    'Mars': (swe.MARS, '♂'),
    'Jupiter': (swe.JUPITER, '♃'),
    'Saturn': (swe.SATURN, '♄'),
    'Uranus': (swe.URANUS, '♅'),
    'Neptune': (swe.NEPTUNE, '♆'),
    'Pluto': (swe.PLUTO, '♇')
}
sign_colors = {
    "♈": "red",      # Aries - Fire
    "♉": "green",    # Taurus - Earth
    "♊": "goldenrod",   # Gemini - Air
    "♋": "blue",     # Cancer - Water
    "♌": "red",      # Leo - Fire
    "♍": "green",    # Virgo - Earth
    "♎": "goldenrod",   # Libra - Air
    "♏": "blue",     # Scorpio - Water
    "♐": "red",      # Sagittarius - Fire
    "♑": "green",    # Capricorn - Earth
    "♒": "goldenrod",   # Aquarius - Air
    "♓": "blue"      # Pisces - Water
}

# Zodiac signs with Unicode symbols only
signs = ["♈", "♉", "♊", "♋", "♌", "♍", "♎", "♏", "♐", "♑", "♒", "♓"]


def calculate_current_transits():
    now = datetime.now(pytz.utc)
    julian_day = swe.julday(now.year, now.month, now.day, now.hour + now.minute / 60.0)
    transit_details = f"**Current Transit Chart for {now.strftime('%Y-%m-%d %H:%M UTC')}**\n"

    return transit_details

import matplotlib.transforms as transforms

from matplotlib import transforms
import matplotlib.pyplot as plt
import numpy as np
import pytz
from datetime import datetime
import swisseph as swe

# Dummy data for planets and colors; replace with actual values if available
PLANETS = {
    'Sun': (swe.SUN, '☉'),
    'Moon': (swe.MOON, '☽'),
    'Mercury': (swe.MERCURY, '☿'),
    'Venus': (swe.VENUS, '♀'),
    'Mars': (swe.MARS, '♂'),
    'Jupiter': (swe.JUPITER, '♃'),
    'Saturn': (swe.SATURN, '♄'),
    'Uranus': (swe.URANUS, '♅'),
    'Neptune': (swe.NEPTUNE, '♆'),
    'Pluto': (swe.PLUTO, '♇')
}
signs = ["♈", "♉", "♊", "♋", "♌", "♍", "♎", "♏", "♐", "♑", "♒", "♓"]
sign_colors = {
    "♈": "red", "♉": "green", "♊": "goldenrod", "♋": "blue",
    "♌": "red", "♍": "green", "♎": "goldenrod", "♏": "blue",
    "♐": "red", "♑": "green", "♒": "goldenrod", "♓": "blue"
}

def create_astro_wheel():
    fig, ax = plt.subplots(figsize=(8, 10), subplot_kw={'projection': 'polar'})
    ax.set_theta_offset((1.5 * np.pi) - (np.pi / 2))
    ax.set_ylim(0, 1)

    # Offset transform for text alignment
    offset_transform = transforms.ScaledTranslation(0, -0.09, fig.dpi_scale_trans)

    # Draw zodiac sign divisions with colors and symbols
    for i, sign in enumerate(signs):
        angle = i * (np.pi / 6)
        color = sign_colors[sign]
        ax.plot([angle] * 2, [0, 1], color="grey", linewidth=0.8)
        ax.text(angle + np.pi / 12, 0.93, sign, ha="center", fontsize=21, fontweight="bold", color=color, transform=ax.transData + offset_transform)

    # Draw circles at specified radii
    theta = np.linspace(0, 2 * np.pi, 100)
    ax.plot(theta, [0.85] * 100, color="black", linestyle="-", linewidth=1)
    ax.plot(theta, [0.6] * 100, color="black", linestyle="-", linewidth=1)
    ax.fill_between(theta, 0.6, .85, color="lightblue", alpha=0.3)  # Light blue fill
    ax.fill_between(theta, 0.85, 1.0, color="antiquewhite", alpha=0.6)
    ax.fill_between(theta, 0.6, 0, color="antiquewhite", alpha=0.6)

    # Add tick marks at each degree with longer ticks every 10 degrees
    for degree in range(360):
        angle = degree * np.pi / 180
        start_radius = 0.81 if degree % 10 == 0 else 0.835
        end_radius = 0.85
        ax.plot([angle, angle], [start_radius, end_radius], color="black", linewidth=0.8)

    # Prepare date and time for the chart
    now = datetime.now(pytz.utc)
    current_time_str = now.strftime("%Y-%m-%d %H:%M UTC")
    julian_day = swe.julday(now.year, now.month, now.day, now.hour + now.minute / 60.0)

    # Dictionary to store planet angles for aspect calculation
    planet_positions = {}
    transit_details = ""

    # Plot planets on the chart
    for name, (planet_id, symbol) in PLANETS.items():
        try:
            result = swe.calc_ut(julian_day, planet_id)
            lon = result[0][0]
            angle = lon * np.pi / 180
            degree_in_sign = lon % 30
            zodiac_sign = int(lon // 30)

            # Display each planet symbol on the chart
            ax.text(angle, 0.75, symbol, fontsize=21, ha='center', va='center')
            ax.text(angle, 0.67, f"{degree_in_sign:.0f}°", fontsize=8, ha='center', va='center')
            ax.plot([angle, angle], [0.6, 0.58], color="black", linewidth=1.5)

            # Add planet information to transit details
            transit_details += f"{symbol} {name}: {degree_in_sign:.0f}° {signs[zodiac_sign]}\n"
            planet_positions[name] = angle

        except Exception as e:
            print(f"Error calculating position for {name}: {e}")

    # Define and plot aspects
    aspects = {
        "soft": [(60, "blue"), (120, "blue")],
        "hard": [(0, "red"), (90, "red"), (180, "red")]
    }
    buffer = 5 * (np.pi / 180)
    for planet1, angle1 in planet_positions.items():
        for planet2, angle2 in planet_positions.items():
            if planet1 != planet2:
                delta_angle = abs(angle1 - angle2)
                delta_angle = min(delta_angle, 2 * np.pi - delta_angle)
                for aspect_type, aspect_list in aspects.items():
                    for aspect_deg, color in aspect_list:
                        aspect_rad = aspect_deg * (np.pi / 180)
                        if aspect_rad - buffer <= delta_angle <= aspect_rad + buffer:
                            ax.plot([angle1, angle2], [0.58, 0.58], color=color, linewidth=1)
                            break

    # Hide polar coordinates and display
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.grid(False)

    # Chart details and title text
    title_text = "The Stellar Compass\n!Transit Chart"
    plt.gcf().text(0.12, 0.95, title_text, ha='left', fontsize=18, va='top', family='monospace')
    plt.gcf().text(0.71, 0.95, f"Transit Details -\n {current_time_str}\n{transit_details}", ha='left', fontsize=9, va='top')

    subtitle_text = "The sky as it is in this moment."
    plt.gcf().text(0.12, 0.89, subtitle_text, ha='left', fontsize=12, va='top', family='monospace')

    chart_details_text = (
        f"Chart Type: Whole Sign Tropical Astrology Live Transit\n"
        f"This is an open source project under AGPL license using PySwissEph.\n"
        f"View source code at: https://github.com/GalacticCodes/PySwissEph-Discord-Bot"
    )

    # Add birth details at the top of the figure
    plt.gcf().text(0.12, 0.87, chart_details_text, ha='left', fontsize=6, va='top', family='monospace')


    # Save the image
    plt.savefig("astro_wheel.png", bbox_inches="tight", dpi=100)
    plt.close(fig)



@bot.command(name='transit')
async def transit(ctx):
    """Send the current transits and astrological wheel when requested."""
    transit_message = calculate_current_transits()
    create_astro_wheel()
    await ctx.send(transit_message)
    await ctx.send(file=discord.File("astro_wheel.png"))

# SQLite database setup
db_path = "birth_details.db"

# Connect to the database and create table if it doesn’t exist
def initialize_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS birth_details (
            user_id INTEGER PRIMARY KEY,
            date_of_birth TEXT,
            time_of_birth TEXT,
            latitude REAL,
            longitude REAL
        )
    ''')
    conn.commit()
    conn.close()

# Function to save user birth details in the database
def save_birth_details(user_id, date_of_birth, time_of_birth, latitude, longitude):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        REPLACE INTO birth_details (user_id, date_of_birth, time_of_birth, latitude, longitude)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, date_of_birth, time_of_birth, latitude, longitude))
    conn.commit()
    conn.close()

# Initialize the database when the script starts
initialize_db()

# Dictionary to temporarily store birth details for each user
user_birth_data = {}

@bot.command(name='set-birth-details')
async def set_birth_details(ctx):
    """Command to start collecting birth details."""
    user = ctx.author
    await user.send("Hello! Let's gather your birth details to generate your natal chart.")
    await user.send("Please enter your date of birth (format: YYYY-MM-DD):")
    user_birth_data[user.id] = {"step": "date_of_birth"}  # Start with date of birth

@bot.event
async def on_message(message):
    """Handle user responses for birth details collection."""
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    user_id = message.author.id
    channel = message.channel

    # Check if the user is in the process of entering birth details
    if user_id in user_birth_data:
        user_data = user_birth_data[user_id]

        if user_data["step"] == "date_of_birth":
            # Store date of birth and move to the next step
            user_data["date_of_birth"] = message.content
            user_data["step"] = "time_of_birth"
            await channel.send("Got it! Now, please enter your time of birth (format: HH:MM, use 24-hour format):")

        elif user_data["step"] == "time_of_birth":
            # Store time of birth and move to the next step
            user_data["time_of_birth"] = message.content
            user_data["step"] = "latitude"
            await channel.send("Thank you! Now, please enter your birth location's latitude in decimal degrees (e.g., 40.7128 for New York):")

        elif user_data["step"] == "latitude":
            # Store latitude and move to the next step
            try:
                user_data["latitude"] = float(message.content)
                user_data["step"] = "longitude"
                await channel.send("Great! Now, please enter your birth location's longitude in decimal degrees (e.g., -74.0060 for New York):")
            except ValueError:
                await channel.send("Please enter a valid decimal number for latitude.")

        elif user_data["step"] == "longitude":
            # Store longitude and complete the process
            try:
                user_data["longitude"] = float(message.content)
                user_data["step"] = "complete"
                
                # Save the data in the database
                save_birth_details(
                    user_id=user_id,
                    date_of_birth=user_data["date_of_birth"],
                    time_of_birth=user_data["time_of_birth"],
                    latitude=user_data["latitude"],
                    longitude=user_data["longitude"]
                )
                
                # Confirm data saving
                await channel.send("Thank you! Your birth details have been saved successfully.")
                del user_birth_data[user_id]  # Clean up after saving
            except ValueError:
                await channel.send("Please enter a valid decimal number for longitude.")

    await bot.process_commands(message)

# Function to retrieve user birth details from the database
def get_birth_details(user_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT date_of_birth, time_of_birth, latitude, longitude FROM birth_details WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result  # Returns None if user data is not found

@bot.command(name='show-birth-details')
async def show_birth_details(ctx):
    """Command to display saved birth details for the user."""
    user_id = ctx.author.id
    details = get_birth_details(user_id)
    
    if details:
        # Unpack the details and display them
        date_of_birth, time_of_birth, latitude, longitude = details
        await ctx.send(f"Your saved birth details:\n"
                       f"**Date of Birth**: {date_of_birth}\n"
                       f"**Time of Birth**: {time_of_birth}\n"
                       f"**Latitude**: {latitude}\n"
                       f"**Longitude**: {longitude}")
    else:
        await ctx.send("You have not saved your birth details yet. Use `!set-birth-details` to enter them.")

def calculate_natal_chart(date_of_birth, time_of_birth, latitude, longitude):
    year, month, day = map(int, date_of_birth.split("-"))
    hour, minute = map(int, time_of_birth.split(":"))
    julian_day = swe.julday(year, month, day, hour + minute / 60.0)

    # Calculate positions of planets
    natal_chart = {}
    for name, (planet_id, symbol) in PLANETS.items():
        result = swe.calc_ut(julian_day, planet_id)
        
        # Extract only the longitude value from the result
        lon = result[0][0] if isinstance(result[0], tuple) else result[0]
        natal_chart[name] = (lon, symbol)  # Store longitude and symbol

    return natal_chart




def create_natal_chart_image(natal_chart, user_name, date_of_birth, time_of_birth, latitude, longitude, north_node):
    fig, ax = plt.subplots(figsize=(8, 10), subplot_kw={'projection': 'polar'})
    ax.set_theta_offset((1.5 * pi) - (pi / 2))
    ax.set_ylim(0, 1)

    # Offset transform for slight downward positioning
    offset_transform = transforms.ScaledTranslation(0, -0.09, fig.dpi_scale_trans)

    # Draw zodiac signs and divisions
    for i, sign in enumerate(signs):
        angle = i * (pi / 6)
        color = sign_colors[sign]
        ax.plot([angle] * 2, [0, 1], color="grey", linewidth=0.8)
        ax.text(angle + pi / 12, 0.93, sign, ha="center", fontsize=21, fontweight="bold", color=color, transform=ax.transData + offset_transform)

    # Add circles for structure
    theta = np.linspace(0, 2 * pi, 100)
    ax.plot(theta, [0.85] * 100, color="black", linestyle="-", linewidth=1)
    ax.plot(theta, [0.6] * 100, color="black", linestyle="-", linewidth=1)
    ax.plot(theta, [0.18] * 100, color="black", linestyle="-", linewidth=1)
    ax.fill_between(theta, 0.6, .85, color="lightblue", alpha=0.3)  # Light blue fill
    ax.fill_between(theta, 0.85, 1.0, color="antiquewhite", alpha=0.6)
    ax.fill_between(theta, 0.6, 0, color="antiquewhite", alpha=0.6)

    # Degree tick marks
    for degree in range(360):
        angle = degree * pi / 180
        start_radius = 0.81 if degree % 10 == 0 else 0.835
        ax.plot([angle, angle], [start_radius, 0.85], color="black", linewidth=0.8)

    # Store planet positions for aspects
    planet_positions = {}
    header_data = []

    # Plot planets, Ascendant, North Node, and gather data for the header
    for name, (lon, symbol) in natal_chart.items():
        angle = np.radians(lon)
        degree_in_sign = lon % 30
        sign_index = int(lon // 30)

        # Plot planet symbols
        ax.text(angle, 0.75, symbol, fontsize=21, ha='center', va='center')
        ax.text(angle, 0.67, f"{int(degree_in_sign)}°", fontsize=8, ha='center', va='center')
        ax.plot([angle, angle], [0.6, 0.58], color="black", linewidth=1.5)
        planet_positions[name] = angle
        header_data.append([name, f"{int(degree_in_sign)}° {signs[sign_index]}", "-", ""])

    # Plot Ascendant and North Node

    nn_angle = np.radians(north_node)
   
    ax.text(nn_angle, 0.75, "☊", fontsize=21, ha='center', va='center', color="black")
    ax.plot([nn_angle, nn_angle], [0.6, 0.58], color="black", linewidth=1.5)

    # Add Ascendant and North Node to header data
    header_data.append(["☊", f"{int(north_node % 30)}° {signs[int(north_node // 30)]}", "-", ""])

    # Aspect lines
    for planet1, angle1 in planet_positions.items():
        for planet2, angle2 in planet_positions.items():
            if planet1 != planet2:
                delta_angle = abs(np.degrees(angle1 - angle2))
                delta_angle = min(delta_angle, 360 - delta_angle)
                for aspect_name, (aspect_angle, symbol, color) in aspect_symbols.items():
                    if aspect_angle - orb <= delta_angle <= aspect_angle + orb:
                        ax.plot([angle1, angle2], [0.58, 0.58], color=color, linewidth=1)
                        for data in header_data:
                            if data[0] == planet1:
                                data[3] += f"{symbol} "
                                break
                        break

    # Hide polar coordinates
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.grid(False)

    # Header with user details
    birth_details_text = (
        f"Name: {user_name}\n"
        f"Date of Birth: {date_of_birth.strftime('%Y-%m-%d')}\n"
        f"Time of Birth: {time_of_birth}\n"
        f"Latitude: {latitude}, Longitude: {longitude}"
    )
    plt.gcf().text(0.10, 0.95, "The Stellar Compass - Natal Chart", ha='left', fontsize=15, va='top', family='monospace')
    plt.gcf().text(0.10, 0.92, birth_details_text, ha='left', fontsize=10, va='top', family='monospace')

    # Planet table on the right
    planet_table = "Planet  | Degree  | Aspects\n" + "-" * 28 + "\n"
    for planet, degree, _, aspects in header_data:
        planet_table += f"{planet:<8} {degree:<8} {aspects}\n"
    plt.gcf().text(0.69, 0.95, planet_table, ha='left', fontsize=8, va='top', family='monospace')

    chart_details_text = (
        f"Chart Type: Whole Sign Tropical Astrology Natal Chart\n"
        f"This is an open source project under AGPL license using PySwissEph.\n"
        f"View source code at: https://github.com/GalacticCodes/PySwissEph-Discord-Bot"
    )

    # Add birth details at the top of the figure
    plt.gcf().text(0.10, 0.85, chart_details_text, ha='left', fontsize=5, va='top', family='monospace')

    # Save as image
    plt.savefig("natal_chart.png", bbox_inches="tight", dpi=100)
    plt.close(fig)

@bot.command(name='natal-chart')
async def natal_chart(ctx):
    user_id = ctx.author.id
    details = get_birth_details(user_id)
    
    if details:
        date_of_birth_str, time_of_birth, latitude, longitude = details
        date_of_birth = datetime.strptime(date_of_birth_str, "%Y-%m-%d")
        natal_chart_data = calculate_natal_chart(date_of_birth_str, time_of_birth, latitude, longitude)

        # Parse for Ascendant and North Node calculation
        year, month, day = map(int, date_of_birth_str.split("-"))
        hour, minute = map(int, time_of_birth.split(":"))
        julian_day = swe.julday(year, month, day, hour + minute / 60.0)
        cusps, ascmc = swe.houses(julian_day, latitude, longitude, b'P')
        north_node = swe.calc_ut(julian_day, swe.MEAN_NODE)[0][0]

        create_natal_chart_image(
            natal_chart_data,
            user_name=ctx.author.display_name,
            date_of_birth=date_of_birth,
            time_of_birth=time_of_birth,
            latitude=latitude,
            longitude=longitude,
            north_node=north_node
        )
        
        await ctx.send(f"{ctx.author.mention}, here is your natal chart:")
        await ctx.send(file=discord.File("natal_chart.png"))
    else:
        await ctx.send("You have not saved your birth details yet. Use `!set-birth-details` to enter them.")


# Aspect symbols, angles, and colors
aspect_symbols = {
    "conjunction": (0, "☌", "red"),
    "sextile": (60, "∠", "blue"),
    "square": (90, "□", "red"),
    "trine": (120, "△", "blue"),
    "opposition": (180, "☍", "red")
}
orb = 5  # Tolerance in degrees for aspect calculations

# Function to plot natal and transit planets with aspects and detailed header
def create_transit_natal_chart_image(natal_chart, user_name, date_of_birth, time_of_birth, latitude, longitude):
    fig, ax = plt.subplots(figsize=(8, 10), subplot_kw={'projection': 'polar'})
    ax.set_theta_offset((1.5 * np.pi) - (np.pi / 2))  # Rotate chart
    ax.set_ylim(0, 1)

    # Set up a slight downward offset transform
    offset_transform = transforms.ScaledTranslation(0, -0.09, fig.dpi_scale_trans)

    # Draw zodiac sign divisions with color-coded symbols
    for i, sign in enumerate(signs):
        angle = i * (np.pi / 6)
        color = sign_colors[sign]
        ax.plot([angle] * 2, [0, 1], color="grey", linewidth=0.8)
        ax.text(angle + np.pi / 12, 0.93, sign, ha="center", fontsize=21, fontweight="bold", color=color, transform=ax.transData + offset_transform)

   
    # Draw circles for chart structure
    theta = np.linspace(0, 2 * np.pi, 100)
    ax.plot(theta, [0.85] * 100, color="black", linewidth=1)
    ax.plot(theta, [0.6] * 100, color="black", linewidth=1)
    ax.plot(theta, [0.70] * 100, color="black", linewidth=.6)
    # Add a light blue background between 0.85 and 1.0 radius
    theta = np.linspace(0, 2 * np.pi, 100)  # Create an array of angles from 0 to 2π
    ax.fill_between(theta, 0.6, .85, color="lightblue", alpha=0.3)  # Light blue fill
    ax.fill_between(theta, 0.85, 1.0, color="antiquewhite", alpha=0.6)
    ax.fill_between(theta, 0.6, 0, color="antiquewhite", alpha=0.6)

         # Add tick marks at each degree on .85 radius, with longer ticks every 10 degrees
    for degree in range(360):
        angle = np.radians(degree)  # Convert degree to radians

        # Set the radius for the start and end of the tick at .85 radius
        if degree % 10 == 0:
            start_radius = 0.83  # Medium tick for every 10 degrees
        else:
            start_radius = 0.84  # Small tick for each degree
        end_radius = 0.85
        ax.plot([angle, angle], [start_radius, end_radius], color="black", linewidth=0.8)

        # Add tick marks at each degree on 1.0 radius, with longer ticks every 10 degrees extending outward
    for degree in range(360):
        angle = np.radians(degree)

        # Set the start and end radius for inverted ticks at 1.0 radius
        if degree % 10 == 0:
            start_radius = 1.0       # Medium tick starting from 1.0
            end_radius = 1.02        # Extending to 1.02 for every 10 degrees
        else:
            start_radius = 1.0       # Small tick starting from 1.0
            end_radius = 1.01        # Extending to 1.01 for each degree

        # Draw the tick mark
        ax.plot([angle, angle], [start_radius, end_radius], color="black", linewidth=0.8)

    # Store natal and transit positions for aspect calculations
    natal_positions = {}
    transit_positions = {}

    # Prepare header data
    header_data = []

    # Plot natal planets (inner planets only for aspects)
    inner_planets = {"Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn"}
    for name, (lon, symbol) in natal_chart.items():
        angle = np.radians(lon)
        degree_in_sign = lon % 30
        sign_index = int(lon // 30)
        sign_name = signs[sign_index]

        # Place natal planet symbol
        ax.text(angle, 0.78, symbol, fontsize=18, ha='center', va='center')
        ax.text(angle, 0.73, f"{int(degree_in_sign)}°", fontsize=8, ha='center', va='center')
         # Draw a bold tick mark at the planet's position on the 0.6 radius circle
        ax.plot([angle, angle], [0.6, 0.58], color="black", linewidth=1.5)
        # Store natal inner planet positions for aspects
        if name in inner_planets:
            natal_positions[name] = angle

        # Add natal data to header
        natal_position = f"{int(degree_in_sign)}° {sign_name}"
        header_data.append([name, natal_position, "-", ""])  # Transit and Aspect to be updated

    # Calculate and plot current transit planets
    now = datetime.now(pytz.utc)
    julian_day_now = swe.julday(now.year, now.month, now.day, now.hour + now.minute / 60.0)
    outer_transit_planets = {"Pluto", "Neptune", "Uranus", "Saturn", "Jupiter"}

    for name, (planet_id, symbol) in PLANETS.items():
        try:
            # Get the current position of the transit planet
            result = swe.calc_ut(julian_day_now, planet_id)
            lon = result[0][0] if isinstance(result[0], tuple) else result[0]
            angle = np.radians(lon)
            degree_in_sign = lon % 30
            sign_index = int(lon // 30)
            sign_name = signs[sign_index]

            # Place transit planet symbol
            ax.text(angle, 0.63, symbol, fontsize=15, ha='center', va='center', color="green")
             # Draw a bold tick mark at the planet's position on the 0.6 radius circle
            ax.plot([angle, angle], [0.6, 0.58], color="green", linewidth=1.5)
            ax.text(angle, 0.67, f"{int(degree_in_sign)}°", fontsize=6, ha='center', va='center')
            # Store outer transit planet positions for aspect calculations
            if name in outer_transit_planets:
                transit_positions[name] = angle

            # Update header data with transit information
            transit_position = f"{int(degree_in_sign)}° {sign_name}"
            for data in header_data:
                if data[0] == name:
                    data[2] = transit_position
                    break
            else:
                header_data.append([name, "-", transit_position, ""])

        except Exception as e:
            print(f"Error calculating position for {name}: {e}")

    # Draw aspects between natal inner planets and outer transit planets
    for natal_name, natal_angle in natal_positions.items():
        for transit_name, transit_angle in transit_positions.items():
            angle_diff = abs(np.degrees(natal_angle - transit_angle))
            angle_diff = min(angle_diff, 360 - angle_diff)  # Wrap angle difference

            # Check if the angle difference is within any aspect angles
            for aspect_name, (aspect_angle, symbol, color) in aspect_symbols.items():
                if aspect_angle - orb <= angle_diff <= aspect_angle + orb:
                    ax.plot([natal_angle, transit_angle], [0.58, 0.58], color=color, linewidth=1)
                    
                    # Update the aspect symbol in the header data
                    for data in header_data:
                        if data[0] == natal_name:
                            data[3] += f" {symbol}"  # Append aspect symbol
                            break
                    break

    # Add house lines
    for i in range(12):
        angle = i * np.pi / 6
        ax.plot([angle, angle], [0, 1], color="gray", linestyle="--", linewidth=0.33)

    # Hide polar coordinates and display
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.grid(False)

    # Create header text with formatted positions and aspects
    header_text = "Planet  | Natal  | Transit  | Aspects\n" + "-" * 40 + "\n"
    for planet, natal_pos, transit_pos, aspects in header_data:
        header_text += f"{planet:<10} {natal_pos:<9} {transit_pos:<9} {aspects}\n"

    # Add header to the top of the figure
    plt.gcf().text(0.55, 0.97, header_text, ha='left', fontsize=8, va='top', family='monospace')

    title_text = "The Stellar Compass\n" 
     # Add header to the top of the figure
    plt.gcf().text(0.10, 0.97, title_text, ha='left', fontsize=18, va='top', family='monospace')

    chart_text = "!Natal-Transit Chart"
    plt.gcf().text(0.10, 0.94, chart_text, ha='left', fontsize=15, va='top', family='monospace')


     # Prepare header data and set up text for user’s birth details
    birth_details_text = (
        f"Name: {user_name}\n"
        f"Date of Birth: {date_of_birth.strftime('%Y-%m-%d')}\n"
        f"Time of Birth: {time_of_birth}\n"
        f"Latitude {latitude}, Longitude {longitude}\n"
        f"Transit Date: {now.strftime('%Y-%m-%d %H:%M UTC')}\n"
    )

    # Add birth details at the top of the figure
    plt.gcf().text(0.10, 0.915, birth_details_text, ha='left', fontsize=8, va='top', family='monospace')
    
    chart_details_text = (
        f"Chart Type: Whole Sign Tropical Astrology Natal-Transit\n"
        f"This is an open source project under AGPL license using PySwissEph.\n"
        f"View source code at: https://github.com/GalacticCodes/PySwissEph-Discord-Bot"
    )

    # Add birth details at the top of the figure
    plt.gcf().text(0.10, 0.855, chart_details_text, ha='left', fontsize=5, va='top', family='monospace')


    # Save the natal-transit chart as an image file
    plt.savefig("natal_transit_chart.png", bbox_inches="tight", dpi=100)
    plt.close(fig)


@bot.command(name='natal-transit')
async def natal_transit(ctx):
    """Generate and send the transit chart with aspects for the user."""
    user_id = ctx.author.id
    details = get_birth_details(user_id)
    
    if details:
        date_of_birth_str, time_of_birth, latitude, longitude = details

        # Automatically format `time_of_birth` if it's in HHMM format
        if len(time_of_birth) == 4 and time_of_birth.isdigit():
            time_of_birth = f"{time_of_birth[:2]}:{time_of_birth[2:]}"
        
        # Check if `time_of_birth` is now in the correct HH:MM format
        if ":" not in time_of_birth or len(time_of_birth.split(":")) != 2:
            await ctx.send("Time of birth should be in 'HH:MM' format. Please use `!set-birth-details` to update your time of birth.")
            return

        try:
            # Parse date_of_birth as a datetime object
            date_of_birth = datetime.strptime(date_of_birth_str, "%Y-%m-%d")
            
            # Ensure time_of_birth is parsed correctly
            hour, minute = map(int, time_of_birth.split(":"))

            user_name = ctx.author.display_name
            
            # Generate natal chart data
            natal_chart_data = calculate_natal_chart(date_of_birth_str, time_of_birth, latitude, longitude)
            
            # Generate and save the chart image with aspects
            create_transit_natal_chart_image(
                natal_chart_data,
                user_name=user_name,
                date_of_birth=date_of_birth,
                time_of_birth=time_of_birth,
                latitude=latitude,
                longitude=longitude
            )
            
            # Send the transit chart image to the Discord channel
            await ctx.send(f"{ctx.author.mention}, here is your transit chart with aspects:")
            await ctx.send(file=discord.File("natal_transit_chart.png"))

        except ValueError as e:
            # Handle errors in parsing time or date format
            await ctx.send(f"An error occurred with your birth details: {e}")
    
    else:
        await ctx.send("You have not saved your birth details yet. Use `!set-birth-details` to enter them.")

@bot.event
async def on_ready():
    print(f'Bot is online as {bot.user}')

def get_sun_position(julian_day):
    """Calculate the Sun's position on a given Julian Day."""
    position, _ = swe.calc_ut(julian_day, swe.SUN, swe.FLG_SWIEPH | swe.FLG_SPEED)
    return position[0]  # Only return the longitude in degrees

def calculate_exact_transit_aspects(natal_sun_position, year):
    """Calculate exact date and time when the transiting Sun forms specific aspects with natal Sun in a given year."""
    aspects = {
        "Sextile (60°)": (natal_sun_position + 60) % 360,
        "Square (90°)": (natal_sun_position + 90) % 360,
        "Trine (120°)": (natal_sun_position + 120) % 360,
        "Quincunx (150°)": (natal_sun_position + 150) % 360,
        "Opposition (180°)": (natal_sun_position + 180) % 360,
        "Quincunx (210°)": (natal_sun_position + 210) % 360,
        "Trine (240°)": (natal_sun_position + 240) % 360,
        "Square (270°)": (natal_sun_position + 270) % 360,
        "Sextile (300°)": (natal_sun_position + 300) % 360
    }

    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)
    transit_dates = {aspect: [] for aspect in aspects}

    current_date = start_date
    while current_date <= end_date:
        for hour in range(24):
            for minute in range(60):
                jd = swe.julday(current_date.year, current_date.month, current_date.day, hour + minute / 60.0)
                transiting_sun_position = get_sun_position(jd)
                for aspect, target_position in aspects.items():
                    if abs(transiting_sun_position - target_position) < 0.001:
                        exact_time = current_date + timedelta(hours=hour, minutes=minute)
                        transit_dates[aspect].append(exact_time.strftime("%Y-%m-%d %H:%M:%S UTC"))
        current_date += timedelta(days=1)
    return transit_dates


def save_as_pdf(transit_dates, year, name, birth_date, location, filename="Sun_Transit_Aspects.pdf"):
    """Save the transit aspects and dates as a PDF document with personal details."""
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    y_position = height - 50

    # Document title and personal details
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, y_position, f"{year} Vital Force Report")
    y_position -= 30
    c.setFont("Helvetica", 12)
    c.drawString(100, y_position, f"Name: {name}")
    y_position -= 15
    c.drawString(100, y_position, f"Date of Birth: {birth_date.strftime('%Y-%m-%d')}")
    y_position -= 15
    c.drawString(100, y_position, f"Location: {location}")
    y_position -= 30

    # Harmonious and challenging aspects columns
    vital_force_aspects = ["Trine (120°)", "Sextile (60°)", "Trine (240°)", "Sextile (300°)"]
    challenging_aspects = ["Quincunx (150°)", "Quincunx (210°)", "Square (90°)", "Square (270°)", "Opposition (180°)"]

    # Harmonious aspects
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, y_position, "Harmonious Aspects")
    y_position -= 20
    for aspect in vital_force_aspects:
        dates = transit_dates.get(aspect, [])
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(colors.blue)
        c.drawString(100, y_position, aspect)
        y_position -= 15
        c.setFont("Helvetica", 8)
        c.setFillColor(colors.black)
        for date in dates:
            c.drawString(120, y_position, f"- {date}")
            y_position -= 10
            if y_position < 80:
                c.showPage()
                y_position = height - 50

    # Challenging aspects
    c.setFont("Helvetica-Bold", 12)
    c.drawString(width / 2 + 50, height - 50, "Challenging Aspects")
    y_position = height - 80
    for aspect in challenging_aspects:
        dates = transit_dates.get(aspect, [])
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(colors.red)
        c.drawString(width / 2 + 50, y_position, aspect)
        y_position -= 15
        c.setFont("Helvetica", 8)
        c.setFillColor(colors.black)
        for date in dates:
            c.drawString(width / 2 + 70, y_position, f"- {date}")
            y_position -= 10
            if y_position < 80:
                c.showPage()
                y_position = height - 50

    c.save()



@bot.command(name="vital-force")
async def vital_force(ctx, year: int = datetime.now().year):
    """Discord command to calculate and save the Sun transit aspects PDF using birth details from the database."""
    user_id = ctx.author.id
    birth_details = get_birth_details(user_id)
    
    if birth_details is None:
        await ctx.send("Birth details not found for this user.")
        return

    # Extract birth details from the database result
    birth_date_str, time_of_birth, latitude, longitude = birth_details
    birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d")
    natal_jd = swe.julday(birth_date.year, birth_date.month, birth_date.day)
    natal_sun_position = get_sun_position(natal_jd)

    # Calculate transits
    transit_aspects = calculate_exact_transit_aspects(natal_sun_position, year)
    filename = f"{ctx.author.display_name}_Vital_Force_{year}.pdf"
    save_as_pdf(transit_aspects, year, ctx.author.display_name, birth_date, f"{latitude}, {longitude}", filename)

    # Send PDF file to Discord
    with open(filename, "rb") as pdf_file:
        await ctx.send(f"Here is the {year} Vital Force report for {ctx.author.display_name}:", file=discord.File(pdf_file, filename))

    # Remove the file after sending
    os.remove(filename)

# Remove the default help command
bot.remove_command("help")

@bot.command(name="help")
async def help_command(ctx):
    """Displays a list of available commands and their descriptions."""
    help_text = """
    
***AstroBot Command List:***

1. **!set-birth-details** - Start the process of entering your birth details...
2. **!show-birth-details** - Display your saved birth details...
3. **!natal-chart** - Generate and send your natal chart...
4. **!transit** - Display the current transit information...
5. **!natal-transit** - Generate a chart combining your natal planets with the current transiting planets...
6. **!vital-force [year]** - Generate a Vital Force report for a specified year...
7. **!suggestion** - Send a suggestion to Victoria and Matthew...
8. **!start** - Direction on how to begin...
9. **!help** - AstroBot Command List

Attention: This server is a public community.

***DIRECT MESSAGE THE COMMANDS TO THE BOT IF YOU WANT TO KEEP BIRTH DETIALS AND CHARTS PRIVATE***

Commands work either in DM or the channels. 
"""
    await ctx.send(help_text)

@bot.command(name="start")
async def help_command(ctx):
    """Displays a list of available commands and their descriptions."""
    help_text = """
    
To begin type `!set-birth-details` into any channel and you will recieve a DM from the astroBot to set your birth details. Then you will have success in using the following chart calculations.

***AstroBot Command List:***

1. **!set-birth-details** - Start the process of entering your birth details...
2. **!show-birth-details** - Display your saved birth details...
3. **!natal-chart** - Generate and send your natal chart...
4. **!transit** - Display the current transit information...
5. **!natal-transit** - Generate a chart combining your natal planets with the current transiting planets...
6. **!vital-force [year]** - Generate a Vital Force report for a specified year...
7. **!suggestion** - Send a suggestion to Victoria and Matthew...

**Example Usage:**
- `!set-birth-details` - Starts the process to enter your birth details.
- `!natal-chart` - Generates your natal chart.
- `!vital-force 2024` - Generates the Vital Force report for the year 2024.

Attention: This server is a public community.

***DIRECT MESSAGE THE COMMANDS TO THE BOT IF YOU WANT TO KEEP BIRTH DETIALS AND CHARTS PRIVATE***

Commands work either in DM or the channels. 
"""
    await ctx.send(help_text)

def initialize_suggestions_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS suggestions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            suggestion TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

initialize_suggestions_db()

@bot.command(name='suggestion')
async def suggestion(ctx, *, suggestion_text: str = None):
    """Allows users to submit a suggestion."""
    # Check if the suggestion_text was provided
    if suggestion_text is None:
        await ctx.send("Please provide a suggestion after the command, like `!suggestion Your suggestion here`.")
        return

    user_id = ctx.author.id
    username = str(ctx.author)

    # Store the suggestion in the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO suggestions (user_id, username, suggestion)
        VALUES (?, ?, ?)
    ''', (user_id, username, suggestion_text))
    conn.commit()
    conn.close()

    # Confirm submission to the user
    await ctx.send(f"Thank you for your suggestion, {ctx.author.mention}! Your feedback has been recorded.")

@bot.command(name='view-suggestions')
@commands.has_permissions(administrator=True)
async def view_suggestions(ctx, limit: int = 10):
    """Allows admins to view the latest suggestions."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT username, suggestion, timestamp FROM suggestions
        ORDER BY timestamp DESC
        LIMIT ?
    ''', (limit,))
    suggestions = cursor.fetchall()
    conn.close()

    if suggestions:
        suggestion_text = "\n\n".join([f"**{username}** at {timestamp}\n{suggestion}" for username, suggestion, timestamp in suggestions])
        await ctx.send(f"**Latest {limit} Suggestions:**\n\n{suggestion_text}")
    else:
        await ctx.send("No suggestions found.")

@bot.command(name='print-placements')
async def print_placements(ctx):
    """Generate and send all planetary placements, including Ascendant, MC, and North Node."""
    user_id = ctx.author.id
    details = get_birth_details(user_id)
    
    if details:
        date_of_birth_str, time_of_birth, latitude, longitude = details
        
        # Convert the date_of_birth from string format to datetime object
        date_of_birth = datetime.strptime(date_of_birth_str, "%Y-%m-%d")
        
        # Calculate natal chart data
        natal_chart = calculate_natal_chart(date_of_birth_str, time_of_birth, latitude, longitude)
        
        # Calculate Ascendant, MC, and North Node
        year, month, day = map(int, date_of_birth_str.split("-"))
        hour, minute = map(int, time_of_birth.split(":"))
        julian_day = swe.julday(year, month, day, hour + minute / 60.0)
        cusps, ascmc = swe.houses(julian_day, latitude, longitude, b'P')
        ascendant = ascmc[0]  # Ascendant
        mc = ascmc[1]         # Midheaven (MC)
        north_node = swe.calc_ut(julian_day, swe.MEAN_NODE)[0][0]  # Mean Node (North Node)
        
        # List of zodiac sign names
        sign_names = [
            "Aries", "Taurus", "Gemini", "Cancer", 
            "Leo", "Virgo", "Libra", "Scorpio", 
            "Sagittarius", "Capricorn", "Aquarius", "Pisces"
        ]
        
        # Format placements for display
        placements_message = "\n**Your Planetary Placements:**\n\n"
        for name, (lon, symbol) in natal_chart.items():
            degree_in_sign = lon % 30
            sign_index = int(lon // 30)
            placements_message += f"{symbol} {name}: {int(degree_in_sign)}° {sign_names[sign_index]}\n"
        
        # Add Ascendant, MC, and North Node
        placements_message += (
            f"Ascendant: {int(ascendant % 30)}° {sign_names[int(ascendant // 30)]}\n"
            f"Midheaven: {int(mc % 30)}° {sign_names[int(mc // 30)]}\n"
            f"North Node: {int(north_node % 30)}° {sign_names[int(north_node // 30)]}\n"
        )

        # Send the placements to the user
        await ctx.send(f"{ctx.author.mention}, here are your planetary placements:\n{placements_message}")
    
    else:
        await ctx.send("You have not saved your birth details yet. Use `!set-birth-details` to enter them.")



@bot.command(name='daily-aspects')
async def daily_aspects(ctx):
    """Print the aspects occuring in the sky on the current day."""
    now = datetime.now(pytz.utc)
    julian_day = swe.julday(now.year, now.month, now.day, now.hour + now.minute / 60.0)

    planet_positions = {}

    for name, (planet_id, _) in PLANETS.items():
        try:
            result = swe.calc_ut(julian_day, planet_id)
            lon = result [0][0] if isinstance(result[0], tuple) else result[0]
            planet_positions[name] = lon
        except Exception as e:
            print(f"Error calculating position for {name}: {e}")

        # Define aspects and their orbs
    aspects = {
        "Conjunction (☌)": 0,
        "Sextile (⚹)": 60,
        "Square (□)": 90,
        "Trine (△)": 120,
        "Opposition (☍)": 180
    }    

    orb = 5  # Tolerance in degrees

    # Find aspects between planets
    aspect_report = "**Daily Aspects for Today:**\n\n"
    checked_pairs = set()  # To avoid duplicate pairs

    for planet1, lon1 in planet_positions.items():
        for planet2, lon2 in planet_positions.items():
            if planet1 != planet2 and (planet1, planet2) not in checked_pairs and (planet2, planet1) not in checked_pairs:
                checked_pairs.add((planet1, planet2))
                delta = abs(lon1 - lon2)
                delta = min(delta, 360 - delta)  # Account for wrapping around the zodiac

                for aspect_name, aspect_angle in aspects.items():
                    if aspect_angle - orb <= delta <= aspect_angle + orb:
                        aspect_report += f"{planet1} {aspect_name} {planet2}\n"

    if aspect_report.strip() == "**Daily Aspects for Today:**":
        aspect_report += "No significant aspects today."

    # Send the aspect report to the user
    await ctx.send(f"{ctx.author.mention}, here are the aspects occurring today:\n{aspect_report}")


bot.run(TOKEN)
