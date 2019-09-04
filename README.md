# Acunetix API

## Create Acunetix
```python

acu = Acunetix(username,password,url,False)
print("Is logged?: {} ".format(acu.is_logged()))

```
## Get target

```python
pprint(acu.get_targets())
```

## PoC
```python
target="42e9892c-3ce0-4cdb-808e-3d9811dd774f"
if(target):
	print("Get target: {}".format(acu.get_target(target)))

	scan = acu.get_last_scan_from_target(target)

	print("Get scan : {} ".format(acu.get_scan(scan)))


	print("Get session id : {} ".format(acu.get_session_id_from_scan(scan)))

	session_id = acu.get_session_id_from_scan(scan)

	#pprint("Get results from scan: {} ".format(acu.get_results(scan,session_id)) )

	results = acu.get_results(scan,session_id)
	for i in results["vulnerabilities"]:
		print("Result: {}".format(i))
		print(i["vuln_id"])
		pprint("Vuln: {}".format(acu.get_vulnerability_from_scan(scan,session_id,i["vuln_id"])))

```
