# This is a sample Python script.
from datetime import datetime
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import json
import os
import shutil
from re import match
import re


#def generate_concatenated_output() -> dict:
 #   files = {}
  #  for file in os.listdir("./inputData"):

   #     files.update(json.load(open("./inputData/"+file)))
    #result_file = open('./outputData/messages.json','w')
    #result_file.write(json.dumps(files))
    #return files
def get_participants() -> list:
    result = []
    opened_file = json.load(open("./enrichedData/enriched_message_1.json"))
    participants = {k: v for k, v in opened_file.items() if k.startswith('participants')}
    # flatten list
    #participants = sum(participants, [])
    for participant in participants.values():
        for value in participant:
            print(value.get("name"))
    return participants


def prepare_wordlist(filename = "entry_list_of_words.txt") -> list:
    result = []
    #wordlist = open("entry_list_of_words.txt", 'r')
    wordlist = open(filename, 'r')
    for line in wordlist:
        result.append(line[:-1])
    wordlist.close()
    return result

def first_meme_this_year() -> dict:
    first_meme_for_each_participant = {}
    messages = prepare_messages()
    for message in messages:
        if "reactions" in message.keys():
            if "photos" in message.keys():

                if message["sender_name"] in first_meme_for_each_participant.keys():
                    stored = datetime.strptime(first_meme_for_each_participant[message["sender_name"]]["timestamp_ms"], "%Y-%m-%d %H:%M:%S")
                    candidate = datetime.strptime(message["timestamp_ms"], "%Y-%m-%d %H:%M:%S")
                    beginning_of_the_year = datetime.fromtimestamp(1672531200)
                    #if message timestamp lower then currently stored message timestamp and message timestamp bigger than 1.01.2023
                    if stored > candidate >= beginning_of_the_year:
                        first_meme_for_each_participant[message["sender_name"]] = message
                else:
                    first_meme_for_each_participant[message["sender_name"]] = message

    return first_meme_for_each_participant

def the_biggest_tryhard() -> dict:
    the_biggest_tryhard_dict = {}
    messages = prepare_messages()
    for message in messages:
        if "photos" in message.keys():
            if "reactions" not in message.keys():
                if message["sender_name"] in the_biggest_tryhard_dict.keys():
                    the_biggest_tryhard_dict[message["sender_name"]] += 1
                else:
                    the_biggest_tryhard_dict[message["sender_name"]] = 1
    return the_biggest_tryhard_dict

def the_biggest_kremowkarz(substring_list = ["rzulty", "rzu\u00c5\u0082ty", "rzu\u00c5\u0082ci", "jp", "papaj", "papiez", "papie\u00c5\u00bc" ]) -> dict:
    the_biggest_kremowkarz_dict = {}
    messages = prepare_messages()
    for message in messages:
        if "content" in message.keys():
            for substring in substring_list:
                if message["content"].find(substring):
                    if message["sender_name"] in the_biggest_kremowkarz_dict.keys():
                        the_biggest_kremowkarz_dict[message["sender_name"]] += 1
                    else:
                        the_biggest_kremowkarz_dict[message["sender_name"]] = 1
    return the_biggest_kremowkarz_dict
def prepare_messages(listdir = "./enrichedData/") -> list:
    for file in os.listdir(listdir):
        opened_file = json.load(open(listdir+file))
        messages = list({k: v for k, v in opened_file.items() if k.startswith('messages')}.values())
        #flatten list
        messages = sum(messages, [])
    return messages
def translate_timestampt_to_date_time() -> dict:
    for file in os.listdir("./inputData"):
        opened_file = json.load(open("./inputData/"+file))
        messages = list({k: v for k, v in opened_file.items() if k.startswith('messages')}.values())
        #flatten list
        messages = sum(messages, [])
        #print(messages)
        for message in messages:
            message["timestamp_day"] = ""
            for key in message:
                if key == "timestamp_ms":
                    formatted_timestamp = datetime.fromtimestamp(message["timestamp_ms"] / 1000).strftime("%Y-%m-%d %H:%M:%S")
                    formatted_day  = datetime.fromtimestamp(message["timestamp_ms"] / 1000).strftime("%Y-%m-%d")
                    message["timestamp_ms"] = formatted_timestamp
                    message["timestamp_day"] = formatted_day

        opened_file = json.dumps(opened_file)
        enriched_file_name = "enriched_"+file
        with open("./enrichedData/"+enriched_file_name, 'w') as target:
            target.write(str(opened_file))



