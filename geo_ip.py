import json
from urllib2 import urlopen
import argparse

state_dict = dict()

parser = argparse.ArgumentParser(description='Geolocate IP addresses from a file')

input_file = "IP_FINAL_2"
output_file = "ip_count.csv"

parser.add_argument("-i", "--input", help="the file to use for input, should contain one IP address per line, defaults to " + input_file)
parser.add_argument("-o", "--output", help="the file to use for output, will be overwritten if it exists and created if it doesn't, defaults to " + output_file)
parser.add_argument("-v", "--verbosity", help="increase verbosity for each flag instance", action="count", default=0)

args = parser.parse_args()


if args.input:
    input_file = args.input

if args.output:
    output_file = args.output

with open(output_file,"w") as ip_output:
    if args.verbosity >= 3:
        print "Clearing output file..."
    pass

try:
    with open(input_file) as ip_file:
      for ip in ip_file:
        ip = ip.split(' ')[0]

        if args.verbosity >=3:
            print "Looking up " + str(ip)

        json_data = json.load(urlopen("http://freegeoip.net/json/" + ip))
        state_init = str(json_data["region_code"])
        state_name = str(json_data["region_name"])
        country_name = str(json_data["country_name"])
        city_name = unicode(json_data["city"])
        lat = str(json_data["latitude"])
        lon = str(json_data["longitude"])

        if args.verbosity >=2:
            print str(ip) + " is located at " + lat + ", " + lon
        
        current_count = 0

        if len(city_name) == 0 or len(state_init) == 0:
            if args.verbosity >= 2:
                print "No address found for " + str(ip) + ", Googling..."
            geo_locate = json.load(urlopen("https://maps.googleapis.com/maps/api/geocode/json?latlng=" + lat + "," + lon + "&result_type=political&key=AIzaSyDhM6ZjGswVPyIEX59f14eNYrLRDm928lQ"))

            for item in geo_locate["results"][0]["address_components"]:
                if args.verbosity >= 3:
                    print "Googling..."
                if "administrative_area_level_1" in item["types"]:
                    state_init = item["short_name"]
                    state_name = item["long_name"]
                if "locality" in item["types"]:
                    city_name = item["long_name"]

            # It's still empty
            if len(city_name) == 0:
                if args.verbosity >=2:
                    print "No city found for " + str(ip) + ", using neighborhood instead"
                for item in geo_locate["results"][0]["address_components"]:
                    if "administrative_area_level_3" in item["types"]:
                        city_name = item["long_name"]

            if len(city_name) == 0:
                if args.verbosity >= 1:
                    print "No city found for " + str(ip) + " at " + lat + ", " + lon + ", giving up"

        if state_init in state_dict:
          if args.verbosity >= 3:
            print "Incrementing count for " + city_name
          current_count = state_dict[state_init]["count"]
        
        state_dict[state_init] = {"city_name": city_name, "state_name": state_name,"state_code": state_init,"country_name": country_name,"count": current_count + 1}

    with open(output_file,"a") as ip_output:
        if args.verbosity >= 1:
            print "Geolocation complete, building output"

        output_title = ""

        for item in state_dict.items()[0][1].keys():
            output_title = output_title + item + ","

        output_title = output_title[:-1] + "\n"

        ip_output.writelines(output_title)
      
        for state in state_dict:
            # if args.verbosity >= 3:
                # print "Writing count (" + str(city_dict[city]["count"]) +  ") for " + city + ", " + city_dict[city]["state_name"]
            output_string = ""
            for item in state_dict[state]:
                output_string = output_string + unicode(state_dict[state][item]) + ","

            output_string = output_string[:-1] + "\n"

            ip_output.writelines(output_string.encode("UTF-8"))

    if args.verbosity >= 1:
        print "Processing complete, output stored in " + output_file

except EnvironmentError:
    print "Program terminated. Make sure the input file (" + input_file +  ") is valid."