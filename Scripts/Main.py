import time
import uuid

import pytchat
import requests
from gtts import gTTS
import os
import pygame
import threading
import queue
from mutagen.mp3 import MP3

pygame.mixer.init()

queued_audio = queue.Queue()


def play_audio():
    while True:
        if not queued_audio.empty():
            filename = queued_audio.get()

            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.delay(50)
            pygame.mixer.music.unload()
            os.remove(filename)


def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    filename = f"./tts/audio_{uuid.uuid4()}.mp3"  # Generate a unique filename
    tts.save(filename)
    audio = MP3(filename)

    if audio.info.length > 3:
        os.remove(filename)
        return

    if filename not in queued_audio.queue:
        queued_audio.put(filename)


#URL for sending commands to the server
command_url = "http://localhost:4567/v1/server/exec"

#Minecraft commands

name = ""

#/summon zombie ~ ~3 ~ {Health:10f,CustomName:'[{"text":"","color":"#ffff","bold":true}]',ArmorItems:[{},{},{},{id:"minecraft:turtle_helmet",Count:1b,tag:{Unbreakable:1b}}]}
give_sword = ""
zombie_spawn1 = "execute at PlonkerJimm run summon zombie ~ ~1 ~ {Health:1f,CustomName:'[{\"text\":\""
zombie_spawn2 = "\",\"color\":\"#8525cf\",\"bold\":true}]',ArmorItems:[{},{},{},{id:\"minecraft:turtle_helmet\",Count:1b,tag:{Unbreakable:1b}}]}"
creeper_spawn = "execute at PlonkerJimm run summon creeper ~ ~1 ~ {powered:1b,Attributes:[{Name:generic.follow_range,Base:1000}]}"
ender_spawn = "execute at PlonkerJimm run summon ender_dragon ~ ~ ~ {DragonPhase:8}"
warden_spawn = "execute at PlonkerJimm run summon warden ~ ~ ~"
#effect give PlonkerJimm instant_health 20 5
#mcstacker.net
#http://localhost:4567/swagger

threading.Thread(target=play_audio).start()

print("Input your stream id: ")
chat = pytchat.create(video_id=input())
while chat.is_alive():
    for c in chat.get().sync_items():
        message = c.message
        print(f"{c.datetime} [{c.author.name}]- {c.message}")
        if message.lower() == "creeper":
            headers = {
                'accept': '*/*',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            data = {
                'command': creeper_spawn,
                'time': ''
            }
            response = requests.post(command_url, headers=headers, data=data)
            print(response)
        elif message.lower() == "ender":
            headers = {
                'accept': '*/*',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            data = {
                'command': ender_spawn,
                'time': ''
            }
            response = requests.post(command_url, headers=headers, data=data)
            print(response)
        elif message.lower() == "warden":
            headers = {
                'accept': '*/*',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            data = {
                'command': warden_spawn,
                'time': ''
            }
            response = requests.post(command_url, headers=headers, data=data)
            print(response)
        else:#message.lower() == "zombie":
            headers = {
                'accept': '*/*',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            data = {
                'command': zombie_spawn1 + message + zombie_spawn2,
                'time': ''
            }
            response = requests.post(command_url, headers=headers, data=data)
            print(response)
            thread = threading.Thread(target=text_to_speech, args=(message,))
            thread.start()