def get_messages_metadata() -> dict:
    all_messages = []
    photos_messages = []
    photos_messages_by_day_content= {str,list}
    photos_messages_by_day = {}
    messages_by_number_of_reactions = {}
    messages_by_author = {}
    messages_by_reaction = {}
    photos_by_reaction = {}
    entry_list_of_words = prepare_wordlist()
    result_map_of_words = {}
    for file in os.listdir("./enrichedData"):
        opened_file = json.load(open("./enrichedData/"+file))
        messages = list({k: v for k, v in opened_file.items() if k.startswith('messages')}.values())
        #flatten list
        messages = sum(messages, [])
        #print(messages)

        for message in messages:
            for key in message:
                if key == "photos":
                    photos_messages.append(message)
                elif key == "sender_name":
                   messages_by_author.setdefault((message[key]),0)
                   messages_by_author[message[key]] += 1
            #memes
            if "reactions" in message.keys():
                if "photos" in message.keys():
                    #messages_by_number_of_reactions[str(len(message.get('reactions')))] = message.get("photos")
                    messages_by_number_of_reactions.setdefault(str(len(message.get('reactions'))),[]).append(message.get("photos"))

                    photos_by_reaction.setdefault(message.get('sender_name'), {}).setdefault(str(len(message.get('reactions'))), [0])
                    current_value = photos_by_reaction.get(message.get('sender_name')).get(str(len(message.get('reactions'))))[0]
                    photos_by_reaction[message.get('sender_name')][(str(len(message.get('reactions'))))][0] = current_value+1
                    for reaction in message.get("reactions"):
                         messages_by_reaction.setdefault(reaction["actor"], 0)
                         messages_by_reaction[reaction["actor"]] += 1

                    #photos_messages_by_day_content[message["timestamp_day"]]
                    if message["timestamp_day"] in photos_messages_by_day:
                        photos_messages_by_day[message["timestamp_day"]] += 1
                    else:
                        photos_messages_by_day[message["timestamp_day"]] = 1

            all_messages.append(message)

        for message in messages:
            for key in message:
                if key == "content":
                    for words in entry_list_of_words:
                        if re.search(words, message.get("content"), re.IGNORECASE):
                            number_of_occurences = re.findall(words, message.get("content"), re.IGNORECASE)
                            current_number_of_occurences = result_map_of_words.get(words)
                            if current_number_of_occurences is None:
                                result_map_of_words[words] = 0
                            #result_map_of_words[words] += 1
                            result_map_of_words[words] += len(number_of_occurences)

        #print(result_map_of_words)



        results = {
            "Team:\n"
            "all_messages(including photos)": len(all_messages),
            "all_photos_sent": len(photos_messages),
            "most popular words": result_map_of_words,
            "photos_messages_by_day": photos_messages_by_day,
            "messages_by_number_of_reactions": messages_by_number_of_reactions,
            "Individual:\n"
            "Meme King/ Meme Queen": photos_by_reaction,
            "Najszybszy memiarz/Najszybsza memiara na zachodzie + Największy leniuszek ": first_meme_this_year(),
            "Nagroda im. Remigiusza Mroza": messages_by_author,
            "The biggest tryhard (a k a, don't leave me hanging)": the_biggest_tryhard(),
            "Kremówkarz/kremówkara": the_biggest_kremowkarz(),
            "Ninja": "value",
            "Participation award": "value",
            "Altruistic": messages_by_reaction,
            "Parcie na szkło": "value",
            "The meme king/the meme queen": "value",
            "Casual mefedron enjoyer": "Najwięcej wiadomości wysłanych w ciągu jednego dnia",
            "Martin Scorsese": "memy nieobrazkowe",
            "Największy leniuszek": "value"}







        #messages.update({k: v for k, v in messages.items() if k.startswith('messages')})
        #files.update({k: v for k, v in messages.items() if k.startswith('messages')})
        #files.update(messages)
        metadata_results = open('./outputData/metadata_results.json', 'w')
        metadata_results.write(json.dumps(results, indent=4))
    return messages_by_number_of_reactions





def move_photos_to_proper_directories(messages: dict):
    for outer_key in messages:
        list_of_messages = messages.get(outer_key)
        for message in list_of_messages:
            for inner_key in message:
                src = "./"+inner_key.get("uri")
                dst = "./outputData/photos/"+outer_key+"/"+inner_key.get("uri")
                shutil.move(src,dst)







if __name__ == '__main__':
    #get_participants()
    map_of_messages_by_reactions = get_messages_metadata()
    #move_photos_to_proper_directories(map_of_messages_by_reactions)
    #translate_timestampt_to_date_time()

    #fastest_memer()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
