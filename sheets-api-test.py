from quickstart import *
credentials = get_credentials()
http = credentials.authorize(httplib2.Http())
discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

spreadsheetId = '13EIFVg-c4Stt2fMWg3Lg2taKF_ykiljBJsN0ovEe6VI'
data = [ 
	{
  	"range": "Sheet1!A1:D5",
  	"majorDimension": "ROWS",
  	"values": [
    	["Item", "Cost", "Stocked", "Ship Date"],
    	["Wheel", "$20.50", "4", "3/1/2016"],
    	["Door", "$15", "2", "3/15/2016"],
    	["Engine", "$100", "1", "30/20/2016"],
    	["Totals", "=SUM(B2:B4)", "=SUM(C2:C4)", "=MAX(D2:D4)"]
  	],
	}
	]

body = {
  'valueInputOption': 'USER_ENTERED',
  'data': data
}
result = service.spreadsheets().values().batchUpdate(
    spreadsheetId=spreadsheetId, body=body).execute()

print(result)
