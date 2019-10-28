from config import *
from acunetix import *


acu = Acunetix(username,password,host,False)


r = acu.get_all_results("895ec03c-c936-42df-b86b-7c55af1cdc19","3909175c-68ea-43af-a205-abd626788f50")

for i in r["vulnerabilities"]:
	if (i["vt_name"].lower() == "directory listing"):
		print(i["affects_url"])
