import csv

def read_subjects_csv(path):
    subjects = {}

    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            code = row["CODE"].strip()
            
            subjects[code] = {
                "period": int(row["PERIOD"].strip()),
                "name": row["NAME"].strip(),
                "prerequisite": parse_codes(row["PREREQUISITE"].strip()),
                "corequisite": parse_codes(row["COREQUISITE"].strip()),
                "time": parse_time(row["TIME"].strip())
            }

    return subjects

def parse_codes(field):
    if not field or field.strip() == "":
        return []
    return [code.strip() for code in field.split(";")]

def parse_time(field):
    if not field or field.strip() == "":
        return []
    
    schedules = []

    for block in field.split(";"):
        block = block.strip()

        i = 0
        while block[i].isdigit():
            i += 1

        days = [int(d) for d in block[:i]]
        shift = block[i]
        start_slot = int(block[i+1])
        duration = int(block[i+2])

        base_hour = shift_start_hour(shift)
        start_time = base_hour + (start_slot - 1) * 0.5
        end_time = start_time + duration * 0.5

        for day in days:
            schedules.append({
                "day": day,
                "shift": shift,
                "start": start_time,
                "end": end_time
            })
    
    return schedules

def shift_start_hour(shift):
    if shift == "M":
        return 8
    elif shift == "T":
        return 13
    elif shift == "N":
        return 18
    else:
        raise ValueError(f"Invalid shift: {shift}")