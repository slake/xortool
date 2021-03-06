#!/usr/bin/env python
#-*- coding:utf-8 -*-

import getopt

from routine import *

PARAMETERS = {
    "input_is_hex": 0,
    "max_key_length": 32,
    "known_key_length": None,
    "most_frequent_char": None,
    "frequency_spread": 0,
    "filename": "-",  # stdin by default
}

def show_usage_and_exit():
    print "xortool.py"
    print "  A tool to do some xor analysis:"
    print "  - guess the key length (based on count of equal chars)"
    print "  - guess the key (base on knowledge of most probable char)"
    print "Usage:"
    print " ", os.path.basename(sys.argv[0]),"[-h|--help] [OPTIONS] [<filename>]"
    print "Options:"
    print " ", "-l,--key-length     length of the key"
    print " ", "-c,--char           most possible char"
    print " ", "-x,--hex            input is hex-encoded str"
    #print " ", "-s,--spread         spread of possible key bytes"
    print " ", "-m,--max-keylen     maximum key length to probe"
    sys.exit(1)
    return


def parse_parameters():
    """
    Parse arguments and update PARAMETERS if needed
    """
    options, arguments = get_options_and_arguments(sys.argv[1:])
    update_parameters(options, arguments)
    return PARAMETERS


def get_options_and_arguments(program_arguments):
    options, arguments = [], []
    try:
        options, arguments = getopt.getopt(program_arguments, "l:c:s:m:x",
                ["key-length=", "char=", "spread=", "max-keylen=",
                                          "hex", "help", "usage"])
        if len(arguments) > 1:  # trick to parse options after filename
            options += get_options_and_arguments(program_arguments[1:])[0]
            arguments = arguments[:1]
        #TODO: add param "brute all possible freq. chars"
        
    except getopt.GetoptError:
        show_usage_and_exit()
    return options, arguments


def update_parameters(options, arguments):
    global PARAMETERS
    for option, value in options:
        if option in ("-x", "--hex"):
            PARAMETERS["input_is_hex"] = 1
        elif option in ("-c", "--char"):
            PARAMETERS["most_frequent_char"] = parse_char(value)
        elif option in ("-l", "--key-length"):
            PARAMETERS["known_key_length"] = int(value)
        elif option in ("-s", "--spread"):
            PARAMETERS["frequency_spread"] = int(value)
        elif option in ("-m", "--max-keylen"):
            PARAMETERS["max_key_length"] = int(value)
        elif option in ("-h", "--help", "--usage"):
            show_usage_and_exit()
            
    if len(arguments) == 1:
        PARAMETERS["filename"] = arguments[0]

    return
