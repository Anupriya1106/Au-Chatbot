import requests
import json
from datetime import datetime, date 
from decimal import Decimal
import mysql.connector

try:
    #Establish connection to the MySQL server
    connection = mysql.connector.connect(
        host="localhost",
        user="anupriya",
        password="Password$12",
        database="goat"
    )
    #Create a cursor object to execute SQL queries
    cursor = connection.cursor()

    def get_bank_statement(email):
        #print("getting the account number of the user")
            #Retrieve the account number based on the email ID
        query = "SELECT account_no FROM AccountInfo WHERE email_id = %s"
        query1 = "SELECT * FROM AccountInfo WHERE email_id = %s"
        # print(query)
        cursor.execute(query, (email,))
        account_no = cursor.fetchone()[0]

        cursor.execute(query1, (email,))
        data = cursor.fetchone()[0]
        return account_no
            
    email = "emily.brown@gmail.com"
    get_bank_statement(email)

    API_URL = 'http://ec2-13-201-130-252.ap-south-1.compute.amazonaws.com:8080/v1chat/prompt'
    # input_mail = input("")
    input_mail = '''
   As a senior citizen it is difficult to visit a branch or make a video call , please suggest other options to update maturity instructions. If you can send a form by email i can resend back with a sign on it by email if you consider it.
Thanks!
Customer name
    '''
    print("\n=====================input mail========================\n", input_mail)
    data = {
    "messages": [
        {
        "content": '''
        You are designed to answer queries received from bank users. Please classify the question asked into intent described below. Give answer in one word. I need intent only in one word, I am using your output to use a switch case: 
        classify the mail into below 4 categories. Do not provide any extra explanation.
        CurrentAccountStatement = if customer is asking about it's 
        AccountStatement = balance statement for account
        loanStatement = the loan due amount.
        genQuery = If user is asking general questions related to banking, not specific about user account or user specific services. 
        If user is asking for any specific service consider it as a general query.
        Complaints = Categorize mails related to complaints in this category.
        If more than one query is asked give answer in a list.
        Do not overthink or assume the intent behind the message other than what is directly described in the message. Do not justify yourself. I am using your output in my code, just give one word answer.
        Do not assume any other category. If the message strictly belongs to above categories, then only categorize that. If you are not sure. Please categorize as NotAvailable and do not provide any other explanation when message comes under NotAvailable category.
        Do not assume fund transfer as loan payment, it can be any other type of fund transfer, just give output as "NotAvailable"  only, no other explanation.
        ''',
        "role": "system"
        },
        {
        "content": input_mail,
        "role": "user"
        }
    ]
    }
    # Make a POST request to the API endpoint with the data
    response = requests.post(API_URL, json=data)
    # Check the response from the API
    if response.status_code == 200:
        # API call successful
        api_response = response.json()
        #print('API Response:', api_response)

        content = api_response['choices'][0]['message']['content']
        #print('Content:', content)
        print("=========>>>>>",content)

        def email_generation(context):
            # account = account_statement()
            prompt = '''
                    You are an AI system named AUMitra designed to analyse incoming customer emails for AU Small Finance Bank and generate concise, genuine responses. Your goal is to understand the customer's query or concern and provide a helpful and appropriate response. Your responses should be clear, courteous, and to the point.
                    please consider all the points described below and generate polite, short and crisp email using the below points:
                        Analyse the Email.
                        Understand Customer Intent.
                        Address Specific Points.
                        Use Empathetic Language.
                        Provide Genuine Assistance.
                        Conclude Professionally.
                         
                    consider all types of messages to be a mail.
                '''
            prompt += f"\nUse context information provided below.\n {context}"
            data = {
            "messages": [
            {
                "content": prompt,
                "role": "system"
                },
                {
                "content": input_mail,
                "role": "user"
                }
            ]
            }
            # Make a POST request to the API endpoint with the data
            response = requests.post(API_URL, json=data)
            # Check the response from the API
            if response.status_code == 200:
            # API call successful
                api_response = response.json()
                #print('API Response:', api_response)
                generated_mail = api_response['choices'][0]['message']['content']
                print('\n ======================generated mail response====================\n', generated_mail)
                return generated_mail
            else:
            # API call failed
                print('API Error:', response.status_code, response.text) 
                return ""       
        def account_statement():
            transaction1 = []
            
            account_no = get_bank_statement(email) 
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
            # Make a POST request to the API endpoint with the data
            response = requests.post(API_URL, json=data)
            # Check the response from the API
            if response.status_code == 200:
            # API call successful
                api_response = response.json()
                #print('API Response:', api_response)
                content = api_response['choices'][0]['message']['content']
                
                data_dict = json.loads(content)
                # Extract the key
                key = list(data_dict.keys())[0]
                #print(key)
                #print("the information of the customer account")    
                if key == 'accountBalance':
                    query = f"select running_balance from AccountStatement WHERE account_no = {account_no}"
                    cursor.execute(query)
                    account_balance = cursor.fetchone()
                    account_balance = float(account_balance[0])
                    # print("the running account balance is:",account_balance)
                    return account_balance, f"your account balance is {account_balance}"
                    
                elif key == 'accountStatement':
                   
                    contentJson = json.loads(content)["accountStatement"]
                    endDate  = contentJson["endDate"]
                    if endDate == 'present':
                        endDate = datetime.now().date()
                    if endDate == 'present':
                        endDate = datetime.now().date()
                    
                    query = f"select * from AccountStatement WHERE account_no = {account_no}"
                    cursor.execute(query)
                    bank_statement = cursor.fetchone()
                    #print(bank_statement)
                    if bank_statement:
                    # Assuming the order of columns in the table matches the order of attributes you mentioned
                        attributes = [
                            "transaction_id",
                            "account_number",
                            "description",
                            "transaction_type",
                            "transaction_amount",
                            "running_balance",
                            "total_credits",
                            "total_debits",
                            "closing_balance",
                            "start_date",
                            "end_date"
                        ]
            
                    bank_statement1 = "Bank Statement from {} to {}:".format(contentJson["startDate"], endDate)
                    #print(bank_statement1)

                    for attribute, value in zip(attributes, bank_statement):
                        if isinstance(value, Decimal):
                            value = float(value)
                        elif type(value) is date:
                            value = value.strftime('%Y-%m-%d')
                        transaction1.append({attribute:value})
                    transactionn = ", ".join(str(item) for item in transaction1)
                
                    return transactionn, f"your transaction details are below \n {transactionn}"
           
            else:
               # API call failed
                print('API Error:', response.status_code, response.text) 
                return ""          
        
        def loan_statement():
           print("loan statement call made")
        account_no = get_bank_statement(email) 
        data = {
              "messages": [
             {
                  "content": '''
                 You are designed to get data from emails received from user for a bank. I want specific keywords from the message as described below. Just answer in the format described below, nothing else. 
                 "LoanBalanceInquiry" = {}  if user is inquiring about their past payments of loans, including the dates and amounts paid.
                 "PaymentHistory" = {}  if user is inquiring about their past payments, including the dates and amounts paid.
                 "InterestRateInquiry" = {} if user wants to know the interest rate associated with their loan.
                 Do not overthink or assume the information behind the message other than what is directly described in the message.Do not justify or explain yourself. I am using your output in my code.Do not assume any other category . if the message is belongs to the above category described than only described them. Answer in the prescribed format only.
                 ''',
                  "role": "system"
                  },
                  {
                  "content": input_mail,
                  "role": "user"
                  }
              ]
              }
              # Make a POST request to the API endpoint with the data
        response = requests.post(API_URL, json=data)
              # Check the response from the API
        if response.status_code == 200:
             # # API call successful
                  api_response = response.json()
                  print('API Response:', api_response)
                  
                  if 'choices' in api_response:
                      content = api_response['choices'][0]['message']['content']
                  # print('Content:', content)
                      try:
                         data_dict = json.loads(content)
                         key = list(data_dict.keys())[0]
                 
                         if key == 'LoanBalanceInquiry':
                             query = f"Select loan_id, inquiry_date, payment_date, payment_amount from loan where account_no = {account_no}"
                             cursor.execute(query)
                             loan_balance = cursor.fetchone()
                             cursor.close()
                             if loan_balance:
                               loan_balance = float(loan_balance[3])
                               print(f"Your loan balance is {loan_balance}")
                             else:
                                print("No loan balance found for the provided account number.")
                            
                         elif key == 'PaymentHistory':
                              query = f"SELECT loan_id, payment_date, payment_amount FROM Loan WHERE account_no = %s ORDER BY payment_date"
                              cursor.execute(query, (account_no,))
                              payment_records = cursor.fetchall()
                              cursor.close()
                              if payment_records:
                                 print("Payment History:")
                                 for record in payment_records:
                                   loan_id, payment_date, payment_amount = record
                                   print(f"Loan ID: {loan_id}, Payment Date: {payment_date}, Payment Amount: {payment_amount}")
                              else:
                                  print("No payment history found for the provided account number.")

                         elif key == 'LoanPayoffQuote': 
                           contentJson = json.loads(content)
                           loanPayoffQuote = contentJson.get("account_no", None)
                           if account_no is not None:
                              query = f"Select account_no, quote_date from Loan where account_no = {account_no}"
                              cursor.execute(query)
                              result = cursor.fetchone()

                           if result:
                              account_no_result, quote_date = result
                              print("Account Number: ", account_no_result)
                              print("Quote Date: ", quote_date)
                           else:
                            print("No records found for the provided account")
               
                         elif key == 'Complaints':
                              contentJson = json.loads(content)
                              account_no = contentJson.get("account_no", None)
                              if account_no is not None:
                                 query = f"select account_no, complaint_date, complaint_description from Loan where account_no = {account_no}"
                                 cursor.execute(query)
                                 result = cursor.fetchall()

                                 if result:
                                  for row in result:
                                   account_no_result, complaint_date, complaint_description = row
                                   print("Account Number: ", account_no_result)
                                   print("Complaint Date: ", complaint_date)
                                   print("Complaint Description: ", complaint_description)
                         else:
                             print("No Complaints found for the provided account")
                      except json.JSONDecodeError:
                            print("Error decoding JSON response")
            
    else:
            # API call failed
                 print('API Error:', response.status_code, response.text)
        
    def credit_statement():
            print("credit statemet call made")
            data = {
            "messages": [
            {
            "content": '''
                You are designed to get data from emails received from user for a bank. 
                I want specific keywords from the message as described below. Just answer in the format described below, nothing else.

                if user wants to know the current outstanding balance on their loan. give information in the format below:
                            "Loan Balance Inquiry" = {}

                if user is inquiring about their past payments, including the dates and amounts paid. give information in the format below:
                            "Payment History" = {}

                if user wants to know the interest rate associated with their loan. give information in the format below:
                            "Interest Rate Inquiry" = {}

                if user is requesting a payoff quote to determine the total amount needed to pay off their loan in full. give information in the format below:
                            "Loan Payoff Quote" = {}

                If user is asking for anything else other than categories mentioned above, then just give which is given below.
                            "unavailable" = {}

                Do not justify or explain yourself. Answer in the prescribed format only.
                ''',
            "role": "system"
            },
            {
            "content": input_mail,
            "role": "user"
            }
        ]
        }
        # Make a POST request to the API endpoint with the data
            response = requests.post(API_URL, json=data)
        # Check the response from the API
            if response.status_code == 200:
                # API call successful
                api_response = response.json()
                print('API Response:', api_response)
                
                content = api_response['choices'][0]['message']['content']
                print('Content:', content)
            else:
            # API call failed
                print('API Error:', response.status_code, response.text)
    def switch_case(content):
     print("\ncategory:", content)
    switch = {
        'AccountStatement': account_statement,
        'LoanStatement': loan_statement,
        'CreditStatement': credit_statement
    }
    content = content.lower().strip()
    
    switch.get(content, "Invalid content")

    if 'accountstatement' in content:
         data, context = account_statement()
         email_res = email_generation(context)
    elif content == 'LoanStatement':
            loan_statement()
    elif content == 'CreditStatement':
                credit_statement()
    else:
            print("information not found")
            result = switch_case(content)

except mysql.connector.Error as error:
        print("Error:", error)
finally:
    # Close the cursor and connection
    if 'connection' in locals():
        cursor.close()
        connection.close()