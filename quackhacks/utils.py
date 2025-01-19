from collections import defaultdict

def convert_time_to_minutes(time_str):
    hours, minutes = map(int, time_str.split(':'))
    return hours * 60 + minutes

def convert_minutes_to_time(minutes):
    hours = minutes // 60
    minutes = minutes % 60
    return f"{hours:02}:{minutes:02}"

def intersect_intervals(intervals1, intervals2):
    i, j = 0, 0
    result = []
    
    while i < len(intervals1) and j < len(intervals2):
        start1, end1 = intervals1[i]
        start2, end2 = intervals2[j]
        
        # Find the overlap
        start = max(start1, start2)
        end = min(end1, end2)
        
        if start < end:
            result.append((start, end))
        
        # Move the pointer of the interval that ends first
        if end1 < end2:
            i += 1
        else:
            j += 1
    
    return result

def reorder_schedule(schedule):
    """Reorders a defaultdict by the days of the week."""
    week_order = ['M', 'T', 'W', 'R', 'F']
    reordered = defaultdict(list)
    
    for day in week_order:
        if day in schedule:
            reordered[day] = schedule[day]
    
    return reordered

def find_common_free_times(schedules):
    # Flatten schedules into a single list
    all_courses = [course for user_schedule in schedules for course in user_schedule]
    
    # Group schedules by day
    schedules_by_day = defaultdict(list)
    for course in all_courses:
        for day in course['days']:
            schedules_by_day[day].append(course)
    
    common_free_times = defaultdict(list)
    
    for day, courses in schedules_by_day.items():
        # Group courses by user
        user_schedules = defaultdict(list)
        for course in courses:
            user_schedules[course['course']].append(course)
        
        # Calculate free times for each user
        free_times_by_user = {}
        for user_id, classes in user_schedules.items():
            classes.sort(key=lambda x: convert_time_to_minutes(x['start_time']))
            free_times = []
            end_of_last_class = 0  # Start of the day in minutes
            
            for cls in classes:
                start_time = convert_time_to_minutes(cls['start_time'])
                if start_time > end_of_last_class:
                    free_times.append((end_of_last_class, start_time))
                end_of_last_class = max(end_of_last_class, convert_time_to_minutes(cls['end_time']))
            
            # Assume end of the day is 1440 minutes (24 hours)
            if end_of_last_class < 1440:
                free_times.append((end_of_last_class, 1440))
            
            free_times_by_user[user_id] = free_times
        
        # Find common free times across users
        common_times = list(free_times_by_user.values())[0]
        for free_times in list(free_times_by_user.values())[1:]:
            common_times = intersect_intervals(common_times, free_times)
        
        common_free_times[day] = [(convert_minutes_to_time(start), convert_minutes_to_time(end)) for start, end in common_times]
    common_free_times = reorder_schedule(common_free_times)
    return common_free_times