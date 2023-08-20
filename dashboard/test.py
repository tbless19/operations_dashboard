import pprint
import datetime
import pyttsx3 as pt


speaker =pt.init()
speaker.say('look mama, I can talk')
get_date= datetime.date.today()

from nestops_client import NestOpsClient
client = NestOpsClient("796d165c-2f0e-4f68-9fd7-20116ef82187")
snapshot = client.get_snapshot(5,f"{get_date}", f"{get_date}")
pprint.pprint(snapshot["rawData"]['off_nominals']['flights_affected'])#["total_flights"]
#print(snapshot["rawData"]["incidents"]["mission_failures"])
#time=(snapshot['rawData']['operations']['nominal']['time_commit_to_launch'])
#print(time[5:11])
#print(snapshot)
#speaker.runAndWait()