import re

# Open the log file
with open('logger/2025.06.18.log', 'r') as f:
    log_data = f.read()

# Regular expression pattern to match the image prediction results
pattern = r"Image Prediction Result : \[{'name': 'customer_on', 'class': 1, 'confidence': (\d+\.\d+), 'box': {'x1': (\d+\.\d+), 'y1': (\d+\.\d+), 'x2': (\d+\.\d+), 'y2': (\d+\.\d+)}}\]"

# Regular expression pattern to match the file name
file_pattern = r"--- Processing image \d+/\d+: (.+)"

# Find all matches
matches = re.findall(pattern, log_data)
file_matches = re.findall(file_pattern, log_data)

# Initialize min and max values and corresponding file names
x1_min = float('inf')
x1_max = float('-inf')
x1_min_file = None
x1_max_file = None
y1_min = float('inf')
y1_max = float('-inf')
y1_min_file = None
y1_max_file = None
x2_min = float('inf')
x2_max = float('-inf')
x2_min_file = None
x2_max_file = None
y2_min = float('inf')
y2_max = float('-inf')
y2_min_file = None
y2_max_file = None

# Iterate over matches
for i, match in enumerate(matches):
    confidence = float(match[0])
    if confidence > 0.9:
        x1 = float(match[1])
        y1 = float(match[2])
        x2 = float(match[3])
        y2 = float(match[4])
        file_name = file_matches[i]
        if x1 < x1_min:
            x1_min = x1
            x1_min_file = file_name
        if x1 > x1_max:
            x1_max = x1
            x1_max_file = file_name
        if y1 < y1_min:
            y1_min = y1
            y1_min_file = file_name
        if y1 > y1_max:
            y1_max = y1
            y1_max_file = file_name
        if x2 < x2_min:
            x2_min = x2
            x2_min_file = file_name
        if x2 > x2_max:
            x2_max = x2
            x2_max_file = file_name
        if y2 < y2_min:
            y2_min = y2
            y2_min_file = file_name
        if y2 > y2_max:
            y2_max = y2
            y2_max_file = file_name

# Print ranges and corresponding file names
if matches:
    print("Ranges and corresponding file names:")
    print(f"x1: [{x1_min} ({x1_min_file}), {x1_max} ({x1_max_file})]")
    print(f"y1: [{y1_min} ({y1_min_file}), {y1_max} ({y1_max_file})]")
    print(f"x2: [{x2_min} ({x2_min_file}), {x2_max} ({x2_max_file})]")
    print(f"y2: [{y2_min} ({y2_min_file}), {y2_max} ({y2_max_file})]")
else:
    print("No matches found with confidence > 0.7")