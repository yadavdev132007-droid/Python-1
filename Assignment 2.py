## 📚 GradeBook Analyzer CLI
#
# Author: [Dev Yadav]
# Date: November 8, 2025 (or current date)
# Title: Analysing and Reporting Student Grades

import csv
import statistics
from typing import Dict, List, Tuple

# --- Global Constants ---
# Define the passing score threshold
PASS_THRESHOLD = 40

# --- Task 3: Statistical Analysis Functions ---

def calculate_average(marks_dict: Dict[str, int]) -> float:
    """Calculates the mean (average) score."""
    if not marks_dict:
        return 0.0
    return sum(marks_dict.values()) / len(marks_dict)

def calculate_median(marks_dict: Dict[str, int]) -> float:
    """Calculates the median score."""
    if not marks_dict:
        return 0.0
    # The 'statistics' module handles the calculation correctly for even/odd counts
    return statistics.median(marks_dict.values())

def find_max_score(marks_dict: Dict[str, int]) -> Tuple[str, int]:
    """Finds the name and score of the student with the highest mark."""
    if not marks_dict:
        return ("N/A", 0)
    
    # Use max() with a key to find the key (name) corresponding to the max value (score)
    max_name = max(marks_dict, key=marks_dict.get)
    return (max_name, marks_dict[max_name])

def find_min_score(marks_dict: Dict[str, int]) -> Tuple[str, int]:
    """Finds the name and score of the student with the lowest mark."""
    if not marks_dict:
        return ("N/A", 0)

    # Use min() with a key to find the key (name) corresponding to the min value (score)
    min_name = min(marks_dict, key=marks_dict.get)
    return (min_name, marks_dict[min_name])

# --- Task 4: Grade Assignment and Distribution ---

def assign_grades(marks_dict: Dict[str, int]) -> Tuple[Dict[str, str], Dict[str, int]]:
    """
    Assigns letter grades based on scores and calculates the grade distribution.
    A: 90+, B: 80-89, C: 70-79, D: 60-69, F: <60
    """
    grades_dict = {}
    distribution = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}

    for name, score in marks_dict.items():
        if score >= 90:
            grade = "A"
        elif score >= 80:
            grade = "B"
        elif score >= 70:
            grade = "C"
        elif score >= 60:
            grade = "D"
        else:
            grade = "F"
        
        grades_dict[name] = grade
        distribution[grade] += 1
        
    return grades_dict, distribution

# --- Task 2: Data Entry or CSV Import Functions ---

def manual_entry() -> Dict[str, int]:
    """Allows manual input of student names and marks."""
    print("\n--- Manual Data Entry ---")
    marks = {}
    while True:
        name = input("Enter student name (or 'done' to finish): ").strip()
        if name.lower() == 'done':
            break
        
        while True:
            try:
                score = int(input(f"Enter mark for {name}: ").strip())
                if 0 <= score <= 100:
                    marks[name] = score
                    break
                else:
                    print("Score must be between 0 and 100.")
            except ValueError:
                print("Invalid input. Please enter a whole number for the score.")
                
    return marks

def import_csv_data() -> Dict[str, int]:
    """Loads student names and marks from a CSV file."""
    print("\n--- CSV Data Import ---")
    file_path = input("Enter the path to the CSV file (e.g., 'grades.csv'): ").strip()
    marks = {}
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            
            # Assuming the CSV has two columns: [Name, Mark] and may have a header row
            try:
                # Attempt to skip header if the first row doesn't look like data
                first_row = next(reader)
                
                # Simple heuristic: if the first item is not all digits and the second is, 
                # or if the first item is 'Name' or 'Student', assume it's a header
                is_header = not (first_row[0].strip().isdigit()) and (first_row[1].strip().isdigit() or first_row[1].lower() in ['mark', 'score'])
                
                if not is_header:
                    # If it wasn't a header, process the first row as data
                    try:
                        name, mark_str = first_row
                        marks[name.strip()] = int(mark_str.strip())
                    except (ValueError, IndexError):
                        print(f"Warning: Skipping malformed first row: {first_row}")
                
            except StopIteration:
                print("The CSV file is empty.")
                return {} # Return empty dict if file is empty

            # Process remaining rows
            for row in reader:
                try:
                    name, mark_str = row[0], row[1]
                    marks[name.strip()] = int(mark_str.strip())
                except (ValueError, IndexError):
                    print(f"Warning: Skipping malformed row: {row}")

        print(f"Successfully loaded {len(marks)} student records.")
        return marks
    
    except FileNotFoundError:
        print(f"Error: File not found at path: {file_path}")
        return {}
    except Exception as e:
        print(f"An error occurred during CSV import: {e}")
        return {}

