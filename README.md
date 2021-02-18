# Python_Pricing

This project concern the python pricing part of the trading strategy analyser project we are building. 

## To SetUp the Project :
### Including GitHub account in PyCharm

- First dowload PyCharm at : https://www.jetbrains.com/fr-fr/pycharm/download/#section=windows (take the community one)
- Launch PyCharm with Anaconda 
- Indicate full path of you Python IDE (please download Python version 3.7 or more if you don't already have it : https://www.python.org/downloads/)
- Then, Ctrl + Alt + S to open settings, got to : Version Control > GitHub : Add account

You can either use token, or either use mail and password. I personnaly recommand using a token. To create one go to your github account settings.  
  - Settings > Developper Settings > Personal Access Token > Generate new token
  - Give you the rights you want
  - Copy and Paste the token in PyCharm
  - Apply
  
Here you have included your GitHub account in PyCharm. Now it's time to clone the project ...

### To Clone the Project

- Simply go to PyCharm, in the top bar menu : VCS > Get from Version Control > Past this URL : https://github.com/tradingstrategyanalyserproject/Python_Pricing/
- Put and empty directory where to clone this project


Start working on it 

##  REQUIREMENTS :
PACKAGES : numpy, scipy, flask
TO RUN : OPEN A COMMAND PROMPT
WRITE "cd (path where the file is)"
"set FLASK_APP=server.py"
"python -m flask run"
SERVER SHOULD BE RUNNING

YOU CAN CHECK THE JSON OUTPUT IN WEB BROWSER AT http://127.0.0.1:5000/price/type/spot/strike/time/rate/vol (replace all values from type to vol with pricing values)
example pricing : http://127.0.0.1:5000/price/call/100.0/100.0/12.0/5.0/30.0
example strike variable : http://127.0.0.1:5000/variable/strike/100.0/150.0/call/100.0/12.0/5.0/30.0
example spot variable : http://127.0.0.1:5000/variable/strike/100.0/150.0/call/100.0/12.0/5.0/30.0
example sigma variable : http://127.0.0.1:5000/variable/sigma/100.0/150.0/call/100.0/100.0/12.0/5.0