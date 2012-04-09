import datetime

def formatDate(d):
    try:
        s = datetime.datetime.strptime(d[0:-6], "%Y-%m-%dT%H:%M:%S").strftime("%d %b %y")
    except ValueError:
        s = "ERROR"
    return s

def formatTime(t):
    try:
        s = datetime.datetime.strptime(t[0:-6], "%Y-%m-%dT%H:%M:%S").strftime("%H:%M")
    except ValueError:
        s = "ERROR"
    return s

def formatDatetime(dt):
    return "%s, %s" % (formatDate(dt), formatTime(dt))