# --- Analysis and Reporting (Integrating Tasks 3-6) ---

def run_analysis(marks: Dict[str, int]):
    """Performs all analysis and prints the summary reports."""
    if not marks:
        print("\n❌ No student data available to analyze.")
        return

    # 1. Statistical Analysis (Task 3)
    print("\n" + "="*50)
    print("📊 Analysis Summary")
    print("="*50)
    
    avg = calculate_average(marks)
    median = calculate_median(marks)
    max_name, max_score = find_max_score(marks)
    min_name, min_score = find_min_score(marks)

    print(f"Total Students: {len(marks)}")
    print(f"Mean Score: {avg:.2f}")
    print(f"Median Score: {median:.2f}")
    print(f"Max Score: {max_score} (Student: {max_name})")
    print(f"Min Score: {min_score} (Student: {min_name})")
    print("="*50)

    # 2. Grade Assignment and Distribution (Task 4)
    grades, distribution = assign_grades(marks)
    
    print("\n⭐ Grade Distribution Summary")
    print("-" * 30)
    total_students = len(marks)
    for grade, count in distribution.items():
        percentage = (count / total_students) * 100 if total_students > 0 else 0
        print(f"Grade {grade}: {count:2} students ({percentage:.1f}%)")
    print("-" * 30)
    
    # 3. Pass/Fail Filter (Task 5)
    # List Comprehension for conditional filtering
    passed_students: List[Tuple[str, int]] = [(name, score) for name, score in marks.items() if score >= PASS_THRESHOLD]
    failed_students: List[Tuple[str, int]] = [(name, score) for name, score in marks.items() if score < PASS_THRESHOLD]

    print(f"\n✅ Pass/Fail Analysis (Pass Threshold: {PASS_THRESHOLD})")
    print("-" * 30)
    print(f"PASSED Students: {len(passed_students)}")
    if passed_students:
        print("   " + ", ".join([f"{name} ({score})" for name, score in passed_students]))

    print(f"\n❌ FAILED Students: {len(failed_students)}")
    if failed_students:
        print("   " + ", ".join([f"{name} ({score})" for name, score in failed_students]))
    print("-" * 30)

    # 4. Results Table (Task 6)
    print("\n📚 Full Grade Report Table")
    print("-" * 30)
    # Using f-strings and alignment for a clean table
    print(f"{'Name':<15}{'Marks':>5}{'Grade':>8}")
    print("-" * 30)
    
    # Sort by score descending for better readability
    sorted_marks = sorted(marks.items(), key=lambda item: item[1], reverse=True)
    
    for name, score in sorted_marks:
        grade = grades[name]
        # Use f-string alignment: < (left-align), > (right-align)
        print(f"{name:<15}{score:>5}{grade:>8}")
        
    print("-" * 30)


# --- Task 1 & Task 6: CLI and Main Loop ---

def main():
    """Main function to run the GradeBook Analyzer CLI."""
    # Task 1: Welcome Message and Menu
    print("="*50)
    print("    💻 GradeBook Analyzer CLI v1.0")
    print("="*50)
    
    marks_data: Dict[str, int] = {}
    
    # Task 6: Main menu loop for repeated analysis
    while True:
        print("\n--- Main Menu ---")
        print("1. Enter marks manually")
        print("2. Import marks from CSV file")
        print("3. Run analysis on loaded data")
        print("4. Clear current data")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == '1':
            marks_data = manual_entry()
        
        elif choice == '2':
            marks_data = import_csv_data()
            
        elif choice == '3':
            run_analysis(marks_data)
            
        elif choice == '4':
            marks_data = {}
            print("\n🗑️ Data cleared.")

        elif choice == '5':
            print("\n👋 Thank you for using the GradeBook Analyzer. Goodbye!")
            break
            
        else:
            print("❗ Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()

# --- Example CSV File Structure (For testing purposes) ---
# Create a file named 'grades.csv' with the following content:
# Name,Mark
# Alice,78
# Bob,92
# Charlie,65
# David,55
# Eve,81
# Frank,90
# Grace,45
# Hannah,72
# Ivan,30

# Julie,60
