# Rouge-2 Evaluation
This script is used to calculate the Rouge-2 evaluation score of summaries. It compares all summaries for subreddits in the subreddit list from algorithms in the algorithm list to those made by users in the user list. These parameters can be specified by altering the python list in the file. 
``` Python
SUBREDDITS = ['history','uofm','engineering','cscareerquestions','puns']
USERS = ['kaushik', 'brian', 'eric', 'daniel', 'moderator']
ALGOS = ['pagerank', 'tf-idf']
```

## Expectations
From each user or algorithm the script expects there to be a file
``` Bash
user.annotations.xml
```
Or
``` Bash
algorithm.annotations.xml
``` 
Respectively. Each of these annotation files must also include a xml tree corresponding to each subreddit in the above list. 

The following Python library must be installed 
``` Bash
PrettyTable
Numpy
```
