##############################################################
## This program does the following
## 1) Reads value from photodiode
##      - 0: light is shining on diode
##      - anything other than zero corresponds to beam-break
##              ==> swinging-sticks flip
## 2) Sends value with time-stamp to plotly
##
##############################################################


##### Setting up Photodiode
from gpiozero import LightSensor
ldr = LightSensor(17, 1, 0.5, 0.99)

## Setting up Plotly
import matplotlib.pyplot as plt
import plotly 
import datetime
import time

##Set credentials the first time this program is run. 
plotly.tools.set_credentials_file(username='swinging-sticks', api_key='9QFKtwuiThwSDeWoiiqG', 
	stream_ids = ['n533fw623f', '11abz0z17d', 'dt2m0v8em8', '1eynig0e1q', 'ji10b2ilrx'])

import plotly.plotly as py
import plotly.tools as tls
from plotly.graph_objs import *

stream_ids = tls.get_credentials_file()['stream_ids']

###### Setting up plot on plotly

# Plotting when flip happens as a function of time
trace0 = Scatter(
    x = [],
    y = [],
    mode = 'lines',
    stream = Stream(token = stream_ids[0], maxpoints = 1000)
)

data0 = Data([trace0])
fig0 = Figure(data=data0) # plot of flips per minute
unique_url0 = py.plot(fig0, filename='Flip')
s0 = py.Stream(stream_ids[0])
s0.open()

#### Setup google sheets

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
  	'range': 'Sheet1!A1:B2',
  	'majorDimension': 'ROWS',
  	'values': [
    	["Timestamp"]
  	],
	}
	]

body = {
  'valueInputOption': 'USER_ENTERED',
  'data': data
}
result = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetId, body=body).execute()

def write2sheets(t):
	spreadsheet_id = '13EIFVg-c4Stt2fMWg3Lg2taKF_ykiljBJsN0ovEe6VI'
	range_ = "Sheet1!A1"

	body = { 
  	"values": [
	[t]
	] 
	}
	
	result = service.spreadsheets().values().append(spreadsheetId=spreadsheetId, range= range_, valueInputOption= 'USER_ENTERED', insertDataOption = 'INSERT_ROWS',  body=body).execute()
	####print(result)

######### Get signal, send to gsheets and plotly
t = datetime.datetime.now()
while(True):
	new_t = datetime.datetime.now()
	if (ldr.value > 0):
		val = 1
		dt = new_t - t
                print (dt)
                if (divmod(dt.days*86400 + dt.seconds, 60)[1] > 1):
                        t = new_t
                        write2sheets(t.strftime('%Y-%m-%d %H:%M:%S'))
                else:
                        continue

	else:
		val = 0
	s0.write(dict(x = new_t.time(),y =val))

 


