import os
from datetime import date

from SweatStack import SweatStack


os.environ["SWEAT_STACK_API_KEY"] = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1R1A4SHhPc3R0NVVCZVgyMWVaOCIsImF6cCI6InVHUDhIeE9zdHQ1VUJlWDIxZVo4IiwiZXhwIjoxNzIwOTAzODM1LCJpYXQiOjE3MjAwMDM4MzV9.Nk4pWhTz3-qJpgvVlseI5FklBwjROS7GTaPN7gy7budia_0qWZZYx_8_cidhdrWfXZY7tOWPWv82yF9RZ3SQbmWxZbk9sydTKOKxX2g4mbj4WhbWg-muhU_BiIMMTZ-HtrWcesr_daoUZJuRUht8lzxHWsUT4cpleOGdN_yI9Wqcn_ZIr1njhRIXa8MaBWO0bxolpNa9a8iKxhUWw5sVJQaVIYidN0puhqaXCqZrrZNntdASbhCmHfWJeIeWlASZ7gtbGIaHTuI08tCrMZEj4Y0i-mAulT_zDtNNTevx6yL9LFSCuWl75euCLEph_2Ncw1yKzGB-wTSb6bP-solNSw"
# os.environ["SWEAT_STACK_URL"] = "http://localhost:2400"

def main():
    client = SweatStack()
    import time
    t0 = time.time()
    awd = client.get_accumulated_work_duration(
        start=date(2024, 1, 1),
        end=date(2024, 8, 1),
        sport="running",
        metric="power",
    )
    print(f"This took: {round(time.time() - t0, 2)} seconds")
    print(awd)


if __name__ == "__main__":
    main()