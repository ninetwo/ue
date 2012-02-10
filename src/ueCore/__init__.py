import datetime

def formatDate(d):
    try:
        s = datetime.datetime.strptime(d, "%Y-%m-%dT%H:%M:%SZ").strftime("%d %b %y")
    except ValueError:
        s = "ERROR"
    return s

def formatTime(t):
    try:
        s = datetime.datetime.strptime(t, "%Y-%m-%dT%H:%M:%SZ").strftime("%H:%M")
    except ValueError:
        s = "ERROR"
    return s

def formatDatetime(dt):
    return "%s %s" % (formatDate(dt), formatTime(dt))

