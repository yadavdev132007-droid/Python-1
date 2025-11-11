# tracker.py
# Name: [Dev Yadav]
# Date: November 8, 2025
# Project Title: Daily Calorie Tracker CLI

import datetime # Used for the timestamp in the log file

# --- Task 1: Setup & Introduction ---
def welcome_message():
    """Prints a welcome message and introduction to the tool."""
    print("==================================================")
    print("         🥗 Daily Calorie Tracker CLI 📊         ")
    print("==================================================")
    print("Welcome! This tool helps you quickly log your meals,")
    print("track total calories consumed, and check against your")
    print("personal daily limit.")
    print("---")

# --- Global Data Structures ---
meal_names = []
calorie_amounts = []
daily_limit = 0.0

def get_user_input():
    """Handles Task 2: Input & Data Collection."""
    global daily_limit
    
    # Get daily limit first
    while True:
        try:
            limit_input = input("Enter your **Daily Calorie Limit (e.g., 2000)**: ")
            daily_limit = float(limit_input)
            if daily_limit <= 0:
                 print("Limit must be a positive number. Please try again.")
                 continue
            break
        except ValueError:
            print("Invalid input. Please enter a numerical value for your limit.")
            
    # Get number of meals
    num_meals = 0
    while True:
        try:
            num_meals_input = input("How many meals/items do you want to enter today? ")
            num_meals = int(num_meals_input)
            if num_meals < 0:
                print("The number of meals cannot be negative. Please try again.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")
            
    # Loop for meal input
    print("\n--- Start Logging Meals ---")
    for i in range(1, num_meals + 1):
        meal_name = input(f"Enter Meal #{i} Name (e.g., Breakfast, Snack, Dinner): ")
        
        while True:
            try:
                calorie_input = input(f"Enter Calories for **{meal_name}**: ")
                calories = float(calorie_input)
                if calories < 0:
                    print("Calorie amount cannot be negative. Please try again.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a numerical value for calories.")
                
        meal_names.append(meal_name)
        calorie_amounts.append(calories)
        print("Logged successfully.")
    
    if not meal_names:
        print("\nNo meals logged. Exiting tracker.")
        return False # Indicate that no data was entered
    return True # Indicate that data was entered

def calculate_summary():
    """Handles Task 3: Calorie Calculations."""
    # Total Calorie Intake (Task 3)
    total_calories = sum(calorie_amounts) 
    
    # Average Calorie Per Meal (Task 3)
    # Avoid ZeroDivisionError if no meals were logged (though handled in get_user_input)
    average_calories = total_calories / len(calorie_amounts) if calorie_amounts else 0
    
    return total_calories, average_calories

def generate_report(total_calories, average_calories):
    """
    Handles Task 4: Exceed Limit Warning System and 
    Task 5: Neatly Formatted Output.
    """
    global daily_limit
    
    # --- Task 5: Neatly Formatted Output ---
    report = "\n"
    report += "📊 Daily Calorie Intake Summary\n"
    report += "--------------------------------------------------\n"
    report += f"| {'Meal Name':<20} | {'Calories (kcal)':>15} |\n"
    report += "--------------------------------------------------\n"
    
    # List all logged meals
    for name, cal in zip(meal_names, calorie_amounts):
        # Using f-string for formatting and alignment
        report += f"| {name:<20} | {cal:>15.2f} |\n" 

    report += "--------------------------------------------------\n"
    report += f"| {'TOTAL INTAKE':<20} | {total_calories:>15.2f} |\n"
    
    # Formatting average to two decimal places
    report += f"| {'AVERAGE PER MEAL':<20} | {average_calories:>15.2f} |\n"
    report += "--------------------------------------------------\n"
    
    # --- Task 4: Exceed Limit Warning System ---
    
    # Compare against daily limit (Task 3 & 4)
    status_message = ""
    if total_calories > daily_limit:
        excess = total_calories - daily_limit
        # Task 4: Warning Message
        status_message = f"🚨 WARNING! You have **exceeded** your limit of {daily_limit:.2f} kcal by {excess:.2f} kcal."
        status = "EXCEEDED LIMIT"
    else:
        remaining = daily_limit - total_calories
        # Task 4: Success Message
        status_message = f"✅ SUCCESS! You are **within** your limit of {daily_limit:.2f} kcal. You have {remaining:.2f} kcal remaining."
        status = "WITHIN LIMIT"
        
    report += f"\nYour Daily Limit: {daily_limit:.2f} kcal\n"
    report += status_message
    report += "\n--------------------------------------------------\n"
    
    print(report)
    return report, status # Return the report text and status for saving

def save_log(report_text, status):
    """Handles Task 6 (Bonus): Save Session Log to File."""
    while True:
        save_choice = input("\nDo you want to save this session log to a file? (yes/no): ").lower()
        if save_choice in ['yes', 'y']:
            filename = "calorie_log.txt"
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Prepare the header information
            log_header = f"*** Calorie Tracker Session Log ***\n"
            log_header += f"Date & Time: {current_time}\n"
            log_header += f"Daily Calorie Limit: {daily_limit:.2f} kcal\n"
            log_header += f"Limit Status: {status}\n"
            log_header += "-----------------------------------\n"
            
            # open("filename.txt", "w") - 'w' mode overwrites the file
            try:
                with open(filename, "w") as f:
                    f.write(log_header)
                    f.write(report_text)
                print(f"🎉 Session log saved successfully to **{filename}**")
            except Exception as e:
                print(f"An error occurred while saving the file: {e}")
            break
        elif save_choice in ['no', 'n']:
            print("Session log not saved. Thank you for using the tracker!")
            break
        else:
            print("Invalid choice. Please enter 'yes' or 'no'.")


# --- Main Execution Block ---
if __name__ == "__main__":
    welcome_message()
    
    # Task 2: Get Input
    if get_user_input():
        # Task 3: Calculate Summary
        total_cal, avg_cal = calculate_summary()
        
        # Task 4 & 5: Generate and Print Report
        report, status = generate_report(total_cal, avg_cal)
        
        # Task 6 (Bonus): Save Log
        save_log(report, status)
    else:
        # Exit gracefully if no meals were logged
        pass
    
    print("\n==================================================")
    print("           Calorie Tracker Closed.              ")

    print("==================================================")
