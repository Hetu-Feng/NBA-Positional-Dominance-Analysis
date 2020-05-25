### How to run the code

This project requires the following packages:

pandas, numpy, requests, BeautifulSoup and Comment from bs4, csv, and matplotlib

You should be good if you are in the conda base environment, but always make sure above packages are installed.

You can clone the repo at https://github.com/Hetu-Feng/inf510_project

### IMPORTANT

One of the dataset used in this project called 'ori_position_2.csv' is downloaded directly from the web. Either to run the code either in the notebook or to run the .py files from command line, you have to put the 'ori_position_2.csv' file in the same directory for the code to work properly. Otherwise, it will throw an error!

'ori_position_2.csv' is in the /data folder as submission guideline required, but please make sure you put this file to where the notebook and .py file is when you are ready to test

#### To Run the notebook

just simply run the notebook.

#### To Run the .py files

In the command line, switch to the directory where the .py files reside. Type 'python3 main.py -source=remote' in the cmd so the code will grab the data from API and websites, store the raw data to the disk, get dat from the disk do modeling, and print the final visualization result. The whole process should take 1 minute depending on your network connection.

Once you have done '-source=remote', you can now try type 'python3 main.py -source=local', for which the code won’t run the web scraper, but will grab the raw data that are already stored to the disk in the previous run and do the modeling and output conclusions as well.

### Outputs you should expect

You will see 7 csv files all with 'ori_' in the namings, including 'ori_position_2.csv' mentioned previously. These are the raw data that our program scraped from API and online. You will also see another 4 csv files all with 'position_' in the namings. They are modeled datasets that are ready for visualization. You will finally see a 'Visualization.png' file which is the visualization of this project.

### major “gotchas”

As what is stated in Question 7 below, in order to solve the “name conversion” problem, we combined the API data set and the downloaded static dataset and create a new one. we could probably improve my code here by creating two separate versions of datasets where one contains all players’ position information with “normal” names and the other one contains all players’ position information with names written in special characters. That would give a clearer view when merging with other data sources.

### What did we set out to study:

We set out to study the change of positional dominance of NBA players in the past 20 years. People are always talking about in recent several years that the ‘Bigs’ are fading and it’s the guards’ league. We want to investigate into this subject and find out if what people saying are true and if it is true, when does it start to happen. We divided player based on the position on court into guards, forwards and center. We look at the change of field goal attempted per game, usage percentage per game, salary and draft expected value based on 3 positions over the year. We wanted to find the trend through the graph we created in the last step.

MINOR CHANGE TO MILESTONE 1: We originally put guards and forwards in 1 category and centers in another. As the project progressing, we decided to put forwards into its own category to make it more intuitive and reasonable.

### conclusions:

The original assumption is partially confirmed as the result shows that it is the guards that are dominating the league in recent years and centers faded. However, since 1998, centers were already not as dominant as guards and forwards, and their dominance was dropping during the year 2000 to 2008 period. Centers are making a small comeback after year 2008 and 2009, but they are still down. An interesting finding is that forwards were at the level with guards before around year 2008 but started to go down after that time and on the same dominance level as centers till today.

### difficulties

We were struggling at getting enough player’s position data from the API. When we were testing the API at milestone 1, we thought it was working fine as it returned players name with their position, but when we started to retrieve the 20 years players information, there are a lot of players with empty values in the position column. We had to scrape data from other places to make up the missing values.

Another difficulty is that some player names contain special characters such as “Toni Kukoč”, which is written as “Toni Kukoc” in the salary data source. Therefore, we have a hard time mapping these player names. Solution to the problem is that the player position dataset we downloaded from Basketball-Reference has player names contain special characters which helps to merge with three other datasets: FGA, USG, and draft; while the API data contains “normal” versions of player names that easily map the salary dataset. In this case, after combining the API data set and the downloaded static data set, and creating a new data set, when we merge it with other datasets using Pandas data frames, it automatically maps the version of names that the other data sources share.

### What would we do “next” to expand or augment the project:

We can add more relevant metrics to the analysis to further concrete the conclusion. We should devise an appropriate weighting method to put all the metrics together in one graph to get a conclusive trend. We can also extend the years of selection to 50 years and see the change in this long period. Since we’ve had the conclusion in this project, we can further dive into it and see what the reason is that caused this dominance change.

