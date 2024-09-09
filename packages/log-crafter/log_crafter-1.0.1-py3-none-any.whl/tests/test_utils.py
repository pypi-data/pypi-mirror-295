import unittest
import os
from app.utils import generate_logs_from_yaml

class TestUtils(unittest.TestCase):

    def setUp(self):
        """
        Setup method to create necessary directories and files before each test.
        """
        # Ensure the directory for generated logs exists
        os.makedirs('./logs', exist_ok=True)

    def test_generate_logs_from_yaml(self):
        """
        Test the log generation function using the actual example YAML configuration.
        """
        # Define the path to the actual YAML configuration file
        config_file_path = './config/example_logs_config.yml'
        
        # Generate logs using the actual config file
        generate_logs_from_yaml(config_file_path)

        # List of expected log files as per the provided YAML configuration
        expected_log_files = [
            './logs/auth.log',
            './logs/syslog.log',
            './logs/kern.log',
            './logs/daemon.log',
            './logs/fail2ban.log',
            './logs/failed_auth.log',
            './logs/privilege_escalation.log',
            './logs/sql_injection.log',
            './logs/phishing.log',
            './logs/ddos.log'
        ]

        # Check if all expected log files were created
        for log_file in expected_log_files:
            self.assertTrue(os.path.exists(log_file), f"Log file {log_file} was not created.")

    def tearDown(self):
        """
        Cleanup method to remove any files or directories after each test.
        """
        log_files = [
            './logs/auth.log',
            './logs/syslog.log',
            './logs/kern.log',
            './logs/daemon.log',
            './logs/fail2ban.log',
            './logs/failed_auth.log',
            './logs/privilege_escalation.log',
            './logs/sql_injection.log',
            './logs/phishing.log',
            './logs/ddos.log'
        ]

        for log_file in log_files:
            if os.path.exists(log_file):
                os.remove(log_file)

if __name__ == '__main__':
    unittest.main()
