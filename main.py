# This is a sample Python script.

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
    opened_file = json.load(open("./inputData/message_1.json"))
    participants = {k: v for k, v in opened_file.items() if k.startswith('participants')}
    # flatten list
    #participants = sum(participants, [])
    for participant in participants.values():
        for value in participant:
            print(value.get("name"))
    return participants


def prepare_wordlist() -> list:
    result = []
    wordlist = open("entry_list_of_words.txt", 'r')
    for line in wordlist:
        result.append(line[:-1])
    wordlist.close()
    return result


def get_messages_metadata() -> dict:
    all_messages = []
    photos_messages = []
    messages_by_number_of_reactions = {}
    messages_by_author = {}
    messages_by_reaction = {}
    photos_by_reaction = {}
    entry_list_of_words = prepare_wordlist()
    result_map_of_words = {}
    for file in os.listdir("./inputData"):
        opened_file = json.load(open("./inputData/"+file))
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

            all_messages.append(message)
        for message in messages:
            for key in message:
                if key == "content":
                    for words in entry_list_of_words:
                        if re.search(words, message.get("content"), re.IGNORECASE):
                            current_number_of_occurences = result_map_of_words.get(words)
                            if current_number_of_occurences is None:
                                result_map_of_words[words] = 0
                            result_map_of_words[words] += 1

        print(result_map_of_words)
        results = {
            "all_messages(including photos)": len(all_messages),
            "all_photos_sent": len(photos_messages),
            "who reacted the most": messages_by_reaction,
            "who_posted_the_most": messages_by_author,
            "who_got_the_most_reactions": photos_by_reaction,
            #"numbers of messages by reactions": {
              #  "1" : len(messages_by_number_of_reactions["1"]),
              #  "2": len(messages_by_number_of_reactions["2"]),
               # "3": len(messages_by_number_of_reactions["3"]),
               # "4": len(messages_by_number_of_reactions["4"]),
               # "5": len(messages_by_number_of_reactions["5"]),
              #  "6": len(messages_by_number_of_reactions["6"]),
             #   "7": len(messages_by_number_of_reactions["7"]),
             #   "8": len(messages_by_number_of_reactions["8"])
        #    },
            "messages_by_number_of_reactions": messages_by_number_of_reactions,
            "most popular words": result_map_of_words
        }




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



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
