# -*- coding:utf-8 -*-
import codecs
import datetime
import json
import sched
import optparse
import os
import time
import TelethonB
import threading
import sys

from telethon import TelegramClient
from telethon import errors
from telethon.tl.functions.channels import LeaveChannelRequest
from telethon.tl.functions.channels import JoinChannelRequest


def create_settings():
    default = {"telegram_api":"Your api here",
               "api_hash": "Your hash here",
               "username":"Your username here",
               "#1/Xth ot the average activity(messages per runtime) required to not be marked as inactive. default: 1/3th":"",
               "min_activity":"3",
              }
    with codecs.open("config.txt", "w", encoding="utf-8") as config:
        for key in default:
            if default[key] != "":
                config.write("{}={}\n".format(key, default[key]))
            else:
                config.write("{}\n".format(key))
    print("[*] Please fill in your api data into the config.txt")


def read_settings():
    settings = dict()
    try:
        with codecs.open("config.txt", "r", encoding="utf-8") as config:
            data = config.readlines()
            for entry in data:
                if "#" not in entry:
                    entry = [entry.strip() for entry in entry.split("=")]
                    settings[entry[0]] = entry[1]
            config.close()
    except FileNotFoundError:
        print("[!] config.txt not found. Creating it...")
        self.create_settings()
        sys.exit()
    return settings


settings = read_settings()
client = TelegramClient(settings["username"], settings["telegram_api"], settings["api_hash"])
min_activity = settings["min_activity"]


async def main():

    # Now you can use all client methods listed below, like for example...
    # await client.send_message('me', 'Hello to myself!')

    # initialize_run
    dialogs = await client.get_dialogs(limit=5000)
    groups = list()
    dialog_names = set()

    for dialog in dialogs:
        try:
            groups.append(TelethonB.Channel(dialog, 0, min_activity, client)) #Creates list of channel objects
            dialog_names.add(dialog.name)
        except TypeError as e:
            print(e)
            continue
        except RuntimeError as e:
            print(e)
            continue
    print("[+] All groups successfully initialized!")

    # run
    count = 20000
    leave = False

    #read_leftout_groups()
    for channel in groups:
        print("[+] Running Channel: {}".format(channel.name))
        channel.run(count)


    # collect_data
    chatoutput = list()
    blacklist = set()
    join_groups = list()
    metadata = list()
    for channel in groups:
        print("Looking at channel:")
        print(channel.active)
        print(channel.output)
        print(channel.groups)
        print(channel.metadata)
        print(type(channel))
        print(channel)

        if channel.active:
            blacklist = blacklist.union(channel.groups_blocked)
            join_groups = join_groups.union(channel.groups)
            chatoutput.append(channel.output)
            print(chatoutput)
            metadata.append(channel.metadata)
            print(metadata)
        else:
            if leave:
                print("Should leave this group")

    # self.join_groups(join_groups, blacklist)
    # self.write_data(self.blacklist, "blocked_groups")
    # self.write_data(metadata, "groups.meta")
    # block_number = self.get_highest_chatblock()
    # self.write_data(chatoutput, "chat_block-{}".format(block_number))
    # self.write_leftout_groups()



    print("_--------------------all finished-------------------_")



with client:
    client.loop.run_until_complete(main())
