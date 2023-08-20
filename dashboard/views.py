from django.shortcuts import render
import requests
import datetime
import time
from .nestops_client import NestOpsClient
from django.http import JsonResponse

from requests.exceptions import ConnectionError, Timeout
import tkinter as tk
import time
import threading
import math


NEST_ID= 7


def dashboard(request):

    return render(request,'dashboard/base.html',{})


# This section of the code contains the logic for counting the number of airborne zips
# and by extension the number of available slots
def get_airborne_flights():
    nest_id = NEST_ID
    end_time = datetime.datetime.utcnow()
    start_time = end_time - datetime.timedelta(hours=2)
    end_time = end_time.isoformat()
    start_time = start_time.isoformat()

    endpoint = "api/flights"

    response = NestOpsClient("796d165c-2f0e-4f68-9fd7-20116ef82187").get_request(
        endpoint,
        {
            "nest": nest_id,
            "start": start_time,
            "end": end_time,
        },
    )
    flights = response.json() # Convert the response data to a JSON format
    #print(flights)

    # This  function counts the number of outbound flights
    def is_outbound(flight):
        if flight['timeLaunched'] is not None and flight['timeRecovered'] is None and flight['timeDelivered'] is None:
            return True
        return False
        
    # This function counts the number of inbound flights
    def is_inbound(flight):
        if flight['timeRecovered'] is None and flight['timeDelivered'] is not None or flight['timeMissionFailure'] is not None:
            return True
        return False

    num_of_outbound = 0
    num_of_inbound = 0
    zip_total = 14
    for  flight in flights:
        if is_outbound(flight):
            num_of_outbound+= 1
        if is_inbound(flight):
            num_of_inbound+=1

    inbound, outbound = num_of_inbound,num_of_outbound
    num_avail_zip = zip_total - (num_of_inbound + num_of_outbound)
    # print(inbound,outbound)
    return [inbound,outbound,num_avail_zip]

"""
    This next script is for showing the batteries fully charged as well as a categorization of 2-dot and 3-dot
"""
url = "http://10.0.0.3:5005/status"
max_retries = 3
retry_delay = 5
bcb_numbers_3dots = [
"17S6A6611017027"
,"17S6C4419005023"
,"17S6A6611002027"
,"17S6A6612034016"
,"17S6A6611010030"
,"17S6A6612012049"
,"17S6C4419040024"
,"17S6A6611019040"
,"18S9Y4825030054"
,"17S6A6611060035"
,"17S6A6611051024"
,"17S6A6611006023"
,"18S9Y4823013035"
,"17S6A6611052035"
,"17S6A6611058028"
,"17S6A6611025013"
,"18S9Y4822013050"
     ]
def update_data():
    for retry in range(max_retries):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                content = response.json()
                ready_batteries_2dots = 0
                ready_batteries_3dots = 0
                for battery in content.values():
                    if battery["state"] == "READY_FOR_FLIGHT":
                        if battery["battery_a_serial"] in bcb_numbers_3dots:
                            ready_batteries_3dots += 1
                        else:
                            ready_batteries_2dots += 1

                #display_results(ready_batteries_2dots, ready_batteries_3dots)
                break

        except (ConnectionError, Timeout):
            print("Connection attempt failed. Retrying...")
            time.sleep(retry_delay)
    else:
        print("Failed to establish a connection after multiple retries.") 
    ready_batteries_total = ready_batteries_3dots + ready_batteries_2dots
    return [ready_batteries_total, ready_batteries_3dots, ready_batteries_2dots]
     

