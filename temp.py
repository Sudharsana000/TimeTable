import random

# Define the input parameters
working_days = 5
hours_per_day = 7
lab_courses = ['C lab', 'DS lab', 'MAD lab']
occurrence_per_week = [2, 2, 2]
labs = ['CC', 'ISL', 'project']  # Updated labs
faculty_course = {"Geetha": "C lab", "Gayathri": "DS lab", "Sundar": "MAD lab"}

# Initialize variables
lab_slots = 2  # Each lab lasts for 2 hours
num_lab_courses = len(lab_courses)

# Function to generate a random allocation for the timetable
def generate_timetable():
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
                if course not in [timetable[day]]:
                    even_hours = [h for h in range(0, hours_per_day - lab_slots + 1) if h % 2 == 0]
                    start_hour = random.choice(even_hours)
                    end_hour = start_hour + lab_slots
                    
                    # Ensure that the chosen time slot is available
                    if all(timetable[day][hour] == "" for hour in range(start_hour, end_hour)):
                        for hour in range(start_hour, end_hour):
                            timetable[day][hour] = f"{course} ({lab}, {faculty})"
                        allocated = True
                        occurrences_remaining -= 1
    
    return timetable

# Generate 10 unique timetables
timetables = set()
while len(timetables) < 10:
    new_timetable = generate_timetable()
    # Convert to tuple of tuples to make it hashable
    timetable_tuple = tuple(tuple(row) for row in new_timetable)
    timetables.add(timetable_tuple)

# Select one timetable randomly
selected_timetable = random.choice(list(timetables))

# Print the selected timetable
for day_index, day in enumerate(selected_timetable):
    print(f"Day {day_index + 1}:")
    for hour, course in enumerate(day):
        print(f" Hour {hour + 1}: {course if course else 'Free'}")
    print("\n")