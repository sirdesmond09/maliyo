import requests, os


def bank_verification(code, account_num):
    res = requests.get(
        url = f'https://api.paystack.co/bank/resolve?account_number={account_num}&bank_code={code}', 
                       
        headers={
            'Authorization':f"Bearer {os.getenv('PAYSTACK_SECRET_KEY')}"
        })

   

    if res.json()['status'] == True:
        data = dict(res.json()['data'])
        data.pop('bank_id')
        return data