def get_data(request):
        """THIS  SECTION OF THE CODE IS WHERE WE ADD/COMPUTE 
        METRICS TO BE DISPLAYED ON THE DASHBOARD.
        EVERY VALUE HAS A DESCRIPTIVE COMMENT ON WHAT IS IT. REACH OUT  
        SIAW IF YOU NEED TO ADD A VALUE"""

        get_date= datetime.date.today() # GET THE CURRENT DATE AT NATIVE NEST
        client = NestOpsClient("796d165c-2f0e-4f68-9fd7-20116ef82187") #UNIQUE TOKEN FOR EACH NEST
        snapshot = client.get_snapshot(NEST_ID, f"{get_date}",f"{get_date}")
        flight_count=snapshot["rawData"]["total_flights"]             # VALUE FOR THE TOTAL FLIGHTS
        #print (snapshot["rawData"])
        delivery_count=snapshot["rawData"]["deliveries"]["total"] #VALUE FOR TOTAL DELIVERIES
        #print(delivery_count)
        mission_failure_before_delivery=(snapshot["rawData"]["incidents"]["mission_failures"]["before_delivery"]) #MISSION FAILURE BEFORE DELIVERY
        off_nominal_flights=(snapshot["rawData"]['off_nominals']['flights_affected'])  #OFF-NOMINAL FLIGHTS
        nominal_flights=  flight_count-off_nominal_flights    # SOLUTION FOR NOMINAL FLIGHTS
        avg_time=(snapshot['rawData']['operations']['nominal']['time_commit_to_launch']) # Average time for nominal package commitment to launch
        avg_time=(avg_time[4:11]) #SLICING THE AVERAGE TIME STRING TO DISPLAY ONLY MINUTES AND SECONDS
        ratios= (mission_failure_before_delivery)
        set_count=50   # CHANGE THIS VALUE TO COMMENSURATE HOW MANY FLIGHTS THAT ARE REQUIRED TO START A CHANGE OVER
        swap_value = flight_count % set_count # THIS DOES A MODULO DIVISION TO CHECK IF SET TIME FOR  CHANGEOVER IS EQUAL TO THE CURRENT FLIGHT COUNT

        # THE SECTION BELOW CONTAINS THE CHANGEOVER LOGIC. CONTACT STELLA FOR ANY CHANGES
        if flight_count==0:
                percentage_nominal='0'
        else:
                percentage_nominal =str(round((nominal_flights/flight_count)*100)) + "%"


        counter= math.ceil(flight_count/set_count)

        if  flight_count <= set_count:
                count_down = set_count- flight_count
        else:              
                count_down = (set_count * counter)- flight_count

        #if swap_value ==0:

               # display_swap='Available Zips'              
      #  else: 
             #   display_swap='CHANGEOVER COUNTDOWN : ' + str(abs(count_down))
        display_swap = 'Available Zips:'
        test = get_airborne_flights()
        battery_status = update_data()
       
       # avail_zip = total_zips - (test[1] + test[0])
        json_dict={
                'hello':'there',
                'flights':flight_count,
                'nominal_flights':nominal_flights,
                'avg_time':avg_time,
                'percentage_nominal':percentage_nominal,
                'ratios':ratios, 
                'swap_value':swap_value,
                'display_swap':display_swap,
                'num_inbound':test[0],
                'num_outbound':test[1],
                'available_zips':test[2],
                'num_delivery':delivery_count,
                'total_bats':battery_status[0],
                'dot3_bats':battery_status[1],
                'dot2_bats':battery_status[2],

        }
#'num_inbound': inbound_outbound[1],
                # 'num_outbound':inbound_outbound[0],

        return JsonResponse(json_dict)

def Get_Maintenance(request):
    
    operator= [operator.objects.all()]
    context={
        'operator':operator
    }
    
        
    return render(request,'dashboard/base.html',context)




# THIS IS LEGACY CODE AND SHOULD BE USED AS A FALLBACK

# def is_airborne(flight):
#     """This is a nested function that contains the logic which determines which flights are airborne
#        based on the event time stamps of the flights
#     """
#     if flight["timeLaunched"] is None:
#         # This means the flight never launched
#         return False
#     if flight["timeRecovered"] is not None or flight["timeFlightFailure"] is not None:
#         # This means the flight either recovered or paralanded
#         return False

#     # If it gets here, this means the flight launched but has not recovered
#     return True

# num_airborne_flights = 0
# for flight in flights:
#     if is_airborne(flight):
#         num_airborne_flights = num_airborne_flights + 1
