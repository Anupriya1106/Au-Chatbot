import requests
import json
from datetime import datetime
from decimal import Decimal
from bank_statement import get_bank_statement


def fetch_account_statement(email, input_mail, cursor):
 transaction1 = []
            
account_no = bank_statement.get_bank_statement(email) 
            #print(account_number)
            #print("account statement call made")
data = {
            "messages": [
            {
            "content": '''
                You are designed to get data from emails received from user for a bank. 
                I want specific keywords from the message as described below. Just answer in the format described below, nothing else.
    
                if user asking to fetch account statement, then give start date and end date from the message  exactly in below format: just give string given below
                            {"accountStatemtent":{"startDate": "yyyy-mm-dd","endDate": "yyyy-mm-dd"}}
                if any of the date is not available return null in respective date, and for present date return 'present' in date.
    
                if user is asking regarding its account balance details, give output in the format below:
                            {"accountBalance":{}}
    
    
                if user is asking its account details regarding account information, example  account number, registered name, IFSC code etc., give information in below format: 
                            {"account_information":{'whatever is asking' : {}}}
    
                If user is asking for anything else other than the categories above. give response in below format:
                            {"unavailable":{}}
                Do not overthink or assume the information behind the message other than what is directly described in the message. Do not justify yourself. I am using your output in my code.
                Do not assume any other category. If the message strictly belongs to above categories, then only categorize that. If you are not sure. Please categorize as unavailable and do not provide any other explanation when message comes under unavailable category.
            ''',
            "role": "system"
            },
            {
            "content": input_mail,
            "role": "user"
            }
            ]
            }

response = requests.post(API_URL, json=data)
