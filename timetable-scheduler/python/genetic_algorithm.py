import random
from itertools import product

# Initial Data
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

# Timetable Initialization
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
hours_per_day = 7

# Helper function to check if a slot is free
def is_free(timetable, day, start_hour, duration=2):
    for hour in range(start_hour, start_hour + duration):
        if timetable[day][hour] != "Free":
            return False
    return True

# Helper function to allocate a slot
def allocate_slot(timetable, day, start_hour, subject, faculty, classroom, duration=2):
    for hour in range(start_hour, start_hour + duration):
        timetable[day][hour] = f"{subject}, {faculty}, {classroom}"

# Helper function to check for conflicts in classroom and faculty allocations
def has_conflict(timetable, day, start_hour, subject, duration=2):
    faculty = faculties[subject][0]  # Assuming one faculty per subject for simplicity
    for hour in range(start_hour, start_hour + duration):
        if timetable[day][hour] != "Free" and (faculty in timetable[day][hour]):
            return True
    return False

# Helper function to count lab sessions per day
def count_sessions(timetable, day, step=2):
    return sum(1 for hour in range(0, hours_per_day - 1, step) if timetable[day][hour] != "Free")

# Backtracking function to generate timetable for labs
def generate_timetable(timetable, lab_classes, index=0, all_timetables=[], max_timetables=50):
    if len(all_timetables) >= max_timetables:
        return True

    if index >= len(lab_classes):
        all_timetables.append({day: timetable[day][:] for day in days})
        return True

    lab_class = lab_classes[index]
    faculty = faculties[lab_class][0]
    classroom = classrooms["lab"][index % len(classrooms["lab"])]

    found = False
    even_hours = [i for i in range(0, hours_per_day - 1, 2)]

    for day1, day2 in product(days, repeat=2):
        if day1 == day2:
            continue

        for hour1, hour2 in product(even_hours, repeat=2):
            if hour1 + 1 >= hours_per_day or hour2 + 1 >= hours_per_day:
                continue

            if (is_free(timetable, day1, hour1) and 
                is_free(timetable, day2, hour2) and 
                count_sessions(timetable, day1) < 2 and 
                count_sessions(timetable, day2) < 2):
                
                allocate_slot(timetable, day1, hour1, lab_class, faculty, classroom)
                allocate_slot(timetable, day2, hour2, lab_class, faculty, classroom)

                if generate_timetable(timetable, lab_classes, index + 1, all_timetables, max_timetables):
                    found = True

                # Backtrack
                for hour in range(hour1, hour1 + 2):
                    timetable[day1][hour] = "Free"
                for hour in range(hour2, hour2 + 2):
                    timetable[day2][hour] = "Free"

    return found

# Generate timetable for Class1 first
timetable1 = {day: ["Free"] * hours_per_day for day in days}
all_timetables1 = []
generate_timetable(timetable1, lab_subjects, 0, all_timetables1)

if not all_timetables1:
    print("No valid timetable found for Class1.")
    exit()

# Use timetable1 as a constraint to generate timetable for Class2
def generate_timetable_with_constraints(timetable1, timetable2, lab_classes, index=0, all_timetables=[], max_timetables=50):
    if len(all_timetables) >= max_timetables:
        return True

    if index >= len(lab_classes):
        all_timetables.append({day: timetable2[day][:] for day in days})
        return True

    lab_class = lab_classes[index]
    faculty = faculties[lab_class][0]
    classroom = classrooms["lab"][index % len(classrooms["lab"])]

    found = False
    even_hours = [i for i in range(0, hours_per_day - 1, 2)]

    for day1, day2 in product(days, repeat=2):
        if day1 == day2:
            continue

        for hour1, hour2 in product(even_hours, repeat=2):
            if hour1 + 1 >= hours_per_day or hour2 + 1 >= hours_per_day:
                continue

            if (is_free(timetable2, day1, hour1) and 
                is_free(timetable2, day2, hour2) and 
                count_sessions(timetable2, day1) < 2 and 
                count_sessions(timetable2, day2) < 2 and 
                not has_conflict(timetable1, day1, hour1, lab_class) and 
                not has_conflict(timetable1, day2, hour2, lab_class)):
                
                allocate_slot(timetable2, day1, hour1, lab_class, faculty, classroom)
                allocate_slot(timetable2, day2, hour2, lab_class, faculty, classroom)

                if generate_timetable_with_constraints(timetable1, timetable2, lab_classes, index + 1, all_timetables, max_timetables):
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
    timetable2 = {day: ["Free"] * hours_per_day for day in days}
    generate_timetable_with_constraints(timetable1_instance, timetable2, lab_subjects, 0, all_timetables2)

if not all_timetables2:
    print("No valid timetable found for Class2.")
    exit()

# Regular class allocation
subjects = ["MFCS", "SPC", "DS", "DBMS", "WT", "TWM"]
subject_hours = [4, 3, 3, 4, 3, 1]  # Total of 18 teaching hours

# Helper function to allocate regular classes
def allocate_regular_classes(timetable, subjects, subject_hours):
    for subject, hours in zip(subjects, subject_hours):
        allocated_hours = 0
        while allocated_hours < hours:
            for day in days:
                for hour in range(hours_per_day):
                    if allocated_hours >= hours:
                        break
                    if is_free(timetable, day, hour, 1):
                        faculty = faculties[subject][0] if len(faculties[subject]) == 1 else random.choice(faculties[subject])
                        classroom = classrooms["regular"][allocated_hours % len(classrooms["regular"])]
                        if not has_conflict(timetable, day, hour, subject, 1):
                            allocate_slot(timetable, day, hour, subject, faculty, classroom, 1)
                            allocated_hours += 1
                            if allocated_hours >= hours:
                                break
                        else:
                            continue

# Allocate regular classes for Class1
for timetable in all_timetables1:
    allocate_regular_classes(timetable, subjects, subject_hours)

# Allocate regular classes for Class2 with constraints
for timetable in all_timetables2:
    allocate_regular_classes(timetable, subjects, subject_hours)

# Select one timetable randomly
selected_index = random.randint(0, min(len(all_timetables2), 50) - 1)
selected_timetable1 = all_timetables1[selected_index]
selected_timetable2 = all_timetables2[selected_index]

print(f"Number of possible outcomes: {min(len(all_timetables2), 50)}")

# print("\nSelected Timetable for Class1:")
# for day, slots in selected_timetable1.items():
#     print(f"{day}: {slots}")
    
# print("\nSelected Timetable for Class2:")
# for day, slots in selected_timetable2.items():
#     print(f"{day}: {slots}")

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
for day in days:
    for i in range(7):
        print(day, " ",i+1, " ",selected_timetable1[day][i], " ", selected_timetable1[day][i])

print("----------------------------------------------------------------------")

for day in days:
    for i in range(7):
        if selected_timetable1[day][i][1] == selected_timetable2[day][i][1] or selected_timetable1[day][i][2] == selected_timetable2[day][i][2]:
            print(day, " ",i+1, " ",selected_timetable1[day][i], "--- ", selected_timetable1[day][i])