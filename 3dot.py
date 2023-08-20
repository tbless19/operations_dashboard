import requests
from requests.exceptions import ConnectionError, Timeout
import tkinter as tk
import time
import threading

url = "http://10.0.0.3:5005/status"
max_retries = 3
retry_delay = 5
bcb_numbers_3dots = ["17S6A6602013026"
,"17S6A6611002027"
,"17S6A6611006023"
,"17S6A6611010030"
,"17S6A6611017027"
,"17S6A6611019040"
,"17S6A6611025013"
,"17S6A6611026038"
,"17S6A6611051024"
,"17S6A6611052035"
,"17S6A6611058028"
,"17S6A6611059023"
,"17S6A6611060035"
,"17S6A6612012049"
,"17S6A6612034016"
,"17S6C4419005023"
,"17S6C4419040024"
,"17S6C4419050025"
,"17S6C4420013009"
,"18S9Y4822013050"
,"18S9Y4822027038"
,"18S9Y4823022008"
,"18S9Y4825030054"]


root = tk.Tk()
root.title("Battery Status")
root.geometry("350x1366")

label_font = ("Times New Roman", 100, "bold")
label_padx = 200
label_pady = 8

total_desc = tk.Label(root, text="Total Charged Batteries", font=("Arial", 30), bg="#ffffff", fg="#202020")
total_desc.pack(padx=17, pady=2)

total_label = tk.Label(root, text="", font=label_font, bg="azure4", fg="#000000", padx=label_padx, pady=label_pady)
total_label.pack(fill=tk.Y, expand=True)

label_3dots_desc = tk.Label(root, text="3-Dot Batteries", font=("Arial", 30), bg="#ffffff", fg="#202020")
label_3dots_desc.pack(padx=17, pady=2)

label_3dots = tk.Label(root, text="", font=label_font, bg="azure3", fg="#000000",
                       padx=label_padx, pady=label_pady)
label_3dots.pack(fill=tk.Y, expand=True)

label_2dots_desc = tk.Label(root, text="2-Dots Batteries", font=("Arial", 30), bg="#ffffff", fg="#202020")
label_2dots_desc.pack(padx=17, pady=2)

label_2dots = tk.Label(root, text="", font=label_font, bg="azure2", fg="#000000",
                      padx=label_padx, pady=label_pady)
label_2dots.pack(fill=tk.Y, expand=True)

root.configure(bg="#ffffff")


def display_results(ready_batteries_2dots, ready_batteries_3dots):
    total_label.config(text=ready_batteries_2dots + ready_batteries_3dots)
    label_3dots.config(text=ready_batteries_3dots)
    label_2dots.config(text=ready_batteries_2dots)


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

                display_results(ready_batteries_2dots, ready_batteries_3dots)
                break

        except (ConnectionError, Timeout):
            print("Connection attempt failed. Retrying...")
            time.sleep(retry_delay)
    else:
        print("Failed to establish a connection after multiple retries.")


def run_update_data():
    threading.Timer(3, run_update_data).start()
    update_data()


run_update_data()
root.mainloop()