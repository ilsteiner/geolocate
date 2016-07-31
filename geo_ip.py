import json
from urllib2 import urlopen
from geopy.geocoders import Nominatim

state_dict = dict()

with open("IP_FINAL_2", "r") as ip_file:
  ips = ip_file.readlines()
  for ip in ips:
    ip = ip.split(' ')[0]
    json_data = json.load(urlopen("http://freegeoip.net/json/" + ip))
    state_init = str(json_data["region_code"])
    state_name = str(json_data["region_name"])
    country_name = str(json_data["country_name"])
    lat = str(json_data["latitude"])
    lon = str(json_data["longitude"])
    
    current_count = 0
    
    if state_init in state_dict:
      current_count = state_dict[state_init][1]
    
    state_dict[state_init] = [state_name,current_count + 1,country_name,lat,lon]

with open("ip_counts.csv","a") as ip_output:
  ip_output.writelines("Country Name,State Code,State Name,Latitude,Longitude,Address,IP Count\n")
  
  geolocator = Nominatim()
  
  for state in state_dict:
    state_code = str(state_dict[state][1])
    state_name = str(state_dict[state][4])
    address = ''
  
    if len(state_name) == 0:
      location = geolocator.reverse(str(state_dict[state][3]),str(state_dict[state][4]))
      address = location.address
    
    ip_output.writelines(str(state_dict[state][2]) + "," + state + "," + str(state_dict[state][0]) + "," + str(state_dict[state][1]) + "," + str(state_dict[state][3]) + "," + address + "," + str(state_dict[state][4]) + "\n")
  