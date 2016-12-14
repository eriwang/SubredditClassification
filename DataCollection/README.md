# Data Collection

## Collect Data
This script downloads all self posts in the included subreddits. Subreddits can be chosen by modifying the global python list inside the file.
``` Python
SUBREDDITS = ['history','uofm','engineering','cscareerquestions','puns']
```
Can be run using
``` Bash
python collectData.py
```

## Annotate Data
This script is used for turning user-create or algorithm-created summaries into XML. It requires a name of the user or algorithm to be passed as a commandline argument. 
``` Bash
python annotateData.py <Name>
```
The summary must then be given as standard input. 
``` Bash
cat <summary.txt> | python annotateData.py <Name>
```

## Expectations
The following Python library must be installed
``` Bash
PRAW
```
