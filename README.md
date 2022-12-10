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
$ load [source]
    $ alt  : l
    $ desc : load data from csv file (must have a header with columns name)
$ load_workfile [source]
    $ alt  : lwf
    $ desc : load previously created work file 
$ sort_by_stacktrace [stacktracesHeaderID]
    $ alt  : sst
    $ desc : sort the loaded data based on the column with header stacktracesHeaderID to recompose stack traces
$ store_in_workfile
    $ alt  : swf
    $ desc : store the currently loaded data in a workfile (i.e: to avoid sorting the same data twice)
$ satisfy [params...]
    $ alt  : s
    $ desc : check if a row in the loaded data match all the given parameters
$ workflow_s [source] [params...]
    $ alt  : ws
    $ desc : automatic workflow to execute satisfy (load -> satisfy)
$ probability_satisfy [stacktracesHeaderID] [params...]
    $ alt  : ps
    $ desc : get the probability for at least one record in a stacktrace to match all the given parameters
$ workflow_p_s [source] [stacktracesHeaderID] [params...]
    $ alt  : wps
    $ desc : automatic workflow to get the probability for at least one record in a stacktrace to match all
             the given parameters (load -> sort by stacktrace -> satisfy)
```

