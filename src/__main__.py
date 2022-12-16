#!/usr/bin/python
from colors import print_result, print_warning, print_error, print_status
from StackTracesUtilities import StackTracesUtilities
import sys
import os
import csv
import time
# try:
#     __import__('time')
# except ImportError:
#     pip.main(['install', 'time'])
#     __import__('time')

def scenarios(idScenario):
    #setup
    r = StackTracesUtilities()
    params = [('Label','Anomaly'), ('Src_IP','192.168.0.13')]
    
    #scenarios
    if idScenario == "1":
        print("scénario 1")
        r.load_data('./intrusion_dataset.csv')
        r.F(params)
    if idScenario == "2":
        print("scénario 2")
        r.load_data('./intrusion_dataset.csv')
        r.sort_data('Timestamp')
        r.create_work_file()
        r.P_F_by_stacktrace('Timestamp',params)

    #différent scénarios
    if idScenario == 'scenarios':
        print_status('''
        after putting the "intrusion_dataset.csv" in the folder of the app, try one of these :
          1 : load the data from the csv file and searches for a line that match : F( Label=="Anomaly" && src_ip=="192.168.0.13")
          2 : load the data from the csv file, reorganise it in stack traces based on the Timestamp column, \n |     store it and it calculates the percentage of stack traces that matches : F(Label=="Anomaly" && Src_IP=="192.168.0.13)
        ''')

def workspace():
    user_input = ""
    r = StackTracesUtilities()
    print_status("you are now in a workspace, use 'help' to see the available commands")
    while True:
        user_input = input("command :\n").split(' ')
        if user_input[0] in ["quit","q"]: exit(0)

        output_status, output_message = command_handler(user_input, r)
        if output_status == -1 :
            print_error(output_message)
        else:
            print_status(output_message)

