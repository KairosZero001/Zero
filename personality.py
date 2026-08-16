#loads memory from system.txt and adds current date and time and user name

from datetime import datetime
from prompts import load_prompt

def load_personality():

    personality = load_prompt("system.txt")

    now = datetime.now()

    personality += f"""

Current Date:
{now.strftime("%d %B %Y")}

Current Time:
{now.strftime("%I:%M %p")}
"""

    return personality