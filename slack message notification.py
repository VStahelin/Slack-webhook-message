import requests
import json
import psutil
import platform
from datetime import datetime

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


# System overview
uname = platform.uname()
system_name = uname.system
Release = uname.release
Version = uname.version
from time import gmtime, strftime
time = str(strftime("%d/%m/%y %H:%M:%S", gmtime()))

# Boot Time
boot_time_timestamp = psutil.boot_time()
bt = datetime.fromtimestamp(boot_time_timestamp)
boot_time =  (str(bt.day) + "/" + str(bt.month) + "/" + str(bt.year) + " " + str(bt.hour) + ":" + str(bt.minute) + ":" + str(bt.second))

# CPU Information
# number of cores
Physical_cores = psutil.cpu_count(logical=False)
Total_cores = psutil.cpu_count(logical=True)

# CPU frequencies
cpufreq = psutil.cpu_freq()
Current_Frequency = str(cpufreq.current) + "Mhz"

# CPU usage
core = ""
for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
    core = core + "\n core " + str(i) + ": " + str(percentage) + "%"
Total_CPU_Usage = str(psutil.cpu_percent()) + "%"

# Memory Information
svmem = psutil.virtual_memory()
Total_Memory = get_size(svmem.total)
Memory_Used = get_size(svmem.used)
Memory_Percentage = str(svmem.percent)

slack_msg = {
    "text": "Gateway Action",
    "blocks": [
        {
            "type": "section",
            "block_id": "section567",
            "text": {
                "type": "mrkdwn",
                "text": "*Restarting Master and Gateway* _machine time: " +time+ "_"
            },
            "accessory": {
                "type": "image",
                "image_url": "https://upload.wikimedia.org/wikipedia/commons/b/bc/Refresh_icon.png",
                "alt_text": "Reload ICON"
            },
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "*Name*"
                },
                {
                    "type": "mrkdwn",
                    "text": "*Value*"
                },
                {
                    "type": "plain_text",
                    "text": "System"
                },
                {
                    "type": "plain_text",
                    "text": system_name + "\n release: " + Release + "\n version: " + Version 
                },
                {
                        "type": "plain_text",
                    "text": "Boot Time"
                },
                {
                    "type": "plain_text",
                    "text": boot_time
                }
            ]
        },
		{
			"type": "divider"
		},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Machine Diagnostics*"
            },
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "*Name*"
                },
                {
                    "type": "mrkdwn",
                    "text": "*Value*"
                },
                {
                        "type": "plain_text",
                    "text": "Total CPU Usage from x cores"
                },
                {
                    "type": "plain_text",
                    "text": str(Total_CPU_Usage) + " from " + str(Total_cores) + " cores"
                },
                {
                    "type": "plain_text",
                    "text": "Current Frequency"
                },
                {
                    "type": "plain_text",
                    "text":  Current_Frequency
                },
                {
                    "type": "plain_text",
                    "text": "Memory Used from *"
                },
                {
                    "type": "plain_text",
                    "text":  Memory_Used + " from " + Total_Memory
                },
                {
                    "type": "plain_text",
                    "text": "Memory Percentage"
                },
                {
                    "type": "plain_text",
                    "text":  Memory_Percentage + "%"
                }
            ]
        }
    ]
}

#Sending message for slack
web_hook_url = 'https://hooks.slack.com/services/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'
requests.post(web_hook_url,data=json.dumps(slack_msg))