#Author: Ishara Harshana
#Date: 24/11/2024
#IIT Student ID: 20244040
#UoW ID: w2121271

import tkinter as tk

class TrafficDataProcessor:
    # Task A: Input Validation
    def validate_date_input(message, error_message, max_value, min_value):
        """
        Prompts the user for a date in DD MM YYYY format, validates the input for:
        - Correct data type
        - Correct range for day, month, and year
        """
        while True: # Repeat block until get the right date inputs
            try:
                while True:
                    date_input = int(input(message))
                    if date_input > max_value or date_input < min_value:
                        print(error_message)
                        continue
                    
                    str_date_input = str(date_input)
                    if len(str_date_input) == 1:
                        str_date_input = "0" + str_date_input
                        
                    return str_date_input
                    break
                break
                    
            except ValueError: # If user enters a different character instead of a number, gives this error
                print("Integer required")

    def validate_continue_input():
        """
        Prompts the user to decide whether to load another dataset:
        - Validates "Y" or "N" input
        """
        # After an output, programme ask whether user wants to continue or not 
        user_cont = input("Do you want to select another data file for a different date? Y/N > ")
        if user_cont == "N" or user_cont == "n":
            print("End of run ")
            return False       
        elif user_cont == "Y" or user_cont == "y":
            return True
        else:
            while True: # If user enter something else, below section prompts
                user_cont = input("Please enter “Y” or “N” > ")
                if user_cont == "N" or user_cont == "n":
                    print("End of run ")
                    break           
                elif user_cont == "Y" or user_cont == "y":
                    return True
                else:
                    continue
                    
    # Task B: Processed Outcomes
    def process_csv_data(file_path):
        """
        Processes the CSV data for the selected date and extracts:
        - Total vehicles
        - Total trucks
        - Total electric vehicles
        - Two-wheeled vehicles, and other requested metrics
        """
        try:
            traffic_data_list = [] # This list use to insert all the necessary traffic data.
            
            for i in range(0, 16): # Insert 16, zero values to the list (for increment purposes)
                traffic_data_list.append(0)

            # First value of the list represent csv file name
            traffic_data_list[0] = file_path
            
            # open and read the relevent csv file
            file = open(file_path, "r")
            rows = file.readlines()
            data_rows = rows[1:] # Discard the heading row
            
            # below variables store essential data required for the incrementation
            bikes_count = 0
            scooter_count = 0
            current_hour = 0
            vehicles_ph = 0
            max_vehicles_ph = 0
            max_vehicles_frm_hour = 0
            total_elm_avenue = 0

            rain_hours = 0
            rain_minutes = 0
            rain_times = list()
            previous_weather = None
            
            # Get data from csv file and assign those into the traffic_data_list
            for row in data_rows:
                # Total vehicle count
                traffic_data_list[1] += 1 

                # Seperate each csv row values
                columns = row.strip().split(',')
                
                # Truck count
                if columns[8] == 'Truck': 
                    traffic_data_list[2] += 1
                    
                # Electric vehicle count
                if columns[9] == 'True':
                    traffic_data_list[3] += 1

                # Two wheeled vehicle count
                if columns[8] == 'Bicycle' or columns[8] == 'Motorcycle' or columns[8] == 'Scooter':
                    traffic_data_list[4] += 1

                # Busses leaving Elm Avenue/Rabbit Road heading North 
                if columns[8] == 'Buss' and columns[0] == 'Elm Avenue/Rabbit Road' and columns[4] == "N":
                    traffic_data_list[5] += 1

                # Vehicles through both junctions not turning left or right
                if columns[3] == columns[4]:
                    traffic_data_list[6] += 1
                    
                # Calculate truck percentage
                truck_percent = (traffic_data_list[2] / traffic_data_list[1]) * 100
                traffic_data_list[7] = str(round(truck_percent)) + "%"
                
                # Calculate bikes per hour
                if columns[8] == 'Bicycle':
                    bikes_count += 1
                traffic_data_list[8] = int(bikes_count / 24)
                
                # High speed vehicles
                if int(columns[7]) > int(columns[6]):
                    traffic_data_list[9] += 1
                
                # Vehicles from Elm Avenue/Rabbit Road    
                if columns[0] == 'Elm Avenue/Rabbit Road':
                    traffic_data_list[10] += 1
                    
                # Vehicles from Hanley Highway/Westway
                if columns[0] == 'Hanley Highway/Westway':
                    traffic_data_list[11] += 1
                        
                # Calculate hourly data to get maximum number of vehicles per hour       
                time_parts = columns[2].split(":")
                hour = int(time_parts[0])
                minutes = int(time_parts[1])
                if hour > current_hour and columns[0] == 'Hanley Highway/Westway':
                    if vehicles_ph > max_vehicles_ph:
                        max_vehicles_ph = vehicles_ph
                        max_vehicles_frm_hour = hour
                    current_hour = hour 
                    vehicles_ph = 1 # Starting count the vehicles from next hour
                elif hour == current_hour and columns[0] == 'Hanley Highway/Westway':
                    vehicles_ph += 1
                    
                # Get the total vehicles through Elm Avenue/Rabbit Road
                if columns[0] == 'Elm Avenue/Rabbit Road':
                    total_elm_avenue += 1

                # Scooter percentage through Elm Avenue/Rabbit Road
                if columns[8] == "Scooter" and columns[0] == 'Elm Avenue/Rabbit Road':
                    scooter_count += 1
                traffic_data_list[12] = int((scooter_count/total_elm_avenue) * 100)
                    
                # Assign hourly data to relevent traffic_data_list value    
                traffic_data_list[13] = max_vehicles_ph
                traffic_data_list[14] = max_vehicles_frm_hour
            
                # Number of hours of rain calculation
                # Get all the rain hours and minutes records to a list
                if columns[5] == 'Light Rain' or columns[5] == 'Heavy Rain':
                    rain_times.append([hour, minutes])

                # Calculation section
                if columns[5] not in ('Light Rain', 'Heavy Rain') and previous_weather in ('Light Rain', 'Heavy Rain'):

                    # Convert times to total minutes since midnight
                    time_in_minutes = [(time[0] * 60 + time[1]) for time in rain_times]

                    # Find minimum and maximum times
                    min_time_minutes = min(time_in_minutes)
                    max_time_minutes = max(time_in_minutes)

                    # Calculate the range
                    range_minutes = max_time_minutes - min_time_minutes
                    range_hours = range_minutes // 60
                    range_rem_minutes = range_minutes % 60
                    rain_hours += range_hours
                    rain_minutes += range_rem_minutes
                    if rain_minutes >= 60:
                        rain_hours += 1
                        rain_minutes -= 60
                    traffic_data_list[15] = (rain_hours, rain_minutes)
                    rain_times.clear()

                previous_weather = columns[5]

            return traffic_data_list
        
        except FileNotFoundError:
            print("File directory not found")

    def display_outcomes(outcomes):
        """
        Displays the calculated outcomes in a clear and formatted way.
        """
        results = [] # This list use to insert all the traffic data in a structered way
        results.append(f"{'*'*40} \ndata file selected is {outcomes[0]} \n{'*'*40}")
        results.append(f"The total number of vehicles recorded for this date is {outcomes[1]}")
        results.append(f"The total number of trucks recorded for this date is {outcomes[2]}")
        results.append(f"The total number of electric vehicles for this date is {outcomes[3]}")
        results.append(f"The total number of two-wheeled vehicles for this date is {outcomes[4]}")
        results.append(f"The total number of Busses leaving Elm Avenue/Rabbit Road heading North is {outcomes[5]}")
        results.append(f"The total number of Vehicles through both junctions not turning left or right is {outcomes[6]}")
        results.append(f"The percentage of total vehicles recorded that are trucks for this date is {outcomes[7]}")
        results.append(f"The average number of Bikes per hour for this date is {outcomes[8]} \n")
        results.append(f"The total number of vehicles recorded as over the speed limit for this date is {outcomes[9]}")
        results.append(f"The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {outcomes[10]}")
        results.append(f"The total number of vehicles recorded through Hanley Highway/Westway junction is {outcomes[11]}")
        results.append(f"{outcomes[12]}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters. \n")
        results.append(f"The highest number of vehicles in an hour on Hanley Highway/Westway is {outcomes[13]}")
        results.append(f"The most vehicles through Hanley Highway/Westway were recorded between {outcomes[14] - 1}:00 - {outcomes[14]}:00")
        if outcomes[15] != 0:
            rain_hours, rain_minutes = outcomes[15]
            results.append(f"The number of hours of rain for this date is {rain_hours} hours and {rain_minutes} minutes \n\n")
        else:
            results.append(f"The number of hours of rain for this date is 0 \n\n")
        
        for i in results:
            print(i)
            
        return results

    # Task C: Save Results to Text File
    def save_results_to_file(outcomes, file_name="results.txt"):
        """
        Saves the processed outcomes to a text file and appends if the program loops.
        """
        file = open("results.txt", "a")
        for rows in outcomes:
            file.writelines(rows + "\n")

    # Call validate_date_input function to get user inputs and validate them.
    while True:
        day = validate_date_input(
                    "Please enter the day of the survey in the format DD: ",
                    "Out of range - value must be in the range 1 to 31.",
                    31, 1
                    )

        month = validate_date_input(
                    "Please enter the month of the survey in the format MM: ",
                    "Out of range - value must be in the range 1 to 12.",
                    12, 1
                    )

        year = validate_date_input(
                    "Please enter the year of the survey in the format YYYY: ",
                    "Out of range - value must lie in the range 2000 to 2024.",
                    2024, 2000
                    )

        # Combine variables and get the file name
        date = day + month + year # Get the date as "ddmmyyyy" format
        file_name = "traffic_data" + date + ".csv" # Get the csv file name structure

        # Call process_csv_data function to process traffic data.
        traffic_data = process_csv_data(file_name)
        if traffic_data == None:
            user_op = validate_continue_input()
            if user_op == True:
                continue
            else:
                break
            
        # Call display_outcomes function to display the outputs.
        results = display_outcomes(traffic_data)
        
        # Save results to a txt file
        save_results_to_file(results)

        # Ask for another input to continue or exit
        user_op = validate_continue_input()
        if user_op == True:
            continue
        else:
            break

