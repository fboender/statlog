#!/usr/bin/python

import sys
import datetime
import time

def get_datetime():
    now = datetime.datetime.now()
    return {
        "time_epoch": time.mktime(now.timetuple()),
        "time_datetime": now.strftime("%Y-%m-%d_%H:%M:%S"),
    }

def get_load_avg():
    with open('/proc/loadavg', 'r') as f:
        fields = f.readline().split()
        return {
            "load_avg_1": float(fields[0]),
            "load_avg_5": float(fields[1]),
            "load_avg_15": float(fields[1])
        }

def get_cpu():
    with open('/proc/stat', 'r') as f:
        fields = f.readline().split()
        return {
            "cpu_id": fields[0],
            "cpu_user": int(fields[1]),
            "cpu_nice": int(fields[2]),
            "cpu_system": int(fields[3]),
            "cpu_idle": int(fields[4]),
            "cpu_iowait": int(fields[5]),
            "cpu_irq": int(fields[6]),
            "cpu_softirq": int(fields[7]),
            "cpu_steal": int(fields[8]),
        }

def get_vmstat():
    vmstat = {}
    with open('/proc/vmstat', 'r') as f:
        for line in f.readlines():
            key, value = line.strip().split()
            vmstat['vmstat_' + key] = int(value)
    return vmstat

def get_mem():
    meminfo = {}
    with open('/proc/meminfo', 'r') as f:
        for line in f.readlines():
            key, value = line.strip().split(':')
            if value.endswith("kB"):
                meminfo['mem_' + key.lower()] = int(value.lstrip().split(' ')[0]) * 1024
            else:
                meminfo['mem_' + key.lower()] = int(value.lstrip())
    return meminfo

show_fields = [
    "time_datetime",
    "load_avg_1",
    "load_avg_5",
    "load_avg_15",
    "cpu_iowait",
    "mem_memtotal",
    "mem_memfree",
    "mem_buffers",
    "mem_cached"
]
fmt_headers = " ".join(show_fields)
fmt_fields = " ".join(
        ["{"+format(field)+"}" for field in show_fields]
    )

sys.stdout.write(fmt_headers + "\n")

while True:
    stats = {}
    stats.update(get_datetime())
    stats.update(get_load_avg())
    stats.update(get_cpu())
    stats.update(get_vmstat())
    stats.update(get_mem())

    sys.stdout.write(fmt_fields.format(**stats) + "\n")
    sys.stdout.flush()
    time.sleep(1)
