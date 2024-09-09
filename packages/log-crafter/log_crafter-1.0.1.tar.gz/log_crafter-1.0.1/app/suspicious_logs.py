import random
import datetime

def generate_failed_auth_log(output_file: str, log_count: int):
    """Generates and writes failed auth log entries to the specified output file."""
    with open(output_file, 'w') as file:
        for _ in range(log_count):
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            event_type = "Failed password"
            user_id = random.choice(["root", "admin", "guest", "unknown"])
            ip_address = f"203.0.{random.randint(0, 255)}.{random.randint(0, 255)}"
            log_message = f"{timestamp} AUTH {event_type} for {user_id} from IP {ip_address}"
            file.write(log_message + "\n")

def generate_privilege_escalation_log(output_file: str, log_count: int):
    """Generates and writes privilege escalation log entries to the specified output file."""
    with open(output_file, 'w') as file:
        for _ in range(log_count):
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            user_id = random.choice(["user1", "user2", "user3"])
            log_message = f"{timestamp} SECURITY Privilege escalation attempt by {user_id}"
            file.write(log_message + "\n")

def generate_sql_injection_log(output_file: str, log_count: int):
    """Generates and writes SQL injection log entries to the specified output file."""
    with open(output_file, 'w') as file:
        for _ in range(log_count):
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ip_address = f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}"
            log_message = f"{timestamp} WEB SQL Injection attempt from IP {ip_address}"
            file.write(log_message + "\n")

def generate_phishing_log(output_file: str, log_count: int):
    """Generates and writes phishing log entries to the specified output file."""
    with open(output_file, 'w') as file:
        for _ in range(log_count):
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            user_id = random.choice(["user1", "user2", "user3"])
            log_message = f"{timestamp} EMAIL Phishing email detected for {user_id}"
            file.write(log_message + "\n")

def generate_ddos_log(output_file: str, log_count: int):
    """Generates and writes DDoS attack log entries to the specified output file."""
    with open(output_file, 'w') as file:
        for _ in range(log_count):
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ip_address = f"10.0.{random.randint(0, 255)}.{random.randint(0, 255)}"
            log_message = f"{timestamp} NETWORK DDoS attack detected from IP {ip_address}"
            file.write(log_message + "\n")
