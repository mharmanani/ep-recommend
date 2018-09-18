# TV Episode Recommendation System
A command line interface for recommending TV episodes based on ratings and keyword matching.

## How it works
The program reads from the *SHOWS* file, which contains structured data about each TV show it uses for its computations. 

The file is structured this way: 
```
<SHOW>
NAME OF THE SHOW
https://imdb.com/title/ttsmtgsmtg/
1 2 3 4 5
</SHOW>
```

After all the necessary data has been included in the *SHOWS* file, the program is ready to be used.

The user is first greeted by a message, a short overview of the different commands, and a command prompt. 

* __quit__: Exit the program.
* __download *show*__: Parses the data in *SHOWS* to create a file with data from each episode of the selected show - episode code, title, rating, and description.
```
S01E01. Pilot (7.9/10)
Description here...
S01E02. Episode 2 (8.7/10)
Description here...
...
```
* __load *show*__: Load a TV show into the program. 
* __top *n*__: List the top n episodes.