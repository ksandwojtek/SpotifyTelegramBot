from colorama import init, Fore
from dotenv import load_dotenv
import datetime
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import sys
import os
import yt_dlp
from urllib import request as rq
from pytube import YouTube
from youtube_search import YoutubeSearch
import io
from spotify import find_and_download_song
import requests

client_credentials_manager = SpotifyClientCredentials(
    client_id="ff4080297d9345d981420e2f1bf8900d", client_secret="e6b8ef166d16429b8b5a9bb02bd025a6")
spotify = spotipy.Spotify(
    client_credentials_manager=client_credentials_manager)

init(autoreset=True)

load_dotenv("config.env")

sys.path.append("./libs")

api_key = os.getenv('TOKEN')
admin = os.getenv('ADMIN')
print(Fore.GREEN + "[+] Bot is starting...")
bot = telebot.TeleBot(api_key, parse_mode=None)


def statsUpdate(link_count=False, user_count=False):
    with open('data.json', 'r') as f:
        data = json.load(f)

    if user_count:
        data["users"] += 1
    if link_count:
        data["link"] += 1

    with open('data.json', 'w') as f:
        try:
            json.dump(data, f)
        except Exception as e:
            print(e)

    return


def getStats(link_count=False, user_count=False):
    f = open('data.json', 'r')
    data = json.load(f)
    f.close()

    if user_count:
        return data["users"]
    if link_count:
        return data["link"]

    return


def db_check(msg):
    with open('user_data.json', 'r+') as f:
        data = json.load(f)
        if str(msg.from_user.id) not in data["userdata"]:
            data["userdata"][msg.from_user.id] = {
                "username": msg.from_user.username,
                "first_name": msg.from_user.first_name,
                "last_name": msg.from_user.last_name,
                "id": msg.from_user.id
            }
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
        else:
            pass


@bot.message_handler(commands=['start'])
def start(message):
    db_check(message)
    statsUpdate(user_count=True)


@bot.message_handler(commands=['help'])
def help(message):
    db_check(message)
    bot.send_message(
        message.chat.id, "Send a spotify song link or just the song name or use /stats to see stats")


@bot.message_handler(commands=['stats'])
def stats(message):
    db_check(message)
    users = getStats(user_count=True)
    link_sent = getStats(link_count=True)
    bot.send_message(message.chat.id, f"Users: {users}")
    bot.send_message(message.chat.id, f"Generated videos: {link_sent}")


def extract_arg(arg):
    return arg.split()[1:]


def dict_to_list(dictionary: dict):
    return dict.keys()


@bot.message_handler(commands=['announce'])
def announce(message):
    db_check(message)
    if message.from_user.id == int(admin):
        arg_list = extract_arg(message.text)
        msg = ' '.join([str(elem) for elem in arg_list])
        with open("user_data.json", "r") as f:
            data = json.load(f)
            for user in data["userdata"]:
                bot.send_message(user, f"Announcement:\n{msg}")


