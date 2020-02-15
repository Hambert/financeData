
# importing modules 
import json
import urllib.request
from flask import Flask, render_template, redirect
import time
import settings
myKey = settings.APIKEY
#
def getTimeSeriesData(symbol, api):
	urlData = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+symbol+'&outputsize=conpact&datatype=json&apikey=' + api
	webURL = urllib.request.urlopen(urlData)
	data = webURL.read()
	encoding = webURL.info().get_content_charset('utf-8')
	return json.loads(data.decode(encoding))


# declaring app name
app = Flask(__name__) 


@app.route('/')
def index():
	return redirect("/main", code=302)


@app.route('/main')
def main():
	if myKey is not None:
		VIX_data = getTimeSeriesData("VIX", myKey)
		VIX_timeSeries = VIX_data["Time Series (Daily)"]

		VXV_data = getTimeSeriesData("VXV", myKey)
		VXV_timeSeries = VXV_data["Time Series (Daily)"]

		dataFrom = VXV_data["Meta Data"]["3. Last Refreshed"]
		struct_time = time.strptime(dataFrom, "%Y-%m-%d")
		strTime = time.strftime("%d.%m.%Y", struct_time)

		lastVIX = VIX_data["Time Series (Daily)"][dataFrom]['4. close']
		lastVXV = VXV_data["Time Series (Daily)"][dataFrom]['4. close']

		chartData = ''

		for key, value in VXV_timeSeries.items():
			try:
				vix = float(VIX_timeSeries[key]['4. close'])
				vxv = float(VXV_timeSeries[key]['4. close'])
				result = round(vix / vxv, 3)
				chartData = chartData + '[\'' + key + '\', ' + str(result) + ', ' + str(vix) + ', ' + str(vxv) + '],'
				# print(key + ", VIX: " + str(vix) + " VXV: " + str(vxv) + " res: " + str(result))

			except KeyError:
				print('ende')

		return render_template("main.html", data=chartData, date=strTime, vix=lastVIX, vxv=lastVXV)
	else:
		return redirect("/error", code=302)


@app.route('/about')
def about():
	return render_template("about.html")


@app.route('/settings') 
def settings():
	return render_template("settings.html")


@app.route('/error')
def errorpage():
	return render_template("error.html")


if __name__ == '__main__': 
	# running app 
	app.run(use_reloader = True, debug = True) 
