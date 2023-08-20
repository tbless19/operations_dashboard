document.addEventListener('DOMContentLoaded', function () {
        // Clock
    function showTime() {
      let time = new Date();
      let hour = time.getHours();
      let min = time.getMinutes();
      let sec = time.getSeconds();
      let am_pm = "AM";
  
      if (hour > 12) {
        hour -= 12;
        am_pm = "PM";
      }
      if (hour == 0) {
        hour = 12;
        am_pm = "AM";
      }
  
      hour = hour < 10 ? "0" + hour : hour;
      min = min < 10 ? "0" + min : min;
      sec = sec < 10 ? "0" + sec : sec;
  
      let currentTime = hour + ":" + min + ":" + sec + " " + am_pm;
  
      document.getElementById("clock").innerHTML = currentTime;
    }
  
    setInterval(showTime, 1000);
    
    // Data update
    function getData() {
      fetch('/data')
        .then(response => response.json())
        .then(data => {
          document.getElementById('flight-count-number').textContent = data.flights;
          document.getElementById('average-time-value').textContent = data.avg_time;
          document.getElementById('inbound-value').textContent = data.num_inbound;
          document.getElementById('outbound-value').textContent = data.num_outbound;
          document.getElementById('available-zips-value').textContent = data.available_zips;
        })
        .catch(error => console.error('Error:', error))
        .finally(() => {
          setTimeout(getData, 6000);
        });
    }
  
    getData();
  
    // Flight frequency
    let states = { '674': 3, '657': 5, '660': 3, '650': 3 };
  
    let flightFrequency = document.getElementById("flight_frequency");
  
    for (let zip in states) {
      let wrapper = document.createElement("div");
      wrapper.className = "flight_frequency_box";
  
      let zipNumber = document.createElement("h4");
      zipNumber.textContent = zip;
  
      let zipFreq = document.createElement("h4");
      zipFreq.textContent = states[zip];
  
      wrapper.appendChild(zipNumber);
      wrapper.appendChild(zipFreq);
  
      flightFrequency.appendChild(wrapper);
    }
  });
  