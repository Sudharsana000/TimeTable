import random
from itertools import product

# Initial Data
lab_subjects = ["MAD Lab", "DS Lab", "C Lab"]  # Modify this list to have fewer labs if needed
classrooms = ["CC", "ISL"]  # Adjust classrooms based on the number of labs
faculties = {"MAD Lab": "Sundar", "DS Lab": "Gayatri", "C Lab": "Geetha"}  # Map faculties to labs

# Timetable Initialization
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
hours = 7  # Each day has 7 hours

# Helper function to check if a slot is free
def is_free(timetable, day, start_hour, duration=2):
    for hour in range(start_hour, start_hour + duration):
        if timetable[day][hour] != "Free":
            return False
    return True

# Helper function to allocate a slot
def allocate_slot(timetable, day, start_hour, lab_class, faculty, classroom):
    for hour in range(start_hour, start_hour + 2):
        timetable[day][hour] = f"{lab_class}, {faculty}, {classroom}"

# Helper function to check for conflicts in classroom and faculty allocations
def has_conflict(timetable, day, start_hour, lab_class, duration=2):
    faculty = faculties[lab_class]
    classroom_index = lab_subjects.index(lab_class) % len(classrooms)
    classroom = classrooms[classroom_index]
    
    for hour in range(start_hour, start_hour + duration):
        if timetable[day][hour] != "Free" and (faculty in timetable[day][hour] or classroom in timetable[day][hour]):
            return True
    return False

# Helper function to count lab sessions per day
def count_sessions(timetable, day):
    return sum(1 for hour in range(0, 6, 2) if timetable[day][hour] != "Free")

# Backtracking function to generate timetable
def generate_timetable(timetable, lab_classes, index=0, all_timetables=[]):
    if len(all_timetables) >= 50:
        return True  # Stop if we have reached the limit

    if index >= len(lab_classes):
        all_timetables.append({day: timetable[day][:] for day in days})  # Store a copy of the timetable
        return True

    lab_class = lab_classes[index]
    faculty = faculties[lab_class]
    classroom_index = index % len(classrooms)
    classroom = classrooms[classroom_index]

    found = False
    even_hours = [i for i in range(0, 6, 2)]  # Only even hours: 0, 2, 4

    for day1, day2 in product(days, repeat=2):
        if day1 == day2:
            continue

        for hour1, hour2 in product(even_hours, repeat=2):
            if hour1 + 1 >= hours or hour2 + 1 >= hours:
                continue

            if (is_free(timetable, day1, hour1) and 
                is_free(timetable, day2, hour2) and 
                count_sessions(timetable, day1) < 2 and 
                count_sessions(timetable, day2) < 2):
                
                allocate_slot(timetable, day1, hour1, lab_class, faculty, classroom)
                allocate_slot(timetable, day2, hour2, lab_class, faculty, classroom)

                if generate_timetable(timetable, lab_classes, index + 1, all_timetables):
                    found = True

                # Backtrack
                for hour in range(hour1, hour1 + 2):
                    timetable[day1][hour] = "Free"
                for hour in range(hour2, hour2 + 2):
                    timetable[day2][hour] = "Free"

    return found

# Generate timetable for Class1 first
timetable1 = {day: ["Free"] * hours for day in days}
all_timetables1 = []
generate_timetable(timetable1, lab_subjects, 0, all_timetables1)

if not all_timetables1:
    print("No valid timetable found for Class1.")
    exit()

# Use timetable1 as a constraint to generate timetable for Class2
def generate_timetable_with_constraints(timetable1, timetable2, lab_classes, index=0, all_timetables=[]):
    if len(all_timetables) >= 50:
        return True  # Stop if we have reached the limit

    if index >= len(lab_classes):
        all_timetables.append({day: timetable2[day][:] for day in days})  # Store a copy of the timetable
        return True

    lab_class = lab_classes[index]
    faculty = faculties[lab_class]
    classroom_index = index % len(classrooms)
    classroom = classrooms[classroom_index]

    found = False
    even_hours = [i for i in range(0, 6, 2)]  # Only even hours: 0, 2, 4

    for day1, day2 in product(days, repeat=2):
        if day1 == day2:
            continue

        for hour1, hour2 in product(even_hours, repeat=2):
            if hour1 + 1 >= hours or hour2 + 1 >= hours:
                continue

            if (is_free(timetable2, day1, hour1) and 
                is_free(timetable2, day2, hour2) and 
                count_sessions(timetable2, day1) < 2 and 
                count_sessions(timetable2, day2) < 2 and 
                not has_conflict(timetable1, day1, hour1, lab_class) and 
                not has_conflict(timetable1, day2, hour2, lab_class)):
                
                allocate_slot(timetable2, day1, hour1, lab_class, faculty, classroom)
                allocate_slot(timetable2, day2, hour2, lab_class, faculty, classroom)

                if generate_timetable_with_constraints(timetable1, timetable2, lab_classes, index + 1, all_timetables):
                    found = True

                # Backtrack
                for hour in range(hour1, hour1 + 2):
                    timetable2[day1][hour] = "Free"
                for hour in range(hour2, hour2 + 2):
                    timetable2[day2][hour] = "Free"

    return found

# Initialize empty timetable for Class2
all_timetables2 = []

# Generate timetables for Class2 with constraints from Class1
for timetable1_instance in all_timetables1:
    timetable2 = {day: ["Free"] * hours for day in days}
    generate_timetable_with_constraints(timetable1_instance, timetable2, lab_subjects, 0, all_timetables2)

if not all_timetables2:
    print("No valid timetable found for Class2.")
else:
    # Select one timetable randomly
    selected_index = random.randint(0, len(all_timetables2) - 1)
    selected_timetable1 = all_timetables1[selected_index]
    selected_timetable2 = all_timetables2[selected_index]

    print(f"Number of possible outcomes: {min(len(all_timetables2), 50)}")

    print("\nSelected Timetable for Class1:")
    for day, slots in selected_timetable1.items():
        print(f"{day}: {slots}")
    
    print("\nSelected Timetable for Class2:")
    for day, slots in selected_timetable2.items():
        print(f"{day}: {slots}")
