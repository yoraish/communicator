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
  * name_to_msg.json -- maps names to the message they will send
  * msg_history.txt  -- keeps track of the msgs that were sent. This is used to retrieve msgs - 
                        aka send them to the clients. Also cool to see history.
"""


DEFAULT_MSG = "I'm shouting and barfing hysterically"

def get_recent_msgs(num_msgs=3):
    out = ["" for _ in range(num_msgs)] # the msg at index 0 is the most recent
    with open("msg_history.txt", "r") as hist_file:
        for line in hist_file:
            # Advance msgs in the vector.
            # Pop the last one.
            out.pop()
            # Insert the most recent line
            out = [line] + out
        return out

def receive_msgs_to_hist_and_dict(data):
    """
    function that updates the file msg_history.txt with a new msg request
    Arguments:
        data {} -- data of form {"sender": string_sender_name, "password":123456, "cmd" : command_string, "new_msg": msg_string}
        command string could be:
            * "send"       -- send the stored msg to everyone
            * "set_msg"    --  set the awaiting msg to be a custom msg
                * "new_msg_content"    -- (only if the cmd is "set_msg"), specifies the new msg to be stored for later sending, mapped to the sender name
            * "get_recent" -- asks for the recent most msgs in the txt file, the server should return them
            * "summary"    -- Present a summary for the data in the server, on the browser.

    """
    # take the msg that corresponds to the name in the json file, revert it to default for future use, and send the msg to msg_history.txt
    # if name is not in the json file, then add it and assign default msg

    # get the cmd 
    cmd = data["cmd"].value
    
    if cmd == "send":
        with open("name_to_msg.json", 'r') as name_to_msg_file:
            name_to_msg = json.load(name_to_msg_file)
            sender_name = data["sender"].value
            # If the sender is in the dict, then use the msg that's mapped there.
            if sender_name in name_to_msg:
                msg_to_send = name_to_msg[sender_name]
            else:
                msg_to_send = DEFAULT_MSG
            # In any case, revert back the msg in the dict to the default now.
            # This also adds the sender if it didn't exist in the dict.s
            name_to_msg[sender_name] = DEFAULT_MSG
        with open("name_to_msg.json", 'w') as name_to_msg_file:
            # Write back to json.
            json.dump(name_to_msg, name_to_msg_file)

        # Now actually send the msg (write to text file)
        with open("msg_history.txt", "a") as hist_file:
            timestamp = datetime.datetime.now()
            msg = sender_name +"@"+ str(timestamp.hour)+":"+str(timestamp.minute) +" " + msg_to_send
            hist_file.write(msg +"\n" )
            # Now clients would be able to grab the last lines of the txt file to get updated messages.
        
        # Indicate success:
        print("Successfully wrote to file: ", msg)

    if  cmd == "set_msg":
        # Map the new msg to the sender name
        sender_name = data["sender"].value
        new_msg_content = data["new_msg_content"].value
        # Get the json dict.
        with open("name_to_msg.json", 'r') as name_to_msg_file:
            name_to_msg = json.load(name_to_msg_file)
        # Set the new msg.
        name_to_msg[sender_name] = new_msg_content
        # Write back to json.
        with open("name_to_msg.json", 'w') as name_to_msg_file:
            # Write back to json.
            json.dump(name_to_msg, name_to_msg_file)
        #Indicate success.
        print("Successfully set new message for cliend:", sender_name, "<br> New msg: ", new_msg_content)

    if cmd == "get_recent":
        # Print the most recent 3 messges. Recent on top.
        with open("msg_history.txt", "r") as hist_file:
            recent_msgs = get_recent_msgs(3)
            for ix in range(len(recent_msgs)):
                print(recent_msgs[ix], "<br>")
 

    if  cmd == "summary":
        # Show a summary of the information currently stored on the server.
        # Show title:
        print("<h1>Summary Page for Server Information</h1>")
        # Show the jsom file.
        with open("name_to_msg.json", 'r') as name_to_msg_file:
            name_to_msg = json.load(name_to_msg_file)
            print("<h2> Name to msg JSON file</h2>")
            print(name_to_msg)
        # Show the history txt file.
        with open("msg_history.txt", "r") as hist_file:
            print("<br><h2>The 10 most recent msgs:</h2><br>")

            recent_msgs = get_recent_msgs(10)
            for ix in range(len(recent_msgs)):
                print("The " , ix , "most recent mssage: ", recent_msgs[ix], "<br>")

    

        
        



        
    
    



if __name__ == "__main__":
    #ask that the info will bi in the form of asdfgefs/dataHandler.py?command=getLast
    #command below takes the arguements from the get request and puts them in some sort of a dictionary
    inDataDict = cgi.FieldStorage()
    # update the msg_history.txt file with the new msg
    receive_msgs_to_hist_and_dict(inDataDict)
