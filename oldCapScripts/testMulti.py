import subprocess
import threading
import time

# RUN THIS AS SUDO

# The list of commands that IP Addrs will be appended to
attackCommands = [
    # ("python3 HTTPRequest.py ", "HTTP_Request")           
    # ("nmap -sX -p 1-100 ", "XMAS_Flood"),
    # ("hping3 -S -c 100 -p 443 ", "TCP_SYN_Flood"),
    # ("hping3 --udp -c 100 -p 53 ", "UDP_Flood"),
    # ("hping3 -S -c 100 -p 80 ", "HTTP_Flood")
    
]

ipAddrs = [
    ("192.168.1.172", "phillipsHub"),
    ("192.168.1.196", "nestCam"),
    ("192.168.1.102", "googleNestMini"),
    ("192.168.1.103", "amazonAlexa"),
    ("192.168.1.175", "longPlus-Cam"),
    ("192.168.1.104", "kasaSmartPlug"),
    ("192.168.1.170", "roborockVacc"),	
    ("192.168.1.200", "okpVacc"),
    ("192.168.1.215", "GosungLight2"),	
    ("192.168.1.221", "RingDoorbell"),	
   ("192.168.1.", "HentleSmartLock")	
]

# The duration to collect packets (8 hours)
capture_duration = 8 * 60 * 60
# Safe period to stop attacks before the capture ends
safe_period = 15 * 60

def run_command(command):
    subprocess.run(command, shell=True)


# Function to schedule attacks within the allowed timeframe (8 hours minus the last 15 minutes)
# Schedule attacks within the allowed timeframe (8 hours minus the last 15 minutes)
def schedule_attacks(ipAddr, attackCommands, allowed_duration):
    start_time = time.time()
    log_path = f"./AttackCaps/{ipAddr[1]}_Multi.txt"
    
    with open(log_path, 'w') as log_file:
        total_attacks = len(attackCommands) * 3
        interval = (allowed_duration / total_attacks)
        
        for attackCommand in attackCommands:
            for i in range(3):  # Run each attack 3 times
                current_time = time.time()
                if current_time + interval < start_time + allowed_duration:
                    run_command(f"{attackCommand[0]}{ipAddr[0]}")
                    time_since_start = current_time - start_time
                    log_file.write(f"Attack: {attackCommand[1]}, Attempt: {i+1}, Unix Time: {current_time}, Time Since Start: {time_since_start}\n")
                    time.sleep(interval)
                else:
                    break


# Iterate through the list of devices
for ipAddr in ipAddrs:
    print(f"Capture started on {ipAddr[1]}")

    # Start tcpdump to collect packets
    tcpdump_process = subprocess.Popen(
        ["tcpdump", "-w", fr"./AttackCaps/{ipAddr[1]}_Multi.pcap"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    # Start time for capture
    capture_start_time = time.time()

    # Run attacks for the allowed timeframe (8 hours minus the last 15 minutes)
    schedule_attacks(ipAddr, attackCommands, capture_duration - safe_period)

    # Calculate remaining time to fulfill 8 hours of capture
    remaining_capture_time = (capture_start_time + capture_duration) - time.time()
    if remaining_capture_time > 0:
        time.sleep(remaining_capture_time)

    # Terminate the tcpdump process
    tcpdump_process.terminate()
    
    print(f"Capture and attacks completed on {ipAddr[1]}")

