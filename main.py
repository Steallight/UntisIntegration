import os
import datetime
from datetime import timedelta
from itertools import count

import discord

import webuntis
from aiohttp.log import client_logger
from dotenv import load_dotenv
from webuntis.utils.timetable_utils import table
from collections import defaultdict

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

server=os.getenv("UNTIS_SERVER")
username=os.getenv("UNTIS_USERNAME")
password=os.getenv("UNTIS_PASSWORD")
school=os.getenv("UNTIS_SCHOOL")
useragent='WebUntis Test'




# Beispiel: Mockup für PeriodObject-Daten
class PeriodObject:
    def __init__(self, data):
        self.id = data.get('id')
        self.date = data.get('date')
        self.startTime = data.get('startTime')
        self.endTime = data.get('endTime')
        self.kl = data.get('kl', [])
        self.te = data.get('te', [])
        self.su = data.get('su', [])
        self.ro = data.get('ro', [])
        self.lstext = data.get('lstext', '')
        self.lsnumber = data.get('lsnumber')
        self.sg = data.get('sg', '')  # Sicherstellen, dass `sg` immer einen Wert hat
        self.activityType = data.get('activityType', '')  # Sicherstellen, dass `activityType` immer einen Wert hat

    def __repr__(self):
        return f"Unterricht (Fach-ID: {self.su[0]['id'] if self.su else 'N/A'}, Lehrer-ID: {self.te[0]['id'] if self.te else 'N/A'}, Raum-ID: {self.ro[0]['id'] if self.ro else 'N/A'})"

with webuntis.Session(server=server, username=username,password=password,school=school,useragent=useragent).login() as s:

    today = datetime.date.today()

    start_date = today - datetime.timedelta(days=today.weekday())  # Start of the week (Monday)
    end_date = start_date + datetime.timedelta(days=15)

    klasse = s.klassen().filter(name="E1FS5")[0]

    table_extended = s.timetable_extended(klasse=klasse,start=start_date,end=end_date).to_table()




def erstelle_stundenplan(table_response):
    stundenplan = defaultdict(lambda: defaultdict(list))

    if not table_response:
        return "Keine Vertretungen vorhanden für diese Woche"

    stundenplan_str = ""

    for zeit, tage in table_response:
        for tag, period_objects in tage:
            if period_objects:
                for period in period_objects:
                    stundenplan[tag][zeit].append(period)

    for tag, zeiten in sorted(stundenplan.items()):

        german_weekday = tag.strftime("%A")  # Get the weekday name
        german_weekday_mapping = {
            "Monday": "Montag",
            "Tuesday": "Dienstag",
            "Wednesday": "Mittwoch",
            "Thursday": "Donnerstag",
            "Friday": "Freitag",
            "Saturday": "Samstag",
            "Sunday": "Sonntag"

        }
        german_weekday = german_weekday_mapping[german_weekday]

        stundenplan_str += f"Stundenplan für {german_weekday}, {tag.strftime('%d.%m.%Y')}:\n"
        for zeit, period_list in sorted(zeiten.items()):

            new_zeit = (datetime.datetime.strptime(zeit.strftime('%H:%M'), '%H:%M') + datetime.timedelta(
                minutes=45)).strftime('%H:%M')

            stundenplan_str += f"  {zeit.strftime('%H:%M')} - {new_zeit} - "
            for period in period_list:
                # Einzelne Attributabfragen mit Standardwerten, falls das Attribut fehlt
                activity_type = getattr(period, 'activityType', 'N/A')
                sg = getattr(period, 'sg', 'N/A')

                # Lehrer-ID, Raum-ID und Fach-ID prüfen und auf 'N/A' setzen, falls sie nicht existieren
                lehrer_id = period.te[0]['id'] if hasattr(period, 'te') and period.te and 'id' in period.te[
                    0] else 'N/A'
                raum_id = period.ro[0]['id'] if hasattr(period, 'ro') and period.ro and 'id' in period.ro[0] else 'N/A'
                fach_id = period.su[0]['id'] if hasattr(period, 'su') and period.su and 'id' in period.su[0] else 'N/A'

                stundenplan_str += f"{activity_type} ({sg}), Lehrer-ID: {lehrer_id}, Raum-ID: {raum_id}, Fach-ID: {fach_id} | "
            stundenplan_str += "\n"
        stundenplan_str += "\n" + "-" * 50 + "\n"
    return stundenplan_str



# Aufrufen der Funktion zur Anzeige des Stundenplans
stundenplan_finished = str(erstelle_stundenplan(table_extended))


client = discord.Client(intents=intents)

def cut_string(string, max_length):
    if len(string) <= max_length:
        return string
    else:
        return string[:max_length]

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.content == "!plan":




        embed = discord.Embed(
            colour=discord.Colour.blurple(),
            description=cut_string(stundenplan_finished, 4093)
        )
        await message.author.send(embed=embed)

client.run(os.getenv("DC_TOKEN"))