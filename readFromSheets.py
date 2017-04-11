import csv
import pandas
from pprint import pprint
from dateutil import parser
from quickstart import *
from datetime import datetime
credentials = get_credentials()
http = credentials.authorize(httplib2.Http())
discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

spreadsheet_id = '13EIFVg-c4Stt2fMWg3Lg2taKF_ykiljBJsN0ovEe6VI'

range_ = "A:A"
value_render_option = "FORMATTED_VALUE"
date_time_render_option = "SERIAL_NUMBER"

request = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_, valueRenderOption=value_render_option, dateTimeRenderOption=date_time_render_option)
response = request.execute()

values = response.get('values', [])
f = open('timestamp.csv', 'w')
if not values:
    print('No data found.')
else:
    for row in values:
        print('%s' % (str(row[0])))
	f.write(str(row[0])+'\n')
       

