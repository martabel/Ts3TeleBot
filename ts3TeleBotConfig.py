import toml
import os
import os.path

TS3_HOST = 'localhost'
TS3_PORT = 10011
TS3_SA_PASSWD = None
TELEGRAM_TOKEN = None
TOML_CONFIG_PATH = 'config.toml'

def readToml(configPath):
	ts3Host = None
	ts3Port = None
	ts3SaPasswd = None
	teleToken = None
	with open(configPath) as cfFile:
		tomlParsed = toml.loads(cfFile.read())
		ts3Host = tomlParsed['teamspeak']['host']
		ts3Port = tomlParsed['teamspeak']['port']
		ts3SaPasswd = tomlParsed['teamspeak']['sa_passwd']
		teleToken = tomlParsed['telegram']['api_token']
	return ts3Host, ts3Port, ts3SaPasswd, teleToken

if 'TS3_TELE_BOT_CFG' in os.environ.keys():
	TOML_CONFIG_PATH = os.environ['TS3_TELE_BOT_CFG']

# try to read toml config
if os.path.isfile(TOML_CONFIG_PATH):
	TS3_HOST, TS3_PORT, TS3_SA_PASSWD, TELEGRAM_TOKEN = readToml('config.toml')
else:
	print("No config found in " + TOML_CONFIG_PATH)
	quit()
