import unittest
import os
from app.suspicious_logs import (
    generate_failed_auth_log,
    generate_privilege_escalation_log,
    generate_sql_injection_log,
    generate_phishing_log,
    generate_ddos_log
)

class TestSuspiciousLogs(unittest.TestCase):

    def setUp(self):
        """Setup temporary directory for test logs."""
        os.makedirs('./test_logs', exist_ok=True)

    def test_generate_failed_auth_log(self):
        output_file = './test_logs/failed_auth.log'
        generate_failed_auth_log(output_file, 1)
        with open(output_file, 'r') as file:
            log = file.read()
        self.assertIn("AUTH", log)
        self.assertIn("Failed password", log)
        self.assertIn("IP", log)

    def test_generate_privilege_escalation_log(self):
        output_file = './test_logs/privilege_escalation.log'
        generate_privilege_escalation_log(output_file, 1)
        with open(output_file, 'r') as file:
            log = file.read()
        self.assertIn("SECURITY", log)
        self.assertIn("Privilege escalation", log)

    def test_generate_sql_injection_log(self):
        output_file = './test_logs/sql_injection.log'
        generate_sql_injection_log(output_file, 1)
        with open(output_file, 'r') as file:
            log = file.read()
        self.assertIn("WEB", log)
        self.assertIn("SQL Injection", log)
        self.assertIn("IP", log)

    def test_generate_phishing_log(self):
        output_file = './test_logs/phishing.log'
        generate_phishing_log(output_file, 1)
        with open(output_file, 'r') as file:
            log = file.read()
        self.assertIn("EMAIL", log)
        self.assertIn("Phishing", log)

    def test_generate_ddos_log(self):
        output_file = './test_logs/ddos.log'
        generate_ddos_log(output_file, 1)
        with open(output_file, 'r') as file:
            log = file.read()
        self.assertIn("NETWORK", log)
        self.assertIn("DDoS attack", log)
        self.assertIn("IP", log)

    def tearDown(self):
        """Clean up temporary test log files."""
        log_files = [
            './test_logs/failed_auth.log',
            './test_logs/privilege_escalation.log',
            './test_logs/sql_injection.log',
            './test_logs/phishing.log',
            './test_logs/ddos.log'
        ]
        for log_file in log_files:
            if os.path.exists(log_file):
                os.remove(log_file)
        os.rmdir('./test_logs')

if __name__ == '__main__':
    unittest.main()
