from quickstart import *
import csv

credentials = get_credentials()
http = credentials.authorize(httplib2.Http())
discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                'version=v4')
service = discovery.build('sheets', 'v4', http=http,
                          discoveryServiceUrl=discoveryUrl)

spreadsheetId = '1GJqD4TVmSu3C2EBGDzlO-0pLiADkHXB2hTXijnNSdG0'
rangeName = 'Form Responses 1!A2:C'
result = service.spreadsheets().values().get(
    spreadsheetId=spreadsheetId, range=rangeName).execute()
values = result.get('values', [])

response = []

if not values:
    print('No data found.')
else:
    print('Time, Response:')
    for row in values:
        # Print columns A and E, which correspond to indices 0 and 4.
        print('%s, %s' % (row[0], row[1]))
        response.append([row[0], row[1]])


with open('response-data.csv', 'w') as csvfile:
    fieldnames = ['Time', 'Response']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for item in response:
        writer.writerow({'Time':item[0], 'Response':item[1]})





