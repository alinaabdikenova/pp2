from datetime import datetime, timedelta

#1
today = datetime.now()

five_days_ago = today - timedelta(days=5)

print("#1")
print("Today:", today)
print("5 days ago:", five_days_ago)


#2. 
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)
print("#2")
print("Yesterday:", yesterday.date())  
print("Today:", today.date())
print("Tomorrow:", tomorrow.date())


#3.
no_microseconds = today.replace(microsecond=0)
print("#3")
print("With microseconds:", today)
print("Without microseconds:", no_microseconds)


#4. 
date1 = datetime(2025, 5, 10, 12, 0, 0)
date2 = datetime(2025, 5, 12, 14, 30, 0)

difference_seconds = abs((date2 - date1).total_seconds())
print("#4")
print("Date 1:", date1)
print("Date 2:", date2)
print("Difference in seconds:", difference_seconds)