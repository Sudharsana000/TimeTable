import random

# Define the input parameters
working_days = 5
hours_per_day = 7
lab_courses = ['C lab', 'DS lab', 'MAD lab']
occurrence_per_week = [2, 2, 2]
labs = ['CC', 'ISL']
faculty_course = {"Geetha": "C lab", "Gayathri": "DS lab", "Sundar": "MAD lab"}
lab_subjects = ["MAD Lab", "DS Lab", "C Lab"]
classrooms = {
    "regular": ["K504", "K505"],
    "lab": ["CC", "ISL", "Project"]
}
faculties = {
    "MFCS": ["Shankar", "Sundar"],
    "WT": ["Kalyani"],
    "SPC": ["Manavalan"],
    "DS": ["Gayatri"],
    "DBMS": ["Geetha", "Ilayaraja"],
    "TWM": ["Geetha", "Subathra"],
    "MAD Lab": ["Sundar"],
    "DS Lab": ["Gayatri"],
    "C Lab": ["Geetha"]
}
subjects = ["MFCS", "SPC", "DS", "DBMS", "WT", "TWM"]
regular_occurrence_per_week = [4, 3, 3, 4, 3, 1]  # Total of 18 teaching hours
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

# Function to generate a random allocation for the timetable
def generate_timetable(existing_timetable=None):
    timetable = [["" for _ in range(hours_per_day)] for _ in range(working_days)]
    
    for lab_index, course in enumerate(lab_courses):
        faculty = [f for f, c in faculty_course.items() if c == course][0]
        lab = labs[lab_index % len(labs)]  # Use modulo to cycle through available labs
        
        occurrences_remaining = occurrence_per_week[lab_index]
        while occurrences_remaining > 0:
            allocated = False
            while not allocated:
                day = random.randint(0, working_days - 1)
                
                # Ensure that the lab class has not already been allocated on this day
                if course not in [cell for cell in timetable[day]]:                    
                    even_hours = [h for h in range(0, hours_per_day - 2 + 1) if h % 2 == 0]
                    start_hour = random.choice(even_hours)
                    end_hour = start_hour + 2

                    # Check if the slot is available in the current timetable and doesn't conflict with existing timetable
                    if all(timetable[day][hour] == "" for hour in range(start_hour, end_hour)) and \
                       (existing_timetable is None or all(existing_timetable[day][hour] == "" for hour in range(start_hour, end_hour))):
                        for hour in range(start_hour, end_hour):
                            timetable[day][hour] = f"{course} ({lab}, {faculty})"
                        allocated = True
                        occurrences_remaining -= 1
    
    return timetable

# Function to allocate regular classes
def allocate_regular_classes(timetable, subjects, occurrence_per_week, existing_timetable=None):
    for subject_index, subject in enumerate(subjects):
        faculty_list = faculties[subject]
        occurrences_remaining = occurrence_per_week[subject_index]
        attempts = 0  # Counter to track the number of attempts
        max_attempts = 100  # Maximum number of attempts before breaking the loop
        
        while occurrences_remaining > 0:
            allocated = False
            attempts += 1
            if attempts > max_attempts:
                print(f"Skipping subject {subject} due to too many attempts")
                break
            
            while not allocated:
                day = random.randint(0, working_days - 1)
                hour = random.randint(0, hours_per_day - 1)
                
                if timetable[day][hour] == "" and (existing_timetable is None or existing_timetable[day][hour] == ""):
                    # Ensure faculty and classroom are free
                    faculty = random.choice(faculty_list)
                    classroom = random.choice(classrooms["regular"])
                    
                    if all(f"{subject}" not in timetable[d] for d in range(working_days)) and \
                       (existing_timetable is None or all(f"{subject}" not in existing_timetable[d] for d in range(working_days))):
                        timetable[day][hour] = f"{subject} ({classroom}, {faculty})"
                        allocated = True
                        occurrences_remaining -= 1

# Generate timetable for Class 1
class1_timetable = generate_timetable()

# Generate timetable for Class 2 without conflict with Class 1
class2_timetable = generate_timetable(existing_timetable=class1_timetable)

# Allocate regular classes for Class 1
allocate_regular_classes(class1_timetable, subjects, regular_occurrence_per_week)

# Allocate regular classes for Class 2 without conflict with Class 1
allocate_regular_classes(class2_timetable, subjects, regular_occurrence_per_week, existing_timetable=class1_timetable)

# Print the combined timetables for both classes
for i in range(len(class1_timetable)):
    for j in range(len(class1_timetable[i])):
        print(class1_timetable[i][j], " ------ ", class2_timetable[i][j])
    print("\n")
