import csv
import matplotlib.pyplot as plt
import numpy as np
import geojson 
import parse 

from geojson import dumps
from collections import Counter

My_file = "path/Data.csv"

#Parses a raw CSV file to a JSON-line object#
#1.Open the raw file.
#2.Read the CSV file with the appropriate delimiter, then close the file.
#3.Initialize an empty list which will be returned by the function.
#4.Grab the first row of the CSV file, the headers/column names, and assign them to the fields variable, which will be a list.
#5.Iterate over each remaining row in the CSV file, mapping column headers → row values, and add to our list we initialized in step 3.
#6.Return the parsed_data variable
def parse(raw_file, delimiter): 
    #opening and reading the file
    opened_file = open(raw_file)
    csv_data = csv.reader(opened_file, delimiter=delimiter)
    #decaring a parsed data
    parsed_data = []
    #to save the header in the fields by using the next() in-built function
    fields = next(csv_data)
    #to add dictionary to map the fields to the values in csv file
    #Python’s built-in zip() function to zip together header → value to make our dictionary of every row.
    for row in csv_data:
        parsed_data.append(dict(zip(fields, row)))  
    #to close the opened file
    opened_file.close()
    return parsed_data



#Visualize data by day of week in a line graph
def visualize_days():
    #grab our parsed data that we parsed earlier
    data_file = parse(My_file, ",")
    #make a new variable 'counter', from iterating through each line of data in the parsed data, and count how many incidents
    #happen on each day
    #iterate every dictionary value of every dictionary key set to ‘DayOfWeek’ for every line item in data_file
    counter = Counter(item["DayOfWeek"] for item in data_file)
    data_list = [
                 counter["Monday"],
                 counter["Tuesday"],
                 counter["Wednesday"],
                 counter["Thursday"],
                 counter["Friday"],
                 counter["Saturday"],
                 counter["Sunday"]
                 ]
    day_tuple = tuple(["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"])
    #plotting the values on the y-axis and x-axis respectively
    plt.plot(data_list)
    plt.xticks(range(len(day_tuple)), day_tuple)
    #plt.show()
    #save the plot in the working directory
    plt.savefig("Days.png")
    #close fig
    plt.clf()

    
    
#Visualize data by category in a bar graph
def visualize_type():
    data_file = parse(My_file,",")
    counter = Counter(items["Category"] for items in data_file)
    
    labels = tuple(counter.keys())
    xlocations = np.arange(len(labels)) + 0.5
    width = 0.5
    
    plt.bar(xlocations, counter.values(), width=width)
    
    #to give the lables on x-axis
    plt.xticks(xlocations + width/2 , labels, rotation = 90)
    # Give some more room so the labels aren't cut off in the graph
    plt.subplots_adjust(bottom=0.4)
    # Make the overall graph/figure larger
    plt.rcParams['figure.figsize'] = 12, 8
    #plt.show()
    #save the graph
    plt.savefig("Category.png")
    #close fig
    plt.clf()

    
#plotting the time     
def visualize_time():
    data_file = parse(My_file,",")
    counter = Counter(item["Time"] for item in data_file)
    labels = list(counter.keys())
    xlocations = np.arange(len(labels))
    width = 0.5
       
    #plotting the graph
    plt.bar(xlocations, counter.values(), width=width, color = 'r')
    #plotting the line
    plt.plot(list(counter.values()))
    plt.xticks(xlocations+width/2,labels,rotation = 90)
    plt.subplots_adjust(bottom=0.5)
    #plt.show()
    plt.savefig("time.png")
    plt.clf()
    
#plotting the map
def create_map(data_file):
    ###Creates a GeoJSON file.
    #Returns a GeoJSON file that can be rendered in a GitHub
    #Gist at gist.github.com.  Just copy the output file and
    #paste into a new Gist, then create either a public or
    #private gist.  GitHub will automatically render the GeoJSON
    #file as a map.###

    # Define type of GeoJSON we're creating
    geo_map = {"type": "FeatureCollection"}

    # Define empty list to collect each point to graph
    item_list = []

    # Iterate over our data to create GeoJSOn document.
    # We're using enumerate() so we get the line, as well
    # the index, which is the line number.
    for index, line in enumerate(data_file):

        # Skip any zero coordinates as this will throw off
        # our map.
        if line['X'] == "0" or line['Y'] == "0":
            continue

        # Setup a new dictionary for each iteration.
        data = {}

        # Assign line items to appropriate GeoJSON fields.
        data['type'] = 'Feature'
        data['id'] = index
        data['properties'] = {'title': line['Category'],
                              'description': line['Descript'],
                              'date': line['Date']}
        data['geometry'] = {'type': 'Point',
                            'coordinates': (line['X'], line['Y'])}

        # Add data dictionary to our item_list
        item_list.append(data)

    # For each point in our item_list, we add the point to our
    # dictionary.  setdefault creates a key called 'features' that
    # has a value type of an empty list.  With each iteration, we
    # are appending our point to that list.
    for point in item_list:
        geo_map.setdefault('features', []).append(point)

    # Now that all data is parsed in GeoJSON write to a file so we
    # can upload it to gist.github.com
    with open('file_sf.geojson', 'w') as f:
        f.write(geojson.dumps(geo_map))

        

def main():
    # Call our parse function and give it the needed parameters
    #new_data = parse(My_file, ",")
    # Let's see what the data looks like!
    #print (type(new_data).__name__)
    #print (new_data[1])
    #visualize_days()
    #visualize_type()
    #visualize_time()
    data = parse(My_file, ",")

    return create_map(data)

if __name__ == "__main__":
    main()