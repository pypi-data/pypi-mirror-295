import random
import datetime

def generate_auth_log(output_file: str, log_count: int):
    """Generates and writes auth log entries to the specified output file."""
    with open(output_file, 'w') as file:
        for _ in range(log_count):
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            event_type = "Accepted password"
            user_id = random.choice(["alice", "bob", "charlie", "dave", "eve"])
            ip_address = f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}"
            log_message = f"{timestamp} AUTH {event_type} for {user_id} from IP {ip_address}"
            file.write(log_message + "\n")

def generate_syslog_log(output_file: str, log_count: int):
    """Generates and writes syslog entries to the specified output file."""
    with open(output_file, 'w') as file:
        for _ in range(log_count):
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            severity = random.choice(["INFO", "NOTICE"])
            service = random.choice(["sshd", "systemd", "nginx", "cron", "docker"])
            message = random.choice([
                "Service started successfully",
                "Configuration reloaded",
                "User logged out",
                "Scheduled task completed"
            ])
            log_message = f"{timestamp} {severity} {service}: {message}"
            file.write(log_message + "\n")

def generate_kern_log(output_file: str, log_count: int):
    """Generates and writes kernel log entries to the specified output file."""
    with open(output_file, 'w') as file:
        for _ in range(log_count):
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_level = random.choice(["INFO", "NOTICE"])
            event = random.choice(["Driver loaded", "Network interface up", "File system mounted"])
            log_message = f"{timestamp} KERNEL {log_level}: {event}"
            file.write(log_message + "\n")

def generate_daemon_log(output_file: str, log_count: int):
    """Generates and writes daemon log entries to the specified output file."""
    with open(output_file, 'w') as file:
        for _ in range(log_count):
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            daemon = random.choice(["sshd", "cron", "nginx", "mysql", "postfix"])
            status = random.choice(["started", "stopped", "restarted"])
            log_message = f"{timestamp} DAEMON {daemon}: Service {status}"
            file.write(log_message + "\n")

def generate_fail2ban_log(output_file: str, log_count: int):
    """Generates and writes fail2ban log entries to the specified output file."""
    with open(output_file, 'w') as file:
        for _ in range(log_count):
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            action = "Unban"
            ip_address = f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}"
            jail = random.choice(["ssh", "apache", "nginx", "mysql"])
            log_message = f"{timestamp} FAIL2BAN {action} IP {ip_address} in {jail}"
            file.write(log_message + "\n")