def command_handler(user_input, r):
    command = user_input[0]
    args = user_input[1:]
    time_func = False
    start = time.time()
    if user_input[0] == "time":
        command = user_input[1]
        args = user_input[2:]
        time_func = True

    status = -1
    if command == "help":
        print_status('''
        available commands :
        the 'alt' field give an alternative call for the command
        $ quit
            $ alt  : q
            $ desc : quit the workspace and exit the program
        $ load [source]
            $ alt  : l
            $ desc : load data from csv file (must have a header with columns name)
        $ load_workfile [source]
            $ alt  : lwf
            $ desc : load previously created work file 
        $ arrange_by_stacktrace [stacktracesHeaderID]
            $ alt  : ast
            $ desc : sort the loaded data based on the column with header stacktracesHeaderID to recompose stack traces
        $ store_in_workfile
            $ alt  : swf
            $ desc : store the currently loaded data in a workfile (i.e: to avoid sorting the same data twice)
        $ satisfy [params...]
            $ alt  : s
            $ desc : check if a row in the loaded data match all the given parameters
        $ probability_satisfy [params...]
            $ alt  : ps
            $ desc : calculate the probability for a row in the loaded data to match all the given parameters
        $ workflow_s [source] [params...]
            $ alt  : ws
            $ desc : automatic workflow to execute satisfy (load -> satisfy)
        $ satisfy_stacktraces [stacktracesHeaderID] [params...]
            $ alt  : sst
            $ desc : check if at least one stacktrace contains a record that match all the given parameters
        $ probability_satisfy_stacktraces [stacktracesHeaderID] [params...]
            $ alt  : psst
            $ desc : calculate the probability for at least one record in list of stacktraces to match all the given parameters
        $ workflow_p_s_stacktraces [source] [stacktracesHeaderID] [params...]
            $ alt  : wpsst
            $ desc : automatic workflow to get the probability for at least one record in a stacktrace to match all 
                     the given parameters (load -> sort by stacktrace -> satisfy)
        $ probability_satisfy_until_stacktraces [stacktracesHeaderID] [params...] -U [params goal]
            $ alt  : psust
            $ desc : calculate the probability for at least one record in list of stacktraces to match all the given parameters until the second params

        you can add 'time' before any command to get the time it took to execute 
        ''')
        status = 0

    if command in ["load","l"]:
        if len(args) < 1: return -1, "this command need 1 argument : [source]"
        r.load_data(args[0])
        status = 0

    if command in ["load_workfile","lwf"]:
        if len(args) < 1: return -1, "this command need 1 argument : [source]"
        r.load_data(args[0], refresh=False)
        status = 0

    if command in ["arrange_by_stacktraces","ast"]:
        if len(args) < 1: return -1, "this command need 1 argument : [stacktracesHeaderID]"
        r.sort_data(args[0])
        status = 0

    if command in ["store_in_workfile","swf"]:
        r.create_work_file()
        status = 0

    if command in ["satisfy","s"]:
        if len(args) < 1: return -1, "this command need 1 argument : [params...] where params are tuples of the form (Header, ExpectedValue)"
        if len(args[0:]) == 0: return -1, "the list of parameters is empty"
        r.F(eval_params(args[0:]))
        status = 0

    if command in ["probability_satisfy","ps"]:
        if len(args) < 1: return -1, "this command need 1 argument : [params...] where params are tuples of the form (Header, ExpectedValue)"
        if len(args[0:]) == 0: return -1, "the list of parameters is empty"
        r.F(eval_params(args[0:]), probability=True)
        status = 0

    if command in ["workflow_s","ws"]:
        if len(args) < 2: return -1, "this command need 2 arguments : [source] [params...] where params are tuples of the form (Header, ExpectedValue)"
        if not os.path.isfile(args[0]) or args[0].split('.')[-1:][0] != "csv": return -1, "%s is not a valid file" % args[0]
        if len(args[1:]) == 0: return -1, "the list of parameters is empty"
        r.load_data(args[0])
        r.F(eval_params(args[1:]))
        status = 0

    if command in ["satisfy_stacktraces","sst"]:
        if len(args) < 2: return -1, "this command need 2 arguments : [stacktracesHeaderID] [params...] where params are tuples of the form (Header, ExpectedValue)"
        print_warning('if you are stuck in what seems like an infinite loop, use ctrl+c to exit the program. your dataset may not be sorted')
        r.F_by_stacktrace(args[0],eval_params(args[1:]))
        status = 0

    if command in ["probability_satisfy_stacktraces","psst"]:
        if len(args) < 2: return -1, "this command need 2 arguments : [stacktracesHeaderID] [params...] where params are tuples of the form (Header, ExpectedValue)"
        print_warning('if you are stuck in what seems like an infinite loop, use ctrl+c to exit the program. your dataset may not be sorted')
        r.F_by_stacktrace(args[0],eval_params(args[1:]), probability=True)
        status = 0

    if command in ["workflow_p_s_stacktraces","wpsst"]:
        if len(args) < 3: return -1, "this command need 3 arguments : [source] [stacktracesHeaderID] [params...] where params are tuples of the form (Header, ExpectedValue)"
        #if not os.path.isfile(args[0]) or args[0].split('.')[-1:][0] != "csv": return -1, "%s is not a valid file" % args[0]
        r.load_data(args[0])
        r.sort_data(args[1])
        r.F_by_stacktrace(args[1],eval_params(args[2:]))
        status = 0

    if command in ["probability_satisfy__until_stacktraces","psust"]:
        if len(args) < 2: return -1, "this command need 3 arguments : [stacktracesHeaderID] [params...] -U [param goal] where params are tuples of the form (Header, ExpectedValue)"
        print_warning('if you are stuck in what seems like an infinite loop, use ctrl+c to exit the program. your dataset may not be sorted')
        
        params = args[1:]
        param_while = eval_params(params[: params.index("-U")])
        param_until = eval_params(params[: params.index("-U") - 1] + params[params.index("-U")+1:])
        
        r.F_Until_by_stacktrace(args[0],param_while, param_until, probability=True)
        status = 0

    if status == -1:
        return -1, "%s is not a command" % (command)
    if time_func:
        return 0, "%i seconds" % (time.time()-start,)
    
    return 0, ""

def eval_params(params):
    return [eval(tupl) for tupl in params]

if __name__ == "__main__":    
    if sys.argv[1:][0] == "scenario":
        if len(sys.argv[1:]) > 1:
            scenarios(sys.argv[1:][1])
        else:
            print('you have to specify a scenario. try :\n py Request.py scenario [1-2]')
    if sys.argv[1:][0] == "scenarios":
        scenarios("scenarios")
    if sys.argv[1:][0] == "workspace":
        workspace()

    if len(sys.argv) == 1:
        print_status('''
        this program need arguments, use of the following arguments lists :
            $ scenarios
            $ scenario [1-2]
            $ workspace
        ''')