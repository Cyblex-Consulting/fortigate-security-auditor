# fortigate-security-auditor
Tool to check a fortigate configuration with the CIS Benchmark.

## Preparing the configuration

First step is to create a json file from the plain configuration extracted from the Fortigate.
```
fortios_xutils parse firewall.conf
```
This will create several files in the `out/` repository. The one which will be used is `all.json`

## Running the benchmark

```
usage: fortigate-security-auditor.py [-h] [-q] [-v] [-o OUTPUT] [-c] config

Apply a benchmark to a Fortigate configuration file. Example: fortigate-security-auditor.py
-q data.json

positional arguments:
  config                if single argument: combine all lines, if multiple arguments: combine
                        lines from all files

optional arguments:
  -h, --help            show this help message and exit
  -q, --quiet           Not interactive: ignore manual steps
  -v, --verbose         Increase verbosity
  -o OUTPUT, --output OUTPUT
                        Output CSV File
  -c, --resume          Resume an audit that was already started. Automatic items are re-
                        checked but manually set values are retrieved from cache.
```

The tool implements some basic caching. When a benchmark is run, the result is saved in `~/.cache/fortigate-security-auditor.json`. The config file path is used to discriminate the various banchmarks performed in the cache file.

By default, re-running the tool will overwrite the cache and so don't use it. Adding `-c` or `--resume` will reload previous results from the cache. Only manual step results are recovered from the cache. Automatic checks are re-run anyway.

## Adding checks

### Implementation prerequisites

Each requirement check is an independant python file in the `checks` subfolder. It needs to specify the `checker` parent class. 2 examples are given as a start in the folder.

Mandatory subclass variables are:

- `self.id`: CIS Reference for the requirement
- `self.title`: CIS Title for the requirement
- `self.levels`: List of CIS levels applicable for the requirement
- `self.auto`: True if the check does not need the operator to review and assess himself if this is compliant
- `self.benchmark_version`: The CIS Benchmark version which was used to implement the check

The function `do_check()` needs to be implemented. It shall return:
- `True` if the check passed
- `False` if the check failed
- `None` if for some reason the check was not performed (for instance, not fully implemented). The check will be marked as SKIP in the results

When run in verbose mode, the tool will print messages, they are configured in the checker and displayed when it is finished. The following function are used:
- `self.set_message(text)`: Configure the message. If the function is run twice, the last message overwrites the previous one.
- `self.add_message(text)`: Add a new line to the existing message. If no message exists, it creates it so it may be used instead of `set_message` even in case of single message output.

For non automatic checks where the operator needs to state if it is ok or not, the checker parent class has some helper functions in the same spirit as self.set_message or add_message
- `self.ask(question)` : Takes in argument a string (can contain `\n`) and displays it. Then wait for user input and returns the typed characters
Implementation on how the answer shall be processed before returning `True` or `False` is left to the check developper.

A few helpers can be used in checks:
- `self.get_config(chapter = None)`: Returns a dictionnary of a single configuration block, or the full config
- `self.is_ip(param)`: Checks if `param` is an IP format
- `self.is_fqdn(param)`: Checks if `param` is compliant with a valid FQDN format

### Example

Here is a single example automatic checker:

```python
from checker import Checker

class Check_1_1(Checker):

    def __init__(self, config, verbose=False):
        
        super().__init__(config, verbose)

        self.id = "1.1"
        self.title = "Ensure DNS server is configured"
        self.levels = [1]
        self.auto = True
        self.benchmark_version = "v1.1.0"

    def do_check(self):
        config_system_dns = self.get_config("system dns")

        if "primary" not in config_system_dns.keys():
            self.set_message(f'No primary DNS configured')
            return False

        if not self.is_ip(config_system_dns["primary"]):
            self.set_message(f'{config_system_dns["primary"]} is not a valid IP for primary DNS')
            return False

        if "secondary" not in config_system_dns.keys():
            self.set_message(f'No secondary DNS configured')
            return False

        if not self.is_ip(config_system_dns["secondary"]):
            self.set_message(f'{config_system_dns["secondary"]} is not a valid IP for secondary DNS')
            return False

        self.add_message(f'{config_system_dns["primary"]}')
        self.add_message(f'{config_system_dns["secondary"]}')

        return True
```
