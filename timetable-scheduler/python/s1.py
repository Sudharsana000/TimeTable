import json
import random

def generate_timetable(subjects, hours, lab_subjects, classrooms, faculties, existing_timetable=None):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    hours_per_day = 7
    total_hours_per_week = len(days) * hours_per_day

    timetable = {day: [None] * hours_per_day for day in days}
    used_classrooms = {day: [None] * hours_per_day for day in days}
    used_faculties = {day: [None] * hours_per_day for day in days}
    
    # Allocate lab hours first
    lab_allocations = {}  # Keep track of lab allocations
    for lab in lab_subjects:
        lab_periods = 2
        lab_allocated = 0
        while lab_allocated < lab_periods:
            day = random.choice(days)
            start_hour = random.choice([i for i in range(0, hours_per_day-1, 2)])
            if (timetable[day][start_hour] is None and timetable[day][start_hour + 1] is None and
                (existing_timetable is None or (existing_timetable[day][start_hour]["subject"] != lab and existing_timetable[day][start_hour + 1]["subject"] != lab)) and
                all(timetable[day][i] not in lab_subjects for i in range(start_hour, start_hour + 2))):

                # Check for available lab classroom and faculty
                available_classrooms = [clsrm for clsrm in classrooms["lab"] if clsrm not in (used_classrooms[day][start_hour: start_hour + 2])]
                available_faculties = [faculty for faculty in faculties[lab] if faculty not in (used_faculties[day][start_hour: start_hour + 2])]
                if available_classrooms and available_faculties:
                    classroom = random.choice(available_classrooms)
                    faculty = random.choice(available_faculties)
                    timetable[day][start_hour] = lab
                    timetable[day][start_hour + 1] = lab
                    used_classrooms[day][start_hour] = classroom
                    used_classrooms[day][start_hour + 1] = classroom
                    used_faculties[day][start_hour] = faculty
                    used_faculties[day][start_hour + 1] = faculty
                    lab_allocations[lab] = (classroom, faculty)
                    lab_allocated += 1

    # Allocate regular hours
    subject_hours = {subject: hrs for subject, hrs in zip(subjects, hours)}
    subject_allocation = {subject: 0 for subject in subjects}
    free_hours = total_hours_per_week - sum(hours) - len(lab_subjects) * 2
    subject_list = sum([[subject] * hrs for subject, hrs in zip(subjects, hours)], [])
    subject_list.extend([""] * free_hours)
    random.shuffle(subject_list)

    # Allocate subjects and remaining free hours
    for subject in subjects:
        while subject_allocation[subject] < subject_hours[subject]:
            for day in days:
                unallocated_hours = [hour for hour in range(hours_per_day) if timetable[day][hour] is None]
                if not unallocated_hours:
                    continue

                unallocated_faculties = [
                    faculty for faculty in faculties[subject]
                    if all(
                        faculty != used_faculties[day][hour] and (existing_timetable is None or faculty != existing_timetable[day][hour]["faculty"]) for hour in unallocated_hours
                    )
                ]
                available_classrooms = [
                    clsrm for clsrm in classrooms["regular"]
                    if all(
                        clsrm != used_classrooms[day][hour] and (existing_timetable is None or faculty != existing_timetable[day][hour]["classroom"]) for hour in unallocated_hours
                    )
                ]
                if unallocated_hours and unallocated_faculties and available_classrooms:
                    hour = random.choice(unallocated_hours)
                    faculty = random.choice(unallocated_faculties)
                    classroom = random.choice(available_classrooms)
                    timetable[day][hour] = subject
                    used_classrooms[day][hour] = classroom
                    used_faculties[day][hour] = faculty
                    subject_allocation[subject] += 1
                    break

    # Place free hours in the preferred slots
    for day in days:
        if timetable[day][-1] is None:
            timetable[day][-1] = ""
        elif timetable[day][3] is None:
            timetable[day][3] = ""

    return timetable

def replace_none_with_empty_string(timetable):
    for day in timetable:
        for i in range(len(timetable[day])):
            if timetable[day][i] is None:
                timetable[day][i] = ""
    return timetable

