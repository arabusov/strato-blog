#!/usr/bin/python3
from typing import List, Tuple
import sys

Text = List[str]
PsTeXRes = Tuple [str, str, str]
State = int

from symbols import symbols
punct=[',', '.', ':', ';']

def reserved_word (command_tuple, par_state):
    res = ""
    command = command_tuple [0]
    tail = ""
    if len (command) > 1 and command[-1] in punct:
        tail=command[-1]
        command=command[:-1]
    argument = command_tuple [1]
    if command == "\\title":
        if par_state == 1:
            res = "</p>\n"
        res = res + "<h2>"+argument+"</h2>\n<p>\n"
        par_state = 1
    elif command == "\\section":
        if par_state == 1:
            res = "</p>\n"
        res = res + "<h3>"+argument+"</h3>\n<p>\n"
        par_state = 1
    elif command == "\\subsection":
        if par_state == 1:
            res = "</p>\n"
        res = res + "<h4>"+argument+"</h4>\n<p>\n"
        par_state = 1
    elif command == "\\it":
        res = "<i>"+argument+"</i>"
    elif command == "\\par" and (par_state == 0):
        res = "\n<p>\n"
        par_state = 1
    elif command == "\\par" and (par_state == 1):
        res = "</p>\n<p>\n"
    elif command in symbols.keys():
        res = symbols[command]
    else:
        res = command
    res = res + tail+" " +  command_tuple [2]
    return (res, par_state)

def substit (line ):
    res = line
    res=res.replace ("``", "\"")
    res=res.replace ("<<", "\u00ab")
    res=res.replace (">>", "\u00bb")
    res=res.replace ("---", "\u2014")
    res=res.replace ("--", "\u2013")
    return res

def main_loop (text: Text):
    text_line = "".join (text)
    no_doubl_lin_br = text_line.replace ("\n\n", " \\par ")
    words = no_doubl_lin_br.split ()
    iterator = 0
    result = []
    while iterator < len (words):
        current_word = words [iterator]
        argument = ""
        command = ""
        rest = ""
        if ("{" in current_word) and ("}" in current_word):
            split_res1 = current_word.split("{")
            command = split_res1[0]
            split_res2 = split_res1[1].split("}")
            argument = split_res2[0]
            rest = split_res2[1]
            res = (command, argument, rest)
            result.append (res)
            iterator = iterator + 1
            continue
        if "{" in current_word:
            split_res1 = current_word.split ("{")
            command = split_res1[0]
            argument = split_res1[1]
            iterator = iterator + 1
            current_word = words [iterator]
            while (iterator < len (words)) and not ("}" in current_word):
                argument = argument + " " + current_word
                iterator = iterator + 1
                current_word = words[iterator]
            split_res2 = current_word.split ("}")
            argument = argument + " " + split_res2[0]
            rest = split_res2[1]
            iterator = iterator + 1
            res = (command, argument, rest)
            result.append (res)
            continue
        if "}" in current_word:
            print ("error")
            sys.exit (1)
        iterator = iterator + 1
        if current_word[0] == "\\":
            res = (current_word, "", "")
        else:
            res = ("", "", current_word)
        result.append (res)
    par_state = 0;
    res_line = ""
    line_len = 0
    for res in result:
        par_tuple=reserved_word (res, par_state)
        subst_res = substit(par_tuple[0])
        if res[0]=="":
            res_line = res_line  +  subst_res
            line_len = line_len + len (subst_res)
            if line_len > 60:
                res_line = res_line + "\n"
                line_len = 0
        else:
            res_line = res_line + "\n" + subst_res
        par_state=par_tuple[1]
    print (res_line)
    if par_state == 1:
        print ("</p>")
if __name__ == "__main__":
    of = open (sys.argv[1])
    text = []
    for line in of:
        text.append (line)
    main_loop (text)
