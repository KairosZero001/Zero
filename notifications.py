notifications = []

def add_notification(text):
    notifications.append(text)

def get_notifications():
    global notifications
    temp = notifications.copy()
    notifications.clear()
    return temp