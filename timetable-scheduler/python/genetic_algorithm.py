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

subjects = ["MFCS", "SPC", "DS", "DBMS", "WT", "TWM"]
subject_hours = [4, 3, 3, 4, 3, 1]  # Total of 18 teaching hours

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
hours_per_day = 7

def is_free(timetable, day, start_hour, duration=1):
    return all(timetable[day][hour] == "Free" for hour in range(start_hour, start_hour + duration))

def allocate_slot(timetable, day, start_hour, subject, faculty, classroom, duration=1):
    for hour in range(start_hour, start_hour + duration):
        timetable[day][hour] = f"{subject}, {faculty}, {classroom}"

def has_conflict(timetable, day, start_hour, subject, duration=1):
    faculty = random.choice(faculties[subject])
    for hour in range(start_hour, start_hour + duration):
        if timetable[day][hour] != "Free" and (faculty in timetable[day][hour] or timetable[day][hour].split(", ")[2] == classrooms["regular"][start_hour % len(classrooms["regular"])]):
            return True
    return False

def count_sessions(timetable, day, step=2):
    return sum(1 for hour in range(0, hours_per_day - 1, step) if timetable[day][hour] != "Free")

def allocate_lab_classes(timetable1, timetable2, lab_classes):
    for lab_class in lab_classes:
        faculty = random.choice(faculties[lab_class])
        classroom = classrooms["lab"][lab_classes.index(lab_class) % len(classrooms["lab"])]
        even_hours = [i for i in range(0, hours_per_day - 1, 2)]
        for day1, day2 in product(days, repeat=2):
            if day1 == day2:
                continue
            for hour1, hour2 in product(even_hours, repeat=2):
                if hour1 + 1 >= hours_per_day or hour2 + 1 >= hours_per_day:
                    continue
                if (is_free(timetable1, day1, hour1, 2) and 
                    is_free(timetable2, day1, hour1, 2) and 
                    is_free(timetable1, day2, hour2, 2) and 
                    is_free(timetable2, day2, hour2, 2) and 
                    count_sessions(timetable1, day1) < 2 and 
                    count_sessions(timetable2, day1) < 2 and 
                    count_sessions(timetable1, day2) < 2 and 
                    count_sessions(timetable2, day2) < 2):
                    allocate_slot(timetable1, day1, hour1, lab_class, faculty, classroom, 2)
                    allocate_slot(timetable2, day1, hour1, lab_class, faculty, classroom, 2)
                    allocate_slot(timetable1, day2, hour2, lab_class, faculty, classroom, 2)
                    allocate_slot(timetable2, day2, hour2, lab_class, faculty, classroom, 2)
                    return True
    return False

def allocate_regular_classes(timetable1, timetable2, subjects, subject_hours):
    for subject, hours in zip(subjects, subject_hours):
        allocated_hours = 0
        while allocated_hours < hours:
            for day in days:
                for hour in range(hours_per_day):
                    if allocated_hours >= hours:
                        break
                    if is_free(timetable1, day, hour, 1) and is_free(timetable2, day, hour, 1):
                        faculty = random.choice(faculties[subject])
                        classroom = classrooms["regular"][allocated_hours % len(classrooms["regular"])]
                        if not has_conflict(timetable1, day, hour, subject, 1) and not has_conflict(timetable2, day, hour, subject, 1):
                            allocate_slot(timetable1, day, hour, subject, faculty, classroom, 1)
                            allocate_slot(timetable2, day, hour, subject, faculty, classroom, 1)
                            allocated_hours += 1
                            if allocated_hours >= hours:
                                break

def generate_timetable(lab_classes, subjects, subject_hours, max_timetables=50):
    all_timetables = []
    for _ in range(max_timetables):
        timetable1 = {day: ["Free"] * hours_per_day for day in days}
        timetable2 = {day: ["Free"] * hours_per_day for day in days}

        if allocate_lab_classes(timetable1, timetable2, lab_classes) and allocate_lab_classes(timetable2, timetable1, lab_classes):
            allocate_regular_classes(timetable1, timetable2, subjects, subject_hours)
            allocate_regular_classes(timetable2, timetable1, subjects, subject_hours)
            all_timetables.append((timetable1, timetable2))

    return all_timetables

all_possible_timetables = generate_timetable(lab_subjects, subjects, subject_hours)

if all_possible_timetables:
    selected_index = random.randint(0, len(all_possible_timetables) - 1)
    selected_timetable1, selected_timetable2 = all_possible_timetables[selected_index]

    print(f"Number of possible outcomes: {len(all_possible_timetables)}")

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    print("\nSelected Timetable for Class1:")
    for day, slots in selected_timetable1.items():
        print(f"{day}: {slots}")

    print("\nSelected Timetable for Class2:")
    for day, slots in selected_timetable2.items():
        print(f"{day}: {slots}")

    print("\nConflicts Check:")
    for day in days:
        for i in range(7):
            if selected_timetable1[day][i] == "Free" or selected_timetable2[day][i] == "Free":
                print(day, " ", i+1, " ", selected_timetable1[day][i], "--- ", selected_timetable2[day][i])
            elif selected_timetable1[day][i].split(", ")[1] == selected_timetable2[day][i].split(", ")[1] or selected_timetable1[day][i].split(", ")[2] == selected_timetable2[day][i].split(", ")[2]:
                print(day, " ", i+1, " ", selected_timetable1[day][i], "--- ", selected_timetable2[day][i])
else:
    print("No valid timetable found.")