import getpass
import sys
import telnetlib
from time import sleep
import time
import ts3TeleBotConfig

HOST = "localhost"
PORT = 10011

def parseTsOutput(data):
	print("parseTsOutput")
	print(type(data))
	print(data)
	if type("") == type(data):
		result = list()
		for entryRaw in data.split("|"):
			entry = dict()
			for optionRaw in entryRaw.split(" "):
				if optionRaw.find("=") != -1:
					entryKey = optionRaw[0:optionRaw.find("=")].replace("\r","")
					entryVal = optionRaw[optionRaw.find("=")+1:].replace("\\s", " ")
					entry[entryKey] = entryVal
				else:
					entry[optionRaw] = None
			result.append(entry)
		return result
	else:
		return None

def getTSClients():
	tn = telnetlib.Telnet(ts3TeleBotConfig.TS3_HOST, ts3TeleBotConfig.TS3_PORT)
	sleep(1)
	tn.write(bytes("login serveradmin " + ts3TeleBotConfig.TS3_SA_PASSWD  + "\n", 'utf-8'))
	#print("Login Success")
	tn.read_until(b"error id=0 msg=ok\n")
	tn.write(b"use 1\n")
	tn.read_until(b"error id=0 msg=ok\n")
	tn.write(b"clientlist\n")
	cRaw = tn.read_until(b"error id=0 msg=ok\n").decode('utf-8')
	#parse clientlist output
	cList = parseTsOutput(cRaw)
	clients = list()
	#get channel info
	for cl in cList:
		if not "serveradmin" in cl["client_nickname"]:
			tn.write(bytes("clientinfo clid=" + str(cl["clid"]) + "\n", 'utf-8'))
			cRaw = tn.read_until(b"error id=0 msg=ok\n").decode('utf-8')
			#parse clientinfo output
			cInfoList = parseTsOutput(cRaw)
			cl["client_info"] = cInfoList[0]
			tn.write(bytes("channelinfo cid="+str(cInfoList[0]["client_channel_group_inherited_channel_id"])+"\n", 'utf-8'))
			cRaw = tn.read_until(b"error id=0 msg=ok\n").decode('utf-8')
			cChannelInfo = parseTsOutput(cRaw)
			cl["channel_info"] = cChannelInfo[0]
			clients.append(cl)
	#close telnet connection
	tn.write(b"quit\n")
	tn.read_until(b"error id=0 msg=ok\n")
	tn.close()
	return clients

def formatClients(clients):
	channels = sortByChannel(clients=clients)
	strOut = ""
	for channelName, channel in channels.items():
		strOut += channelName + '\n'
		for client in channel:
			since = time.strftime("%H:%M", time.localtime(int(client["client_info"]["client_lastconnected"])))
			strOut += '    '+client["client_nickname"]+', online seit '+ str(since) +'\n'
	return strOut

def sortByChannel(clients):
	channels = dict()
	for client in clients:
		if not client["channel_info"]["channel_name"] in channels:
			channels[client["channel_info"]["channel_name"]] = list()
			channels[client["channel_info"]["channel_name"]].append(client)
		else:
			channels[client["channel_info"]["channel_name"]].append(client)
	return channels

if __name__ == '__main__':
	import json
	clients = getTSClients()
	#print(json.dumps(clients, indent=4, sort_keys=True))
	print("\nSort by Channel:\n")
	print(json.dumps(sortByChannel(clients=clients), indent=4, sort_keys=True))
	print("\nFormatted Clients:\n")
	print(formatClients(clients=clients))
