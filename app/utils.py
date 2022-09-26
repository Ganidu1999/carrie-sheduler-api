from matplotlib.style import available
import numpy as np
import pandas as pd
from datetime import datetime, timedelta, date, time


def get_duration(start, end):
    duration = datetime.combine(date.min, end) - datetime.combine(date.min, start)
    seconds = duration.total_seconds()
    hours = seconds // 3600
    print(hours)
    minutes = (seconds % 3600) // 60
    if minutes>0:
        appointment_duration = hours +1
    else: appointment_duration = hours
    return appointment_duration


def find_timeslot(doc_data, user_dist, appointment_duration, user_time_slot, dateA):
    arr=[]
    for doc in doc_data:
        doc_id = (doc['id'])
        appointments = doc['appointments']
        # work_hours = doc['work_hours']
        dist = doc['distance']
        # print(work_hours)
        work_hours = [datetime.combine(dateA, time(9, 0)), datetime.combine(dateA, time(18,0))]
        print(work_hours)
        available_slots = get_slots(work_hours, appointments,appointment_duration, dateA)
        # print(available_slots) 
        col= {
            'id':doc_id,
            'available_slots':available_slots,
            'dist':dist
        }
        arr.append(col)
        # get_daily_appointments(appointments, dateA)
    available_doctors = []
    for data in arr:
        if data['dist']<=user_dist:
            for ts in data['available_slots']:
                # print(ts,user_time_slot )
                if ts==user_time_slot:
                    available_doctors.append(data['id'])
                else: err = "No doctors available at the selected time slot" 
        # else: 
        #     err = "No Doctors available in this range. Please increase the distance!"


    # print(err)
    print(available_doctors)
    return available_doctors


def get_daily_appointments(appointments, dateA):
    # print(dateA)
    appointments_on_the_day = []
    for i in appointments:
        # print(i[0].date())
        if (i[0].date()==dateA):
            appointments_on_the_day.append(i)
    return(appointments_on_the_day)


def get_slots(hours, appointments, appointment_duration, dateA ):
    appointments = get_daily_appointments(appointments, dateA)
    # print(appointments)
    
    duration=timedelta(hours=appointment_duration)
    available_slots = []
    # print(appointments)
    if appointments != []:
        slots = sorted([(hours[0], hours[0])] + appointments + [(hours[1], hours[1])])
    else: slots = [(hours[0], hours[0])] + [(hours[1], hours[1])]
    # print(slots)
    for start, end in ((slots[i][1], slots[i+1][0]) for i in range(len(slots)-1)):
        # print(start, end)
        assert start <= end, "Cannot attend all appointments"
        while start + duration <= end:
            # print(start, start + duration)
            time_slot = "{:%Y:%m:%d:%H:%M} - {:%Y:%m:%d:%H:%M}".format(start, start + duration)
            available_slots.append(time_slot)
            # print ()
            start += duration
    print("hello")
    print(available_slots)       

    return available_slots