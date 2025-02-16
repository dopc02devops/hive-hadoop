import json

# Path to your input JSON file containing an array of objects
input_file_path = './image_data.json'

# Path to your output file (where the one-object-per-line file will be saved)
output_file_path = 'sample-files/image_data.json'

# Open the input file and load the JSON data
with open(input_file_path, 'r') as infile:
    data = json.load(infile)  # Load the entire JSON array

# Open the output file in write mode
with open(output_file_path, 'w') as outfile:
    # Loop through each object in the JSON array and write each to a new line
    for item in data:
        json.dump(item, outfile)
        outfile.write('\n')  # Write each JSON object on a new line
