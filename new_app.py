import gspread
import pandas as pd
import json
import os

# Load the credentials JSON from the environment variable
credentials_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Parse the JSON string to a dictionary
credentials_dict = json.loads(credentials_json)

# Initialize the client using the provided service account credentials
gc = gspread.service_account_from_dict(credentials_dict)

sheet = gc.open('WGA_Training_Log_GS').sheet1
data = sheet.get_all_values()

# Convert the data to a Pandas DataFrame.
headers = data.pop(0)  # Assuming the first row contains headers.
df = pd.DataFrame(data, columns=headers)

# Reverse the order of rows
df_reversed = df[::-1]

# Add a new column with row numbers in reverse order
df_reversed.insert(0, 'Row_Number', range(len(df_reversed), 0, -1))

# Process the 'Workout' column to add line breaks
df_reversed.loc[:, 'Workout'] = df_reversed['Workout'].str.replace('\n', '<br>').str.replace('<br>- ', '<br>').str.replace('- ', '<br>')

# Convert DataFrame to HTML with some styling
html_table = df_reversed.to_html(index=False, classes='my-table-class', border=1, table_id='my-table', justify='center', escape=False)


# Prettify the HTML table
styled_html = f'''
<!DOCTYPE html>
<html>
<head>
<style>
.my-table-class {{
  font-family: Arial, sans-serif;
  border-collapse: collapse;
  width: 100%;
  border: 1px solid #ddd;
}}
.my-table-class th, .my-table-class td {{
  padding: 8px;
  text-align: center;
}}
.my-table-class th {{
  background-color: #f2f2f2;
}}
.my-table-class td:nth-child(3) {{
  text-align: left;
  white-space: pre-wrap;
  width: 50%; /* Adjust the width as needed */
}}
.my-table-class td:nth-child(4) {{
  text-align: center;
  width: 30%; /* Adjust the width as needed */
}}
.my-table-class td:nth-child(1) {{
  width: 5%; /* Adjust the width as needed */
}}
</style>
</head>
<body>
{html_table}
</body>
</html>
'''

# Save the prettified HTML to a file
output_file_path = 'index.html'
with open(output_file_path, 'w', encoding='utf-8') as f:
    f.write(styled_html)

#print(f"Styled HTML table saved to {output_file_path}")
