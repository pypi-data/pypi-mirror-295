import os
import time
from datetime import date, timedelta

import sweatstack as ss


os.environ["SWEAT_STACK_URL"] = "http://localhost:2400"

start = time.time()
ss.login()

print(f"Login successful. {os.environ['SWEAT_STACK_API_KEY']=}")

activities = list(ss.list_activities(as_dataframe=False))
end = time.time()
print(f"Time taken: {end - start} seconds")
print(f"Number of activities: {len(activities)}")


start = time.time()
activities =  ss.list_activities(as_dataframe=True)
end = time.time()

print(f"Time taken: {end - start} seconds")
print(f"Number of activities: {len(activities)}")
print(activities.head())


latest_activity = ss.get_latest_activity()
print(f"{latest_activity=}")


awd = ss.get_accumulated_work_duration(
    start=date.today() - timedelta(days=90),
    sport="running",
    metric="power",
)
print(f"{awd=}")


mean_max = ss.get_mean_max(
    start=date.today() - timedelta(days=90),
    sport="cycling",
    metric="power",
)
print(f"{mean_max=}")

users = ss.list_users()
print(f"{users=}")

users = ss.list_accessible_users()
print(f"{users=}")
print("")

for user in users:
    if user.last_name.lower() == "nistad":
        jon_helge = user
        break
else:
    raise Exception("Did not find Jon Helge!")

user = ss.whoami()
print(f"WHOAMI {user=}")
print("")
ss.switch_user(jon_helge)

user = ss.whoami()
print(f"WHOAMI {user=}")
print("")

activity = ss.get_latest_activity()
print(f"{activity=}")
print("")

user = ss.whoami()
print(f"WHOAMI {user=}")
print("")

ss.switch_to_root_user()
user = ss.whoami()
print(f"WHOAMI {user=}")
print("")

activity = ss.get_latest_activity()
print(f"{activity=}")

data = ss.get_latest_activity_data()
print(f"{data=}")

longitudinal_data = ss.get_longitudinal_data(
    start=date.today() - timedelta(days=180),
    sport="running",
    metrics=["power", "heart_rate", "speed"],
)
print(f"{longitudinal_data.head()=}")