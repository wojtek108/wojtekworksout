# https://chat.openai.com/share/72db03df-da4e-4241-b997-e53acdeafec2


import gspread
import pandas as pd
import google.auth

# Initialize the client using the service account credentials
credentials, project = google.auth.default()
gc = gspread.service_account(filename='credentials.json')  # Update this line

if gc:
    # Your code to interact with Google Sheets
    print('Connection ok!')
else:
    print("Failed to initialize the client.")
