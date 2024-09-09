# LogCrafter

[![pip version](https://badge.fury.io/py/log-crafter.svg)](https://badge.fury.io/py/log-crafter)
[![Build Status](https://github.com/leoteissier/log-crafter/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/leoteissier/log-crafter/actions)

LogCrafter is a Python library designed to generate both normal and suspicious log files. It is built to simulate real-world environments by creating diverse log files, which can be particularly useful for training AI in intrusion detection systems.

## Features

- Generation of authentication logs (auth.log)
- Generation of syslog logs (syslog.log)
- Generation of failed authentication logs (failed_auth.log)
- Generation of logs for privilege escalation, SQL injection, phishing, and DDoS attacks
- Configuration via a YAML file to specify the type of log, output file, and number of logs to generate

## Installation

You can install LogCrafter directly from PyPI (coming soon) or by cloning this repository.

```bash
pip install logcrafter
```

## Usage

### Configuration

Create a YAML configuration file, such as logs_config.yml, to specify the types of logs you want to generate:

```yaml
logs:
  - type: "auth"
    output_file: "./logs/auth.log"
    log_count: 1000

  - type: "failed_auth"
    output_file: "./logs/failed_auth.log"
    log_count: 100
```

### Generating Logs

Use the LogCrafter CLI to generate logs based on your configuration file:

```bash
python -m app.main config/logs_config.yml
```

### Example Log Configuration

Below is an example of a more comprehensive YAML configuration file to showcase the different types of logs that LogCrafter can generate:

```yaml
logs:
  - type: "auth"
    output_file: "./logs/auth.log"
    log_count: 1000

  - type: "syslog"
    output_file: "./logs/syslog.log"
    log_count: 1000

  - type: "failed_auth"
    output_file: "./logs/failed_auth.log"
    log_count: 500

  - type: "privilege_escalation"
    output_file: "./logs/privilege_escalation.log"
    log_count: 200

  - type: "sql_injection"
    output_file: "./logs/sql_injection.log"
    log_count: 300

  - type: "phishing"
    output_file: "./logs/phishing.log"
    log_count: 150

  - type: "ddos"
    output_file: "./logs/ddos.log"
    log_count: 400
```

### Running Tests

To ensure that everything is working correctly, run the included unit tests:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

### Contributing

Contributions are welcome! If you'd like to contribute to LogCrafter, please follow these steps:

- Fork the repository.
- Create a new branch (git checkout -b feature-branch-name).
- Make your changes and commit them (git commit -m 'Add new feature').
Push to the branch (git push origin feature-branch-name).
- Open a pull request.

### Troubleshooting

- No logs generated: Ensure your YAML configuration file is correctly formatted and that paths are correct.
- Missing dependencies: Install required dependencies using pip install -r requirements.txt.
- Permission issues: Run the script with appropriate permissions if writing to system directories.

### License

LogCrafter is open-source software licensed under the MIT License.
