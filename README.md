# StackTracesAnalysisUtilities (stau)
basic stack traces analysis tool allowing you to search stack traces through queries

# Use stau

stau is bundled as a .pyz file, you only have to download stau.pyz to use the program.

You can run it with python by placing yourself in the folder it's located like this : 
``` 
py ./stau.pyz [arguments] 
```


# Available arguments

## scenarios
Use this argument to get the list of premade scenarios (all of them use the intrusion_dataset.csv file so include it in your folder)

Exemple
```
py ./stau.pyz scenarios
```

## scenario [1-2]
Use this argument to run one of the premade scenarios (all of them use the intrusion_dataset.csv file so include it in your folder)

Exemple
```
py ./stau.pyz scenario 1
```

## workspace
Places you inside a workspace where you will be able to load, manipulate and query stack traces stored in csv files 

Exemple
```
py ./stau.pyz workspace
```


Available commands inside the workspace
```
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
```


## To execute the requests from the TP follow those commands in the workspace

```
l intrusion.csv
```
```
s ('Src_IP','192.168.0.13') ('Label','Anomaly')
```
```
ps ('Src_IP','192.168.0.13') ('Label','Anomaly')
```
```
ast Timestamp
```
```
psst ('Src_IP','192.168.0.13') ('Label','Anomaly')
```
```
psust ('Src_IP','192.168.0.13') ('Label','Normal') -U ('Label','Anomaly')
```