class HistogramApp:
    def __init__(self, traffic_data, date):
        """
        Initializes the histogram application with the traffic data and selected date.
        """
        self.traffic_data = traffic_data
        self.date = date
        self.root = tk.Tk()
        self.canvas = None  # Will hold the canvas for drawing

    def setup_window(self):
        """
        Sets up the Tkinter window and canvas for the histogram.
        """
        self.root.title(f"Traffic Histogram for {self.date}")
        self.root.geometry("1200x480")

        # Create and pack the canvas
        self.canvas = tk.Canvas(self.root, width=1200, height=480, bg="white")
        self.canvas.pack()

    def draw_histogram(self):
        """
        Draws the histogram with axes, labels, and bars.
        """
        # Canvas dimensions
        canvas_width = 1050

        # Margins
        left_margin = 100
        bottom_margin = 400
        top_margin = 160

        # Bar properties
        bar_width = 15
        spacing = 10

        # Draw x axes
        self.canvas.create_line(left_margin, bottom_margin, canvas_width, bottom_margin)

        # Maximum value for scaling
        max_value = max(max(v) for v in self.traffic_data.values())
        scale = (bottom_margin - top_margin) / max_value

        # Draw bars and labels
        x_pos = left_margin + spacing
        for hour, (junction1, junction2) in self.traffic_data.items():
            # Bar heights
            height1 = junction1 * scale
            height2 = junction2 * scale

            # Draw junction 1 bar and vehicle count
            self.canvas.create_rectangle(x_pos, bottom_margin - height1, x_pos + bar_width, bottom_margin, fill="#9ff698")
            self.canvas.create_text(x_pos + bar_width / 2, bottom_margin - height1 - 8, text=junction1, font=("Arial", 8, "bold"), fill="#7ab479")
            
            # Draw junction 2 bar and vehicle count
            self.canvas.create_rectangle(x_pos + bar_width, bottom_margin - height2, x_pos + 2 * bar_width, bottom_margin, fill="#f39998")
            self.canvas.create_text(x_pos + 3 * bar_width / 2, bottom_margin - height2 - 8, text=junction2, font=("Arial", 8, "bold"), fill="#b87163")

            # Add hour label
            self.canvas.create_text(x_pos + bar_width, bottom_margin + 10, text=hour)

            # Move x position
            x_pos += 2 * bar_width + spacing

    def add_legend(self):
        """
        Adds a legend to the histogram to indicate which bar corresponds to which junction.
        """
        # Add hour label
        self.canvas.create_text(110, 30, text=f"Histogram of Vehicle Frequency per Hour ({self.date})", anchor="w", font=("Arial", 14, "bold"))
        
        self.canvas.create_rectangle(110, 50, 130, 70, fill="#9ff698")
        self.canvas.create_text(140, 60, text="Elm Avenue/Rabbit Road", anchor="w")

        self.canvas.create_rectangle(110, 80, 130, 100, fill="#f39998")
        self.canvas.create_text(140, 90, text="Hanley Highway/Westway", anchor="w")

        self.canvas.create_text(550, 450, text="Hours 00:00 to 24:00", anchor="w", font=("Arial", 10))

    def run(self):
        """
        Runs the Tkinter main loop to display the histogram.
        """
        self.setup_window()
        self.draw_histogram()
        self.add_legend()
        self.root.mainloop()


