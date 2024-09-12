#LabelPrint by Pecacheu; MIT License

import json, time
from threading import Timer
from selenium import webdriver
from selenium.webdriver.chromium.webdriver import ChromiumDriver
from pycolorutils.color import *

#--- Global WebDriver ---

Options = {
	'timeout': 120, 'engine': "Edge",
	'headless': True, 'silent': False
}
_Drv: ChromiumDriver|None = None
_Tmr: Timer|None = None

def startDriver():
	global _Drv, _Tmr
	if _Tmr: _Tmr.cancel(); _Tmr=None
	if _Drv is False: raise BlockingIOError("WebDriver busy")
	if _Drv: return _Drv
	opt = webdriver.EdgeOptions()
	if Options['headless']: opt.arguments.append("--headless")
	state = {
		'recentDestinations':[{'id':"Save as PDF", 'origin':"local", 'account':""}],
		'selectedDestinationId':"Save as PDF", 'version':2
	}
	prefs = {'printing.print_preview_sticky_settings.appState': json.dumps(state)}
	opt.add_experimental_option('prefs', prefs)
	opt.add_experimental_option('excludeSwitches', ['enable-logging'])
	_Drv = getattr(webdriver, Options['engine'])(opt)
	return _Drv

def stopDriver(force=False):
	global _Drv, _Tmr
	if _Tmr: _Tmr.cancel()
	if not _Drv: return
	if force:
		d=_Drv; _Drv=False; _Tmr=None
		if not Options['silent']:
			msg(C.Di+"[Shutting down WebDriver in background]")
		d.quit()
		if not Options['silent']:
			msg(C.Di+"[WebDriver stopped]")
		_Drv=None
	else:
		_Tmr = Timer(Options['timeout'], stopDriver, [True])
		_Tmr.start()

def getDriver():
	return _Drv

def _exit():
	stopDriver(True)

atexit(_exit)
_GetPerf = ("let n=new URL({}).pathname,l=[],p=performance.getEntries(),"
	"i=p.length-1; for(; i>=0; --i) try {{if(new URL(p[i].name)"
	".pathname===n) return p[i]}} catch(e){{}}")

def get(uri, timeout):
	st=time.monotonic(); _Drv.get(uri)
	while time.monotonic()-st < timeout:
		pf = _Drv.execute_script(_GetPerf.format(json.dumps(uri)))
		if not pf: continue
		res = pf['responseStatus']
		if res != 200: raise ConnectionError(res)
		return res
	raise TimeoutError(uri)