@bot.message_handler(commands=['debug'])
def debug(message):
    db_check(message)
    if message.from_user.id == int(admin):
        switch = extract_arg(message.text)
        if switch[0] == "on":
            with open("debug.json", "r+") as f:
                data = json.load(f)
                status = data["status"]
                data["chat_id"] = message.chat.id
                if status is True:
                    bot.send_message(
                        message.chat.id, "Debug mode is already on")
                    return
                if status is False:
                    data["status"] = True
                    bot.send_message(message.chat.id, "Debug mode turned on")
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
        elif switch[0] == "off":
            with open("debug.json", "r+") as f:
                data = json.load(f)
                status = data["status"]
                data["chat_id"] = message.chat.id
                if status is False:
                    bot.send_message(
                        message.chat.id, "Debug mode is already off")
                    return
                if status is True:
                    data["status"] = False
                    bot.send_message(message.chat.id, "Debug mode turned off")
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
        else:
            return


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        bot.send_message(call.message.chat.id, "Please wait...")
        chat_id = call.message.chat.id
        choices = gen_markup(results["tracks"]["items"])[1]
        if call.data == choices[0]:
            name = results["tracks"]["items"][0]["name"]
            artist = results["tracks"]["items"][0]["artists"][0]["name"]
            song = find_and_download_song(f"{name} - {artist}")
            bot.send_message(chat_id, song[1])

            bot.send_audio(
                audio=song[0], title=name, performer=artist, chat_id=chat_id, timeout=2 * 3600)
        elif call.data == choices[1]:
            name = results["tracks"]["items"][1]["name"]
            artist = results["tracks"]["items"][1]["artists"][0]["name"]
            song = find_and_download_song(f"{name} - {artist}")
            bot.send_message(chat_id, song[1])

            bot.send_audio(
                audio=song[0], title=name, performer=artist, chat_id=chat_id, timeout=2 * 3600)
        elif call.data == choices[2]:
            name = results["tracks"]["items"][2]["name"]
            artist = results["tracks"]["items"][2]["artists"][0]["name"]
            song = find_and_download_song(f"{name} - {artist}")
            bot.send_message(chat_id, song[1])

            bot.send_audio(
                audio=song[0], title=name, performer=artist, chat_id=chat_id, timeout=2 * 3600)
        elif call.data == choices[3]:
            name = results["tracks"]["items"][3]["name"]
            artist = results["tracks"]["items"][3]["artists"][0]["name"]
            song = find_and_download_song(f"{name} - {artist}")
            bot.send_message(chat_id, song[1])

            bot.send_audio(
                audio=song[0], title=name, performer=artist, chat_id=chat_id, timeout=2 * 3600)
        elif call.data == choices[4]:
            name = results["tracks"]["items"][4]["name"]
            artist = results["tracks"]["items"][4]["artists"][0]["name"]
            song = find_and_download_song(f"{name} - {artist}")
            bot.send_message(chat_id, song[1])

            bot.send_audio(
                audio=song[0], title=name, performer=artist, chat_id=chat_id, timeout=2 * 3600)
        with open("debug.json", "r+") as f:
            data = json.load(f)
            status = data["status"]
            if status is True:
                bot.send_message(
                    text=f"(Debug)\n{name} - {artist}", chat_id=data["chat_id"])

                dt = datetime.datetime.fromtimestamp(original_msg.date)
                dt = dt.strftime("%d-%m-%Y %H:%M:%S")

                debug_link = {str(original_msg.from_user.id) + "/" + str(original_msg.date): {"url": Url, "user_id": original_msg.from_user.id, "chat_id": original_msg.chat.id, "username": original_msg.from_user.username,
                                                                                    "first_name": original_msg.from_user.first_name, "last_name": original_msg.from_user.last_name, "date": dt}}
                data["links"].update(debug_link)
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
        statsUpdate(link_count=True)
    except Exception as e:
        bot.send_message(chat_id, "Something went wrong! Please try again.")


def gen_markup(results: list):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    ids = []
    for result in results:
        ids.append(result["id"])
        artist = result["artists"][0]["name"]
        track = result["name"]
        full_name = (f"{track} - {artist}"[:30] + '...') if len(
            f"{track} - {artist}") > 30 else f"{track} - {artist}"
        markup.add(InlineKeyboardButton(

            text=full_name, callback_data=result["id"]))
    return markup, ids


@bot.message_handler(func=lambda message: True)
def on_message(message):
    chat_id = message.chat.id
    global original_msg
    global Url, results
    original_msg = message
    spotify_urls = ["open.spotify.com", "play.spotify.com"]
    Url = None
    if any(url in message.text for url in spotify_urls):
        Url = message.text
    else:
        Url = None
    best_url = None
    if Url is not None:
        try:
            track_id = Url.split("/")[-1].split("?")[0]
            track_name = spotify.track(track_id)["name"]
            artist_name = spotify.artist(spotify.track(
                track_id)["artists"][0]["id"])["name"]
            bot.send_message(
                chat_id, f"Looking for {track_name} - {artist_name}")
            results = spotify.search(
                f"{track_name} {artist_name}", limit=1, type="track")
            best_url = results["tracks"]["items"][0]["external_urls"]["spotify"]
            song = find_and_download_song(
                f"{track_name} - {artist_name}")
            bot.send_message(chat_id, song[1])
            bot.send_audio(
                audio=song[0], title=track_name, performer=artist_name, chat_id=chat_id, timeout=2 * 3600)
        except Exception as e:
            bot.send_message(
                chat_id, "Song not found or something went wrong! Please try again.")
            return
    else:
        search_query = message.text
        try:
            results = spotify.search(search_query, limit=5, type="track")
            track_id = results["tracks"]["items"][0]["id"]
            track_name = results["tracks"]["items"][0]["name"]
            artist_name = results["tracks"]["items"][0]["artists"][0]["name"]
            bot.send_message(
                chat_id, f"Searching {search_query} on Spotify")
            bot.reply_to(message, "Choose requested song:",
                reply_markup=gen_markup(results["tracks"]["items"])[0])
        except Exception as e:
            bot.send_message(
                chat_id, "Song not found or something went wrong! Please try again.")
            return




if __name__ == '__main__':
    bot.polling(timeout=10, long_polling_timeout=10)
