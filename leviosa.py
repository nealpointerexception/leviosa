import argparse 
import subprocess


def conv_to_dict(data, identifier):
    #[class="Mate-terminal" id=48234502 instance="mate-terminal" title="nealc@nealc-Lenovo: ~/pyprojs/volume_control" window_role="mate-terminal-window-29077-2073975251-1557702643"]\
    locator_str = "" # what do you want to id the window by (class or instance)
    # check parameter input
    if identifier == "c":
        locator_str = "class=\""
        
    elif identifier == "i":
        locator_str = "instance=\""
    # find where the string exists in the data
    
    index_a = str(data).find(locator_str)
    index_b = str(data).find("\"", index_a + len(locator_str))  # find where the ending " is using the first index
    return str(data)[index_a + len(locator_str) : index_b] #return final name


if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="perform window actions for i3")
    i3_conf_loc = "~/.config/i3/config" # where config file is located

    # call super cool window property script
    window_data = subprocess.check_output(". ~/scripts/i3-get-window-criteria.sh", shell=True)
    # ask user what they want to id their window by
    window_data = str(window_data)
    print(
        """Select Identifier:
            (c)lass
            (i)nstance

            """
        )

    iden = ""
    while 1:
        iden = input()
        if not (iden == "c" or iden == "i"):
            print("Bad input")
        else:
            break
    # get id string from their selected choice
    identifier_str = conv_to_dict(window_data, iden)
    # assign iden to a full string. This is for the final pipe_string
    if iden == "c": 
        iden = "class" 
    else: 
        iden = "instance"
    # ask user what they would like to do with the window
    print(
        """Select Action:
            (f)loat
            (a)uto move
            """
        )
    action = ""
    while 1:
        action = input()
        if not (action == "f" or action == "a"):
            print("Bad input")
        else:
            break
    # generate a string to pipe to the config file based on their choice
    if action == "f":
        pipe_text = "for_window [{0}=\\\"{1}\\\"] floating enable".format(iden, identifier_str) # break the slashes out so it doesnt interfere with the pipe
        
    elif action == "a":
        ws_index = input("Workspace ID: ") # get id of i3 workspace to move to
        # you need to break out the $ as well
        pipe_text = "for_window [{0}=\\\"{1}\\\"] move to workspace \\$ws{2}".format(iden, identifier_str, ws_index)
        
    # print(pipe_text)
    # pipe out text using a subproc call.
    subprocess.call("echo {0} >> {1}".format(pipe_text, i3_conf_loc), shell=True)
    print("Please refresh i3!")