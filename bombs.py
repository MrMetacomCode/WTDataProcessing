import os
import json
import discord
import random
import pickle
import logging
from datetime import date
from discord import Intents
from discord.ext import commands, tasks
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler

SPREADSHEET_ID = '1S-AIIx2EQrLX8RHJr_AVIGPsQjehEdfUmbwKyinOs_I'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
value_input_option = "USER_ENTERED"

# Setup for Google Spreadsheet to be able to pull from it.
creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()


# Updates values to the given input range on the given spreadsheet.
def update_values(input_range, updated_values, spreadsheet_id):
    request = sheet.values().update(spreadsheetId=spreadsheet_id, range=input_range,
                                    valueInputOption=value_input_option,
                                    body={"values": updated_values}).execute()
    values = input_range.split("!")
    values_ = values[1]
    print(f"Values {values_} updated.")


# Reads the values of the given input range from the given spreadsheet.
def read_values(input_range, spreadsheet_id):
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=input_range).execute()
    values = result.get('values', [])
    return values


SPREADSHEET_ID = '1S-AIIx2EQrLX8RHJr_AVIGPsQjehEdfUmbwKyinOs_I'
american_bombs = 'Bomb Table!B19:D29'
spreadsheet_values = read_values(american_bombs, SPREADSHEET_ID)
print(spreadsheet_values)

directory = 'bombguns'
bomb_name_final = ""
filename = ""
bomb_mass = 0
bomb_explosive_mass = 0
new_bomb_names = []
for filename in os.listdir(directory):
    file = os.path.join(directory, filename)
    if os.path.isfile(file):
        opened_file = open(file)
        filename = opened_file.name.split("\\")[1]
        if filename.startswith("us"):
            for line in opened_file:
                if "bombName" in line:
                    bomb_name1 = line.split(": ")
                    bomb_name2 = bomb_name1[1]
                    bomb_name3 = bomb_name2[1:-3]
                    if "_" in bomb_name3:
                        bomb_name4 = bomb_name3.split("_")
                        bomb_name5 = ""
                        for x in range(len(bomb_name4)):
                            if x > 0:
                                bomb_name5 = f"{bomb_name5}{bomb_name4[x]}"
                            else:
                                bomb_name5 = bomb_name4[x]
                        bomb_name_final = bomb_name5
                        new_bomb_names.append(bomb_name_final)
                    else:
                        bomb_name_final = bomb_name3
                        new_bomb_names.append(bomb_name_final)
                elif "mass" in line:
                    mass_in_kg1 = line.split(": ")
                    mass_in_kg2 = mass_in_kg1[1]
                    mass_in_kg3 = mass_in_kg2[:-2]
                    bomb_mass = float(mass_in_kg3)
                elif "explosiveMass" in line:
                    explosivemass1 = line.split(": ")
                    explosivemass2 = explosivemass1[1]
                    explosivemass3 = float(explosivemass2[:-2])
                    bomb_explosive_mass = explosivemass3

if bomb_name_final != "" and filename != "":
    for bomb in spreadsheet_values:
        if bomb[0] == bomb_name_final.upper():
            print(f"{filename}, {bomb_name_final}, {bomb_mass}, {bomb_explosive_mass}")
