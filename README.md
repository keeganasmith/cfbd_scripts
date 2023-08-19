# cfbd_scripts
helper scripts for cfbd

## Installation

Clone the repo:  
```
git clone https://github.com/keeganasmith/cfbd_scripts.git
```
  
Navigate to directory. Create a .env file and put in your cfbd api credentials.  
Your file should look like this:  
```
API_TOKEN = "&lt;your token here&gt;"
```
To install the dependencies, do:
```
pip install -r requirements.txt
```
## Usage  

To run the program which checks for duplicates simply type:  

```
python3 find_dups.py  
```
or 
```
python find_dups.py
```
This will activate the CLI and will prompt you for various parameters.  
For the endpoint, enter the path after the '/', so for example the /roster endpoint is just `roster` and the /games/media endpoint is just `games/media`.  
For the parameters, just enter the parameters in json format. So for example if we only want data from 2023, you would enter: `{"year":2023}`.  
Next you will be prompted to either  
1. choose fields to include  
2. choose fields to exclude  
3. use all fields  
If you pick 1., it will return all of the records which have the same fields for the fields you specified.  
For example, if we are in the rosters endpoint maybe I want to find all of the records where the players have the same first and last names. In this case I would choose option 1 and enter `first_name`, `last_name` as fields to include.  
If you pick 2., it will return all of the records which have the same fields ignoring the fields you specify.  
For example if I wanted to see the records which have all of the same field values aside from `id` I would pick option 2 and enter `id` as a field to exclude.  
If I simply want to see all of the records which are exactly the same I would pick option 3.
The result is a list of lists containing record ids. Each list contains the ids of records that matched one another.  
An empty list indicates that no duplicates were found.  
