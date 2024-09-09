import unittest
import os
from app.normal_logs import (
    generate_auth_log,
    generate_syslog_log,
    generate_kern_log,
    generate_daemon_log,
    generate_fail2ban_log
)

class TestNormalLogs(unittest.TestCase):

    def setUp(self):
        """Setup temporary directory for test logs."""
        os.makedirs('./test_logs', exist_ok=True)

    def test_generate_auth_log(self):
        output_file = './test_logs/auth.log'
        generate_auth_log(output_file, 1)
        with open(output_file, 'r') as file:
            log = file.read()
        self.assertIn("AUTH", log)
        self.assertIn("Accepted password", log)
        self.assertIn("IP", log)

    def test_generate_syslog_log(self):
        output_file = './test_logs/syslog.log'
        generate_syslog_log(output_file, 1)
        with open(output_file, 'r') as file:
            log = file.read()
        self.assertTrue(any(level in log for level in ["INFO", "NOTICE"]))
        self.assertIn(":", log)

    def test_generate_kern_log(self):
        output_file = './test_logs/kern.log'
        generate_kern_log(output_file, 1)
        with open(output_file, 'r') as file:
            log = file.read()
        self.assertIn("KERNEL", log)
        self.assertTrue(any(level in log for level in ["INFO", "NOTICE"]))
        self.assertIn(":", log)

    def test_generate_daemon_log(self):
        output_file = './test_logs/daemon.log'
        generate_daemon_log(output_file, 1)
        with open(output_file, 'r') as file:
            log = file.read()
        self.assertIn("DAEMON", log)
        self.assertIn("Service", log)

    def test_generate_fail2ban_log(self):
        output_file = './test_logs/fail2ban.log'
        generate_fail2ban_log(output_file, 1)
        with open(output_file, 'r') as file:
            log = file.read()
        self.assertIn("FAIL2BAN", log)
        self.assertIn("IP", log)
        self.assertIn("Unban", log)

    def tearDown(self):
        """Clean up temporary test log files."""
        log_files = [
            './test_logs/auth.log',
            './test_logs/syslog.log',
            './test_logs/kern.log',
            './test_logs/daemon.log',
            './test_logs/fail2ban.log'
        ]
        for log_file in log_files:
            if os.path.exists(log_file):
                os.remove(log_file)
        os.rmdir('./test_logs')

if __name__ == '__main__':
    unittest.main()
