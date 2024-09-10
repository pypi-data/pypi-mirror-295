# 🔧 utilita
[![PyPI version](https://badge.fury.io/py/utilita.svg)](https://badge.fury.io/py/utilita)
[![Build Status](https://travis-ci.com/json2d/utilita.svg?branch=master)](https://travis-ci.com/json2d/utilita) [![Coverage Status](https://coveralls.io/repos/github/json2d/utilita/badge.svg?branch=master)](https://coveralls.io/github/json2d/utilita?branch=master)

a utility library

## Quick install
```bash
pip install utilita
```

## Basic usage

[decent pitch]. Let's dive in.

Out-of-the-box you get some stuff you can do with utilita:

```py
import datetime
from utilita import date_fns

w52d7 = datetime.date(2020,12,27)
w53d1 = datetime.date(2020,12,28)

date_fns.is_in_leap_week(w52d7) # => False
date_fns.is_in_leap_week(w53d1) # => True

date_fns.days_since_same_date_last_year(w52d7) # => 364 (days in non-leep-week years)
date_fns.days_since_same_date_last_year(w53d1) # => 371 (days in leep-week years)

```

more about ISO 8601 leap weeks: https://en.wikipedia.org/wiki/ISO_week_date


# Examples:

## Working with sendgrid

```python
from utilita import sendgridhelper as sghelper

eml = sghelper.SendgridHelper(
    sendgrid_api_key=os.getenv('sendgrid_key'), 
    from_email={"email": 'test@example.com', "name": "Test BI"}
    )

email_subject = f'Testing email from Test BI sent on {int(datetime.datetime.now().timestamp())}'
email_body = '''
    <html>
    <body>
    Hello, <br />
    This is a test email<br />
    <i>Derp</i>
    <br><br>
    Thank you,<br>
    Test BI
    </body>  
'''

eml.config_email(subject=email_subject,
                 body=email_body,
                 recipients={
                     "to": "user1@example.com, user2@example.com",
                    #  "cc": "test@example.com",
                    #  "bcc": "bcc@example.com"
                 }
                 )

# Attach excel files from disk:
eml.attach_excel_file_from_path('files/1.xlsx')
eml.attach_excel_file_from_path('files/2.xlsx')

# attach dataframe as a csv file.
import pandas as pd

headers = ['date', 'department', 'sales']
data = [
    ('2023-12-20', 'Bread', 100),
    ('2023-12-20', 'Deli', 1),
    ('2023-12-20', 'Frozen', 400)
]
df = pd.DataFrame(columns=headers, data=data)
# compressed will compress to a zip file.
eml.attach_single_df_as_csv(df=df, df_filename='sales.csv', compressed=True)

# Send email
eml.send_email()
```

## Example for working with excel workbooks
```python
from utilita import excel
import pandas as pd
import openpyxl as xl

wb = xl.load_workbook(filename='files/tables.xlsx')

# Load dataframe into an excel table:
df = excel.excel_table_to_df(wb=wb, sheet_name='Sheet1', table_name='Table2')

# Get data from an excel table into a dataframe:
# Export table into excel workbook
headers = ['date', 'department', 'sales']
data = [
    ('2023-12-20', 'Bread', 100),
    ('2023-12-20', 'Deli', 1),
    ('2023-12-20', 'Frozen', 400)
]
df = pd.DataFrame(columns=headers, data=data)

excel.df_to_excel_table_resize(df=df, wb=wb, sheet_name='Sheet1', table_name='Table2')

```