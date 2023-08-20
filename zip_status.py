import tkinter as tk
import datetime
from nestops_client import NestOpsClient

root = tk.Tk()
root.title("Flight and Zip Status")
root.geometry("350x1366")

label_font = ("Times New Roman", 50, "bold")
label_padx = 200
label_pady = 8

flights_desc = tk.Label(root, text="Total Flights", font=("Georgia", 20, "bold"), bg="#ffffff", fg="#202020")
flights_desc.pack(padx=10, pady=2)
flights_label = tk.Label(root, text="", font=label_font, bg="azure4", fg="#000000", padx=label_padx, pady=label_pady)
flights_label.pack(fill=tk.Y, expand=True)

deliveries_desc = tk.Label(root, text="Deliveries", font=("Georgia", 20, "bold"), bg="#ffffff", fg="#202020")
deliveries_desc.pack(padx=10, pady=2)
deliveries_label = tk.Label(root, text="", font=label_font, bg="azure4", fg="#000000",
                                padx=label_padx, pady=label_pady)
deliveries_label.pack(fill=tk.Y, expand=True)

avg_time_desc = tk.Label(root, text="Avg Launch Time", font=("Georgia", 20, "bold"), bg="#ffffff", fg="#202020")
avg_time_desc.pack(padx=10, pady=2)
avg_time_label = tk.Label(root, text="", font=("Times New Roman", 15, "bold"), bg="azure2", fg="#000000",
                          padx=label_padx, pady=label_pady)
avg_time_label.pack(fill=tk.Y, expand=True)

outbound_desc = tk.Label(root, text="Outbound", font=("Georgia", 20, "bold"), bg="#ffffff", fg="#202020")
outbound_desc.pack(padx=10, pady=2)
outbound_label = tk.Label(root, text="", font=label_font, bg="azure3", fg="#000000",
                                padx=label_padx, pady=label_pady)
outbound_label.pack(fill=tk.Y, expand=True)

inbound_desc = tk.Label(root, text="Inbound", font=("Georgia", 20, "bold"), bg="#ffffff", fg="#202020")
inbound_desc.pack(padx=10, pady=2)
inbound_label = tk.Label(root, text="", font=label_font, bg="azure3", fg="#000000",
                                padx=label_padx, pady=label_pady)
inbound_label.pack(fill=tk.Y, expand=True)

avail_zips_desc = tk.Label(root, text="Zips Available", font=("Georgia", 20, "bold"), bg="#ffffff", fg="#202020")
avail_zips_desc.pack(padx=10, pady=2)
avail_zips_label = tk.Label(root, text="", font=label_font, bg="azure3", fg="#000000",
                                padx=label_padx, pady=label_pady)
avail_zips_label.pack(fill=tk.Y, expand=True)

NEST_ID = 7

def get_airborne_flights():
    # Fetch the data and update the variables
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
    flights = response.json()
    def is_outbound(flight):
        if flight['timeLaunched'] is not None and flight['timeRecovered'] is None and flight['timeDelivered'] is None:
            return True
        return False

    def is_inbound(flight):
        if flight['timeRecovered'] is None and flight['timeDelivered'] is not None or flight['timeMissionFailure'] is not None:
            return True
        return False

    num_of_outbound = 0
    num_of_inbound = 0
    zip_total = 14
    for flight in flights:
        if is_outbound(flight):
            num_of_outbound += 1
        if is_inbound(flight):
            num_of_inbound += 1

    inbound, outbound = num_of_inbound, num_of_outbound
    num_avail_zip = zip_total - (num_of_inbound + num_of_outbound)
    return [outbound, inbound, num_avail_zip]

def get_data():
    # Fetch the data from NestOpsClient
    get_date = datetime.date.today()
    client = NestOpsClient("796d165c-2f0e-4f68-9fd7-20116ef82187")
    snapshot = client.get_snapshot(NEST_ID, f"{get_date}", f"{get_date}")
    flight_count = snapshot["rawData"]["total_flights"]
    delivery_count = snapshot["rawData"]["deliveries"]["total"]
    mission_failure_before_delivery = snapshot["rawData"]["incidents"]["mission_failures"]["before_delivery"]
    off_nominal_flights = snapshot["rawData"]['off_nominals']['flights_affected']
    nominal_flights = flight_count - off_nominal_flights
    avg_time = snapshot['rawData']['operations']['nominal']['time_commit_to_launch'][4:11]
    test = get_airborne_flights()
    
    return [
        flight_count, 
        delivery_count,     
        avg_time,
        test[0],
        test[1],
        test[2],
    ]

def update_labels():
    data = get_data()

    flights_label.config(text=f"{data[0]}")
    deliveries_label.config(text=f"{data[1]}")
    avg_time_label.config(text=f"{data[2]}")
    outbound_label.config(text=f"{data[3]}")
    inbound_label.config(text=f"{data[4]}")
    avail_zips_label.config(text=f"{data[5]}")
    
    # Update other labels with the respective data

    root.after(500, update_labels)  # Schedule the next update

update_labels()  # Initial update
root.mainloop()
