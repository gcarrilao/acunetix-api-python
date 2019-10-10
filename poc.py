from config import *
from acunetix import *


acu = Acunetix(username,password,host,False)

t =acu.get_targets()
imq_targets = []
for i in t["targets"][7:8]:
        scan = acu.get_scan(i["last_scan_id"])
        target_id = i["target_id"]
        #target= acu.get_target(target_id)
        scan = acu.get_last_scan_from_target(target_id)
        session_id = acu.get_session_id_from_scan(scan)
        r = acu.get_all_results(scan,session_id)
	print(r)
