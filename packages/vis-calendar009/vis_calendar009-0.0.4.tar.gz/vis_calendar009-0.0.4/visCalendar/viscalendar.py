from calendar import calendar

def visCalendar(year:int):
    try:
        print(calendar(year))
    except TypeError:
        print("You didnt enter a proper year.The fuction has one required argument called 'year'(which should be an integer)")

