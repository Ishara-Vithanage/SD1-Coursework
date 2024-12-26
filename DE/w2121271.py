#Author: Ishara Harshana
#Date: 11/12/2024
#IIT Student ID: 20244040
#UoW ID: w2121271

import tkinter as tk

# Task D: Histogram Display
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
        
        # Add legend for junction 1
        self.canvas.create_rectangle(110, 50, 130, 70, fill="#9ff698")
        self.canvas.create_text(140, 60, text="Elm Avenue/Rabbit Road", anchor="w")

        # Add legend for junction 2
        self.canvas.create_rectangle(110, 80, 130, 100, fill="#f39998")
        self.canvas.create_text(140, 90, text="Hanley Highway/Westway", anchor="w")

        # Define x axes
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

            # Add the previous hour's data
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