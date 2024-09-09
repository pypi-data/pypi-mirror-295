import yaml
from app.normal_logs import (
    generate_auth_log,
    generate_syslog_log,
    generate_kern_log,
    generate_daemon_log,
    generate_fail2ban_log
)
from app.suspicious_logs import (
    generate_failed_auth_log,
    generate_privilege_escalation_log,
    generate_sql_injection_log,
    generate_phishing_log,
    generate_ddos_log
)

def generate_logs_from_yaml(config_file_path: str):
    """
    Generate log files based on the configuration provided in a YAML file.
    
    :param config_file_path: Path to the YAML configuration file.
    """
    try:
        with open(config_file_path, 'r') as file:
            config = yaml.safe_load(file)
            log_configs = config.get('logs', [])
            
            # Dictionary mapping log types to functions
            log_generators = {
                'auth': generate_auth_log,
                'syslog': generate_syslog_log,
                'kern': generate_kern_log,
                'daemon': generate_daemon_log,
                'fail2ban': generate_fail2ban_log,
                'failed_auth': generate_failed_auth_log,
                'privilege_escalation': generate_privilege_escalation_log,
                'sql_injection': generate_sql_injection_log,
                'phishing': generate_phishing_log,
                'ddos': generate_ddos_log,
            }
            
            for log_config in log_configs:
                log_type = log_config.get('type')
                output_file = log_config.get('output_file')
                log_count = log_config.get('log_count', 100)  # Default to 100 if not specified

                if log_type not in log_generators:
                    print(f"Unknown log type: {log_type}. Skipping.")
                    continue

                # Call the appropriate log generation function
                log_generators[log_type](output_file, log_count)
                print(f"Generated {log_count} {log_type} logs in {output_file}")
    
    except FileNotFoundError:
        print(f"The configuration file {config_file_path} was not found.")
    except yaml.YAMLError as yaml_error:
        print(f"Error parsing the YAML configuration file: {yaml_error}")
    except Exception as e:
        print(f"An error occurred during log generation: {e}")
        raise
