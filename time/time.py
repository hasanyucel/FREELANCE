from datetime import datetime
today = datetime.today().strftime("%d/%m/%Y")
print(today)
from datetime import datetime, timezone
utc_current_datetime = datetime.now(timezone.utc).strftime("%d/%m/%Y")
print(utc_current_datetime)

import sys
def check_quit(inp):
    if inp == 'q':
        sys.exit(0)
x = str(input("Please press 'q' to exit: "))
check_quit(x)