def allocate_classrooms_and_faculties(timetable, classrooms, faculties, existing_allocations=None):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    hours_per_day = 7
    free_hours = hours_per_day*len(days) - sum(hours) - len(lab_subjects) * 2

    allocated_timetable = {day: [] for day in days}
    used_classrooms = {day: [None] * hours_per_day for day in days}
    used_faculties = {day: [None] * hours_per_day for day in days}
    lab_allocations = {}  # Keep track of lab allocations
    subject_faculty_allocation = {}  # Ensure one faculty per subject per class

    if existing_allocations:
        for day in days:
            for hour in range(hours_per_day):
                if existing_allocations[day][hour]['subject']:
                    used_classrooms[day][hour] = existing_allocations[day][hour]['classroom']
                    used_faculties[day][hour] = existing_allocations[day][hour]['faculty']

    for day in days:
        for hour in range(hours_per_day):
            subject = timetable[day][hour]
            if subject:
                if "Lab" in subject:
                    if subject in lab_allocations and used_classrooms[day][hour] is None:
                        classroom, faculty = lab_allocations[subject]
                    else:
                       available_classrooms = [clsrm for clsrm in classrooms["lab"] if (used_classrooms[day][hour] is None or clsrm not in used_classrooms[day][hour]) and (used_classrooms[day][hour+1] is None or clsrm not in used_classrooms[day][hour+1])]
                       available_faculties = [flty for flty in faculties[subject] if (used_faculties[day][hour] is None or flty not in used_faculties[day][hour]) and (used_faculties[day][hour+1] is None or flty not in used_faculties[day][hour+1])]   
                       print(day," ",hour," ",available_classrooms)                    
                       if available_classrooms and available_faculties:
                            print(available_classrooms)
                            classroom = random.choice(available_classrooms)
                            faculty = random.choice(available_faculties)
                            print(classroom, " ", faculty)
                            lab_allocations[subject] = (classroom, faculty)
                            subject_faculty_allocation[subject] = faculty

                            allocated_timetable[day].append({
                                    "subject": subject,
                                    "classroom": classroom,
                                    "faculty": faculty
                            })
                            used_classrooms[day][hour] = classroom
                            used_faculties[day][hour] = faculty

                    allocated_timetable[day].append({
                            "subject": "",
                            "classroom": "",
                            "faculty": ""
                    })
                    free_hours -= 1

                elif free_hours > 0 and hour == 6:
                    allocated_timetable[day].append({
                        "subject": "",
                        "classroom": "",
                        "faculty": ""
                    })
                    free_hours -= 1

                else:
                    available_classrooms = [clsrm for clsrm in classrooms["regular"] if clsrm not in (used_classrooms[day][hour] if used_classrooms[day][hour] else [])]
                    if not available_classrooms:
                        raise Exception(f"No available regular classrooms for {subject} on {day} at hour {hour}")
                    classroom = random.choice(available_classrooms)

                    available_classrooms_and_faculties = [(clsrm, faculty) for clsrm in classrooms["regular"] for faculty in faculties[subject] 
                                      if clsrm not in (used_classrooms[day][hour] if used_classrooms[day][hour] else []) 
                                      and faculty not in (used_faculties[day][hour] if used_faculties[day][hour] else [])]

                    if available_classrooms_and_faculties:
                        classroom, faculty = random.choice(available_classrooms_and_faculties)
                        allocated_timetable[day].append({
                            "subject": subject,
                            "classroom": classroom,
                            "faculty": faculty
                        })
                        used_classrooms[day][hour] = classroom
                        used_faculties[day][hour] = faculty
            else:
                allocated_timetable[day].append({
                    "subject": "",
                    "classroom": "",
                    "faculty": ""
                })
                free_hours -= 1

    return allocated_timetable

if __name__ == "__main__":
    subjects = ["MFCS", "SPC", "DS", "DBMS", "WT", "TWM"]
    hours = [4, 3, 3, 4, 3, 1]  # Total of 18 teaching hours
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

    class1_timetable = generate_timetable(subjects, hours, lab_subjects, classrooms, faculties)
    class1_timetable = replace_none_with_empty_string(class1_timetable)
    allocated_class1_timetable = allocate_classrooms_and_faculties(class1_timetable, classrooms, faculties)

    class2_timetable = generate_timetable(subjects, hours, lab_subjects, classrooms, faculties, allocated_class1_timetable)
    class2_timetable = replace_none_with_empty_string(class2_timetable)
    allocated_class2_timetable = allocate_classrooms_and_faculties(class2_timetable, classrooms, faculties, allocated_class1_timetable)

    # print(json.dumps({
    #     "class1": allocated_class1_timetable,
    #     "class2": allocated_class2_timetable
    # }, indent=4))
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    for day in days:
        for hour in range(7):
            if allocated_class1_timetable[day][hour]['classroom'] == allocated_class2_timetable[day][hour]['classroom'] or allocated_class1_timetable[day][hour]['faculty'] == allocated_class2_timetable[day][hour]['faculty']:
                print(day," - ",hour, " - ",allocated_class1_timetable[day][hour]," - ",allocated_class2_timetable[day][hour])

    #print(allocated_class1_timetable)