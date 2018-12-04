# The-Truth-About-Twitter
Computer Science final year project
Web application that users can input a Twitter handle into.
Data about the account linked to that handle is retrieved from the Twitter API.
This data is passed into a machine-learning model which makes a decision on 
whether the account is real or a type of spam bot.
Results are then shown on screen for the user to see.

Datasets are too large to upload and as such can be found at their source:
https://botometer.iuni.iu.edu/bot-repository/datasets.html

### Unique Files
![Alt text](documents/unique.PNG?raw=true "Unique Work")

twitter_credentials.py    - Save applications twitter credentials to file for use later on  
twitter_credentials.json  - Applications twitter credentials in json format for use later on  
web_style.css             - CSS stylesheet for index.html  
read_store.py             - Read in datasets from csv files, do data conversions and store in database  
machine_learning.py       - Read out records from database and use in a machine-learning model outputting mean accuracy score to console  

              
### Altered Files from Django Framework
![Alt text](documents/altered.PNG?raw=true "Altered Work")

settings.py - Altered to change database to PostgreSQL instance, allow css sytlesheet to be used in index.html and template files to be located.  
index.html  - Altered for layout of web-front end, added form, css sytlesheet and returned tweets section.  
forms.py    - Altered to add basic form to take user input.  
models.py   - Altered to add tables to database.  
urls.py     - Altered to allow CSS sytlesheet to be used in index.html.  
views.py    - Altered to create form or take in user input from form, connect to twitter, return tweets and pass variables to index.html.  
