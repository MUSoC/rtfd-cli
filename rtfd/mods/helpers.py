from colorama import Style

#Colorize the output statement if colored is true
def formatstr(string, color, colored):
    if colored:    
        print(color + string + Style.RESET_ALL)
    else:
        print(string) 
