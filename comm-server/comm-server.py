#!/usr/bin/env python3
print( "Content-type: text/html\n")
import cgitb
import cgi
import json
import datetime
import sqlite3
import datetime
cgitb.enable()
"""
# related files are:
  * name_to_msg.json -- maps names to the message they will send\
  * msg_history.txt  -- keeps track of the msgs that were sent. This is used to retrieve msgs - 
                        aka send them to the clients. Also cool to see history.
"""


DEFAULT_MSG = "I'm shouting and barfing hysterically"

def receive_msgs_to_hist_and_dict(data):
    """
    function that updates the file msg_history.txt with a new msg request
    Arguments:
        data {} -- data of form {"sender": string_sender_name, "password":123456}
    """
    # take the msg that corresponds to the name in the json file, revert it to default for future use, and send the msg to msg_history.txt
    # if name is not in the json file, then add it and assign default msg
    with open("name_to_msg.json", 'r') as name_to_msg_file:
        name_to_msg = json.load(name_to_msg_file)

        print("<br> Name to msg===\n")
        print(name_to_msg)
        print("<br>Sender name=", data["sender"].value)
        sender_name = data["sender"].value
        # if the sender is in the dict, then use the msg that's mapped there
        if sender_name in name_to_msg:
            msg_to_send = name_to_msg[sender_name]
        else:
            msg_to_send = DEFAULT_MSG
        # in any case, revert back the msg in the dict to the default now
        # this also adds the sender if it didn't exist in the dict
        name_to_msg[sender_name] = DEFAULT_MSG
    with open("name_to_msg.json", 'w') as name_to_msg_file:
        # wrtie back to json
        json.dump(name_to_msg, name_to_msg_file)

    # now actually send the msg (write to text file)
    with open("msg_history.txt", "a") as hist_file:
        timestamp = datetime.datetime.now()
        hist_file.write(sender_name +"@"+ str(timestamp.hour)+":"+str(timestamp.minute) +" " + msg_to_send +"\n" )

        # now clients would be able to grab the last lines of the txt file to get updated messages
        # visualize the file



        
    
    



if __name__ == "__main__":
    #ask that the info will bi in the form of asdfgefs/dataHandler.py?command=getLast
    #command below takes the arguements from the get request and puts them in some sort of a dictionary
    inDataDict = cgi.FieldStorage()
    # update the msg_history.txt file with the new msg
    receive_msgs_to_hist_and_dict(inDataDict)
