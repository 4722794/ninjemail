## python3
#%%
from ninjemail import Ninjemail
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
proxy_df = pd.read_csv('proxylist.csv')
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']



creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
client = gspread.authorize(creds)
sheet = client.open('emails').sheet1
names_df = pd.DataFrame(sheet.get_all_records())

#%%

#%%
def makemail(proxy,names):
    sample_entry = names[names['status'] == 'FALSE'].sample(1)
    sample_proxy = proxy.sample(1).iloc[0].item()

    mailninja = Ninjemail(
        browser='chrome',
        captcha_keys={"capsolver":"CAP-3B5921360B2858E989C79C5B773E069F"},
        sms_keys={"smspool": {"token": "T7u1n6Wn4vGSzAA7pQZVopZHCgm47Sx4"}},
        # proxy=sample_proxy,
        auto_proxy=True)
    userinfo = sample_entry[['username','password','first_name','last_name']].to_dict(orient='records')[0]
    idx = sample_entry.index.item()
    email,password = mailninja.create_gmail_account(**userinfo)
    print(f'New email created with username: {email} and password: {password}')
    return email,idx

#%%
for _ in range(3):
    try:
        email, idx = makemail(proxy_df,names_df)
        sheet.update_cell(idx+2, 5, email)
        sheet.update_cell(idx+2, 6, 'TRUE')
    except Exception as e:
        print(e)

#%%