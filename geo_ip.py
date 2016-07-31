import json
from urllib2 import urlopen

max_bytes = 10

city_dict = dict()

with open("ip_counts.csv","w") as ip_output:
    pass

with open("IP_FINAL_2", "r") as ip_file:
  ips = ip_file.readlines(max_bytes)
  for ip in ips:
    ip = ip.split(' ')[0]
    json_data = json.load(urlopen("http://freegeoip.net/json/" + ip))
    state_init = str(json_data["region_code"])
    state_name = str(json_data["region_name"])
    country_name = str(json_data["country_name"])
    city_name = str(json_data["city"])
    lat = str(json_data["latitude"])
    lon = str(json_data["longitude"])
    
    current_count = 0

    if len(city_name) == 0 or len(state_init) == 0:
        geo_locate = json.load(urlopen("https://maps.googleapis.com/maps/api/geocode/json?latlng=" + lat + "," + lon + "&result_type=political&key=AIzaSyDhM6ZjGswVPyIEX59f14eNYrLRDm928lQ"))

        for item in geo_locate["results"][0]["address_components"]:
            if "administrative_area_level_1" in item["types"]:
                state_init = item["short_name"]
                state_name = item["long_name"]
            if "locality" in item["types"]:
                city_name = item["long_name"]

        # It's still empty
        if len(city_name) == 0:
            for item in geo_locate["results"][0]["address_components"]:
                if "administrative_area_level_3" in item["types"]:
                    city_name = item["long_name"]

        if len(city_name) == 0:
            print lat + "," + lon

    if city_name in city_dict:
      current_count = city_dict[city_name]["count"]
    
    city_dict[city_name] = {"city_name": city_name, "state_name": state_name,"state_code": state_init,"country_name": country_name,"count": current_count + 1}

with open("ip_counts.csv","a") as ip_output:
    # ip_output.writelines("Country Name,State Code,State Name,Latitude,Longitude,IP Count\n")

    output_title = ""

    for item in city_dict.items()[0][1].keys():
        output_title = output_title + item + ","

    output_title = output_title[:-1] + "\n"

    ip_output.writelines(output_title)
  
    for city in city_dict:
        output_string = ""
        for item in city_dict[city]:
            output_string = output_string + str(city_dict[city][item]) + ","

        output_string = output_string[:-1] + "\n"

        ip_output.writelines(output_string)
  