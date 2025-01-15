import os,time,random

"""Get current User"""
def get_current_user():
    return os.getlogin()

"""Generates unique ID wrt epoch time"""
def generate_unique_id():
    epoch_time = int(time.time() * 1000)
    random_suffix = random.randint(1000, 9999)
    return f"{epoch_time}{random_suffix}"