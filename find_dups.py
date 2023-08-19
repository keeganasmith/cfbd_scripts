import os
import requests
from dotenv import load_dotenv
import copy
import json
load_dotenv()

cfbd_api_key = os.environ.get("API_TOKEN")

cfbd_url = "http://api.collegefootballdata.com/"
header = {"Authorization": f"Bearer {cfbd_api_key}"}
def req_data(endpoint: str, params: dict = None):
    result = requests.get(cfbd_url + endpoint, headers = header, params=params).json()
    return result
def convert_list_to_tuple(my_list):
    i = 0;
    while(i < len(my_list)):
        if(isinstance(my_list[i], list) or isinstance(my_list[i], tuple)):
            my_list[i] = convert_list_to_tuple(my_list[i])
        
        i += 1
    return tuple(my_list)
def convert_dictionary_to_tuple(my_dict):
    result = []
    for item in my_dict:
        if(isinstance(my_dict[item], list) or isinstance(my_dict[item], tuple)):
            result.append((item, convert_list_to_tuple(my_dict[item])))
        elif(isinstance(my_dict[item], dict)):
            result.append((item, convert_dictionary_to_tuple(my_dict[item])))
        else:
            result.append((item, my_dict[item]))
    return tuple(result)
        

def get_likely_duplicates(endpoint: str, params: dict = None, fields_to_exclude: list = None, fields_to_include: list = None): #excludes id parameter, add more to the list to exclude others. 
    data = req_data(endpoint = endpoint, params=params)
    current_dict_id_mapping = {}
    result = []
    for joe in data:
        other_joe = copy.deepcopy(joe)
        if(fields_to_exclude):
            for item in fields_to_exclude:
                del other_joe[item]
        elif(fields_to_include):
            other_joe = {}
            for item in fields_to_include:
                other_joe[item] = joe[item]
        tuple_joe = convert_dictionary_to_tuple(other_joe)
        
        if tuple_joe in current_dict_id_mapping:
            current_dict_id_mapping[tuple_joe].append(joe["id"])
        else:
            current_dict_id_mapping[tuple_joe] = [joe["id"]]
    for bob in current_dict_id_mapping:
        if(len(current_dict_id_mapping[bob]) > 1):
            result.append(current_dict_id_mapping[bob])
    return result;



#result = get_likely_duplicates("roster", {"year":2023}, fields_to_include=["first_name", "last_name"])
#result = get_records_with_matching_ids("roster", {"year":2023})

def main():
    while(True):
        endpoint = input("Howdy, please enter the cfbd endpoint you would like to check for duplicates or q to quit: ")
        if(endpoint == 'q'):
            break
        text_params = input("Please enter the params you would like in json format: ")
        params = json.loads(text_params)
        
        user_choice = input("Choose one of these options:\n(1) Enter fields to include, ignoring all other fields\n(2) Enter fields to exclude\n(3) Use all fields\n(4) quit\nenter here: ")
        list_of_fields = []
        include = False
        result = []
        if(user_choice == '1'):
            include = True
        if(user_choice == '1' or user_choice == '2'):
            while(True):
                field = input("Enter field or q to quit: ")
                if(field == 'q'):
                    break;
                list_of_fields.append(field)
                
            if(include):
                result = get_likely_duplicates(endpoint=endpoint, params=params, fields_to_include=list_of_fields)
            else:
                result = get_likely_duplicates(endpoint=endpoint, params=params, fields_to_exclude=list_of_fields)
        elif(user_choice == '3'):
            result = get_likely_duplicates(endpoint=endpoint, params=params)
        else:
            break;
        print(f"duplicate IDs:\n{str(result)}")

if __name__ == '__main__':
    main()


            
