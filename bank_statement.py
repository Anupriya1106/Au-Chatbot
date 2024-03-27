import requests

def get_bank_statement(cursor, email):
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
            
    # email = "emily.brown@gmail.com"
    # get_bank_statement(email)

def classify_mail(API_URL, input_mail):

#     API_URL = 'http://ec2-13-201-130-252.ap-south-1.compute.amazonaws.com:8080/v1chat/prompt'
#     # input_mail = input("")
#     input_mail = '''
#    As a senior citizen it is difficult to visit a branch or make a video call , please suggest other options to update maturity instructions. If you can send a form by email i can resend back with a sign on it by email if you consider it.
# Thanks!
# Customer name
#     '''
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
        content = api_response['choices'][0]['message']['content']
        return content
    else:
         return "Error: Unable to classify mails"
