#!/usr/bin/env python3
import datetime
class Color:
    RESET='\033[0m'
    BOLD='\033[01m'
    UNDERLINE='\033[04m'
    STRIKETHROUGH='\033[09m'
    class Foreground:
        BLACK='\033[30m'
        RED='\033[31m'
        GREEN='\033[32m'
        ORANGE='\033[33m'
        BLUE='\033[34m'
        PURPLE='\033[35m'
        CYAN='\033[36m'
        LIGHTGREY='\033[37m'
        DARKGREY='\033[90m'
        LIGHTRED='\033[91m'
        LIGHTGREEN='\033[92m'
        YELLOW='\033[93m'
        LIGHTBLUE='\033[94m'
        PING='\033[95m'
        LIGHTCYAN='\033[96m'
    class Background:
        BLACK='\033[40m'
        RED='\033[41m'
        GREEN='\033[42m'
        ORANGE='\033[43m'
        BLUE='\033[44m'
        PURPLE='\033[45m'
        CYAN='\033[46m'
        LIGHTGREY='\033[47m'


class Logger:
    def __init__(self, level=0):
        self.level = level
    DEBUG=0
    LOG=1
    WARNING=2
    ERROR=3
    def get_time(self):
        return datetime.datetime.now()
    def get_formatted_time(self):
        return self.get_time().strftime(Color.Background.BLUE + "[%H:%M:%S]" + Color.RESET + " ")

    def get_level(self):
        return self.level
    def set_level(self, level):
        self.level = level
    # TODO: Implement GUI
    def debug(self, msg, gui=False):
        if self.level <= self.DEBUG:
            if gui:
                pass
            else:
                print(self.get_formatted_time() + Color.Foreground.LIGHTGREY + "Debug: " + str(msg) + Color.RESET)
    def log(self, msg, gui=False):
        if self.level <= self.LOG:
            if gui:
                pass
            else:
                print(self.get_formatted_time() + Color.Foreground.LIGHTBLUE + Color.BOLD + "Info: " + Color.RESET + Color.Foreground.LIGHTBLUE + str(msg) + Color.RESET)
    def warn(self, warn, gui=False):
        if self.level <= self.WARNING:
            if gui:
                pass
            else:
                print(self.get_formatted_time() + Color.Foreground.YELLOW + Color.BOLD + "Warning: " + Color.RESET + Color.Foreground.YELLOW + str(warn) + Color.RESET)
    def error(self, err, gui=True):
        if self.level <= self.ERROR:
            if gui:
                pass
            else:
                print(self.get_formatted_time() + Color.Foreground.RED + Color.BOLD + "An Error has occurred: " + Color.RESET + Color.Foreground.RED + str(err) + Color.RESET)