# Task E: Code Loops to Handle Multiple CSV Files
class MultiCSVProcessor:
    def __init__(self):
        """
        Initializes the application for processing multiple CSV files.
        """
        self.current_data = None

    def load_csv_file(self, file_path):
        """
        Loads a CSV file and processes its data.
        """
        try:
            file = open(file_path, "r")
            rows = file.readlines()
            data_rows = rows[1:] # Discard the heading row

            self.current_data = {}
            elm_avenue = 0
            westway = 0
            hour = -1  # Initialize to an invalid hour

            # Get data from csv file and assign those into the self.current_data
            for row in data_rows:
                columns = row.strip().split(',')             
                time_parts = columns[2].split(":")
                current_hour = int(time_parts[0])
                
                if current_hour != hour:
                    if hour != -1:  # Save the previous hour's data
                        self.current_data[hour] = [elm_avenue, westway]
                    hour = current_hour
                    elm_avenue = 0
                    westway = 0
                
                junction = columns[0]
                if junction == "Elm Avenue/Rabbit Road":
                    elm_avenue += 1
                elif junction == "Hanley Highway/Westway":
                    westway += 1

            # Add the last hour's data
            if hour != -1:
                self.current_data[hour] = [elm_avenue, westway]

            app = HistogramApp(self.current_data, f"{self.day}/{self.month}/{self.year}")
            app.run()

        except FileNotFoundError:
            print("File directory not found")

    def clear_previous_data(self):
        """
        Clears data from the previous run to process a new dataset.
        """
        self.current_data = None
        # After an output, programme ask whether user wants to continue or not 
        while True:
            user_cont = input("Do you want to select another data file for a different date? Y/N > ")
            if user_cont == "N" or user_cont == "n":
                print("End of run ")
                return False       
            elif user_cont == "Y" or user_cont == "y":
                return True
            else:
                while True: # If user enter something else, below section prompts
                    user_cont = input("Please enter “Y” or “N” > ")
                    if user_cont == "N" or user_cont == "n":
                        print("End of run ")
                        return False           
                    elif user_cont == "Y" or user_cont == "y":
                        return True
                    else:
                        continue

    def handle_user_interaction(self, message, error_message, max_value, min_value):
        """
        Handles user input for processing multiple files.
        """
        while True: # Repeat block until get the right date inputs
            try:
                while True:
                    date_input = int(input(message))
                    if date_input > max_value or date_input < min_value:
                        print(error_message)
                        continue
                    
                    str_date_input = str(date_input)
                    if len(str_date_input) == 1:
                        str_date_input = "0" + str_date_input
                        
                    return str_date_input
                    
            except ValueError: # If user enters a different character instead of a number, gives this error
                print("Integer required")

    def process_files(self):
        """
        Main loop for handling multiple CSV files until the user decides to quit.
        """
        # Call handle_user_interaction function to get user inputs and validate them.
        while True:
            self.day = self.handle_user_interaction(
                        "Please enter the day of the survey in the format DD: ",
                        "Out of range - value must be in the range 1 to 31.",
                        31, 1
                        )

            self.month = self.handle_user_interaction(
                        "Please enter the month of the survey in the format MM: ",
                        "Out of range - value must be in the range 1 to 12.",
                        12, 1
                        )

            self.year = self.handle_user_interaction(
                        "Please enter the year of the survey in the format YYYY: ",
                        "Out of range - value must lie in the range 2000 to 2024.",
                        2024, 2000
                        )

            # Combine variables and get the file name
            date = self.day + self.month + self.year # Get the date as "ddmmyyyy" format
            file_name = "traffic_data" + date + ".csv" # Get the csv file name structure

            # Call load_csv_file function to process traffic data.
            self.load_csv_file(file_name)
            if self.current_data  == None:
                user_op = self.clear_previous_data()
                if user_op == True:
                    continue
                else:
                    break             

            # Ask for another input to continue or exit
            user_op = self.clear_previous_data()
            if user_op == False:
                break
            else:
                continue


app = MultiCSVProcessor()
app.process_files()