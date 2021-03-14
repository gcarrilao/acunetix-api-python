import requests
import urllib3
import json
import hashlib
import re
from pprint import pprint

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Class acunetix api

class Acunetix ():


	# email password host-acunetix selfsigned-certificate
	def __init__(self,email,password,host,secure):
		self.secure = secure
		self.host= host
		self.fullhost= host + "/api/v1"
		self.request = requests.Session()
		self.__login(email,password)

	# Verified if a is login in acunetix
	def is_logged(self):
		c = self.__get_request("/me").status_code
		return (c == 200)

	# get login to acunetix
	def __login(self,email,password):
		url_login = "{}/me/login".format(self.fullhost)
		sha256_password =  hashlib.sha256(password.encode()).hexdigest()
		js = {
			"email" : email,
			"password": sha256_password,
			"remember_me" : False,
			"logout_previous": True,
		}
		payload = json.dumps(js)
		headers = {
		    'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0",
		    'Accept': "application/json, text/plain, */*",
		    'Accept-Language': "es-AR,es;q=0.8,en-US;q=0.5,en;q=0.3",
		    'Accept-Encoding': "gzip, deflate, br",
		    'Connection': "keep-alive",
		    'Content-Type': "application/json",
		    'cache-control': "no-cache",
		    }
		r = self.request.request("POST", url_login, data=payload, headers=headers,verify=self.secure)
		self.headers= r.headers
		self.cookies= r.cookies

	# post requests base
	def __post_request(self,path,payload):
		r = self.request.request("POST", self.fullhost+path, data=payload, headers=self.headers,cookies=self.cookies,verify=self.secure)
		return r

	# get requests base
	def __get_request(self,path):
		r = self.request.request("GET", self.fullhost+path, headers=self.headers,cookies=self.cookies,verify=self.secure)
		return r

	# get targets
	def get_targets(self):
		r = self.__get_request("/targets")
		return json.loads(r.text)

	# get a specific target
	def get_target(self,target):
		r = self.__get_request("/targets/{}".format(target))
		return json.loads(r.text)
	# get scans
	def get_scans(self):
		r = self.__get_request("/scans")
		return json.loads(r.text)
	# get a specific scan
	def get_scan(self,scan):
		r = self.__get_request("/scans/{}".format(scan))
		return json.loads(r.text)
	# get session id from scan
	def get_session_id_from_scan(self,scan):
		r = self.get_scan(scan)
		return r["current_session"]["scan_session_id"]
	# def get results
	def get_results(self,scan,session_id):
		r = self.__get_request("/scans/{}/results/{}/vulnerabilities".format(scan,session_id))
		return(json.loads(r.text))
	# def get result with cursor
	def get_results_with_cursor(self,scan,session_id,cursor):
		r = self.__get_request("/scans/{}/results/{}/vulnerabilities?c={}".format(scan,session_id,cursor))
		return(json.loads(r.text))
	# def all result
	def get_all_results(self,scan,session_id):
		all_result={}
		all_result["vulnerabilities"] = []
		cursor = "0"
		while (cursor is not None):
			r = self.get_results_with_cursor(scan,session_id,cursor)
			all_result["vulnerabilities"]= all_result["vulnerabilities"] + r["vulnerabilities"]
			cursor= r["pagination"]["next_cursor"]
		return all_result
	#get last scan from a target
	def get_last_scan_from_target(self,target):
		r = self.get_target(target)
		return r["last_scan_id"]
	#get export types
	def get_export_types(self):
		r = self.__get_request("/export_types")
		return r.text
	#get vulneribility from scan
	def get_vulnerability_from_scan(self,scan,session_id,vuln_id):
		r = self.__get_request("/scans/{}/results/{}/vulnerabilities/{}".format(scan,session_id,vuln_id))
		return json.loads(r.text)
	# get scan vulneraribilt types
	def get_scan_vulnerability_types(self,scan,session_id):
		r = self.__get_request("/scans/{}/results/{}/vulnerability_types".format(scan,session_id))
		return json.loads(r.text)
	# get targets with name
	def get_targets_with_name(self,name):
		t = self.get_targets()["targets"]
		name_targets=[]
		p = re.compile(r'.*{}*'.format(name))
		for i in t:
			if(p.match(i["description"])):
				name_targets.append(i)
		return name_targets
