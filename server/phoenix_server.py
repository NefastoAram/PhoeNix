from flask import Flask, jsonify
import psutil
import os
import glob
import requests
# Phoenix Server for monitoring system status
app = Flask(__name__)

# Cache pubblic IP and timestamp
public_ip = None
public_ip_last_update = 0

# Hostname and OS info
import socket, platform, subprocess
hostname = socket.gethostname()
try:
    lsb = subprocess.check_output(['lsb_release', '-a'], universal_newlines=True)
    desc = None
    for line in lsb.splitlines():
        if line.startswith('Description:'):
            desc = line.split(':',1)[1].strip()
            break
    if desc:
        osinfo = desc
    else:
        osinfo = platform.system() + ' ' + platform.release()
except Exception:
    osinfo = platform.system() + ' ' + platform.release()

@app.route('/api/status')
def status():
    # CPU temperature
    cpu_temp = None
    try:
        temps = []
        for zone in glob.glob('/sys/class/thermal/thermal_zone*/temp'):
            try:
                with open(zone) as f:
                    t = int(f.read().strip()) / 1000.0
                    if t > 0:
                        temps.append(t)
            except Exception:
                pass
        if temps:
            cpu_temp = max(temps)
    except Exception:
        pass
    # Alarm threshold (e.g. 120°C)
    cpu_temp_alarm = False
    if cpu_temp is not None and cpu_temp >= 120.0:
        cpu_temp_alarm = True
    cpu_percent = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    net = psutil.net_io_counters()
    # Load averages
    load_avg_1m = None
    load_avg_5m = None
    load_avg_15m = None
    try:
        la = os.getloadavg()
        load_avg_1m = la[0]
        load_avg_5m = la[1]
        load_avg_15m = la[2]
    except Exception:
        pass
    # Uptime
    uptime_seconds = None
    try:
        import time
        uptime_seconds = int(time.time() - psutil.boot_time())
    except Exception:
        pass
    # Info server
    import time
    global public_ip, public_ip_last_update
    now = int(time.time())
    # Update public IP only every hour
    if public_ip is None or (now - public_ip_last_update) > 3600:
        try:
            public_ip = requests.get('https://api.ipify.org', timeout=3).text
            public_ip_last_update = now
        except Exception:
            public_ip = None
    ip = public_ip
    return jsonify({
        'cpu_percent': cpu_percent,
        'ram_percent': ram.percent,
        'disk_percent': disk.percent,
        'net_sent': net.bytes_sent,
        'net_recv': net.bytes_recv,
        'load_avg_1m': load_avg_1m,
        'load_avg_5m': load_avg_5m,
        'load_avg_15m': load_avg_15m,
        'uptime_seconds': uptime_seconds,
        'cpu_temp': cpu_temp,
        'cpu_temp_alarm': cpu_temp_alarm,
        'hostname': hostname,
        'ip': ip,
        'os': osinfo,
        'timestamp': int(time.time())
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
