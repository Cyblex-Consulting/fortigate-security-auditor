# fortigate-security-auditor
Tool to check a fortigate configuration with the CIS Benchmark.

## Preparing the configuration

Parsing is done internally with this project: https://github.com/ssato/fortios-xutils

It shall be installed with `pip install fortios_xutils`.

**Note :** The parsing may fail if the config contains non utf-8 characters. A quick fix has been implemented in the tool with the `--autofix` flag that may result in non standard characters being removed.

## Running the benchmark

```
usage: fortigate-security-auditor.py [-h] [-q] [-v] [-j] [-o OUTPUT] [-l LEVELS [LEVELS ...]] [-i IDS [IDS ...]] [-c] [-w WAN [WAN ...]] [--interfaces] [--zones] [--autofix] config

Apply a benchmark to a Fortigate configuration file. Example: fortigate-security-auditor.py -q -o results.csv -l 1 2 -w WAN1 WAN2 --autofix firewall.conf

positional arguments:
  config                Configuration file exported from the fortigate or fortimanager

optional arguments:
  -h, --help            show this help message and exit
  -q, --quiet           Not interactive: ignore manual steps
  -v, --verbose         Increase verbosity
  -j, --json            Input file is json already parsed by fortios_xutils
  -o OUTPUT, --output OUTPUT
                        Output CSV File
  -l LEVELS [LEVELS ...], --levels LEVELS [LEVELS ...]
                        Levels to check. (default: 1)
  -i IDS [IDS ...], --ids IDS [IDS ...]
                        Checks id to perform. (default: all if applicable)
  -c, --resume          Resume an audit that was already started. Automatic items are re-checked but manually set values are retrieved from cache.
  -w WAN [WAN ...], --wan WAN [WAN ...]
                        List of wan interfaces separated by spaces (example: --wan port1 port2)
  --interfaces          Show list of interfaces and exit
  --zones               Show list of zones and exit
  --autofix             Automatically try to fix errors in input file
```

The tool implements some basic caching. When a benchmark is run, the result is saved in `~/.cache/fortigate-security-auditor.json`. The config file path is used to discriminate the various banchmarks performed in the cache file.

By default, re-running the tool will overwrite the cache and so do not use it. Adding `-c` or `--resume` will reload previous results from the cache. Only manual step results are recovered from the cache. **Automatic checks are re-run anyway.**

## Adding checks

### Implementation prerequisites

To add a new benchmark, create a subfolder in the `checks` directory. Then in the benchmark folder, it check is an independant python file which needs to specify the `checker` parent class. 2 examples are given as a start in the `checks\examples` benchmark folder.

Mandatory subclass variables are:

- `self.id`: Reference for the requirement (in the benchmark)
- `self.title`: Title for the requirement
- `self.levels`: List of levels applicable for the requirement
- `self.auto`: True if the check does not need the operator to review and assess himself if this is compliant
- `self.benchmark_version`: The benchmark version which was used to implement the check
- `self.benchmark_author`: The benchmark author

The function `do_check()` needs to be implemented. It shall return:
- `True` if the check passed
- `False` if the check failed
- `None` if for some reason the check was not performed (for instance, not fully implemented). The check will be marked as `SKIP` in the results

When run in verbose mode, the tool will print messages, they are configured in the checker and displayed when it is finished. The following function are used:
- `self.set_message(text)`: Configure the message. If the function is run twice, the last message overwrites the previous one.
- `self.add_message(text)`: Add a new line to the existing message. If no message exists, it creates it so it may be used instead of `set_message` even in case of single message output.

For non automatic checks where the operator needs to state if it is ok or not, the checker parent class has some helper functions in the same spirit as self.set_message or add_message
- `self.ask(question)` : Takes in argument a string (can contain `\n`) and displays it. Then wait for user input and returns the typed characters
Implementation on how the answer shall be processed before returning `True` or `False` is left to the check developper.
- `self.add_question_context(string)` : For more complex use case, it is possible to generate the question in an easy way by appending strings to the question context. This method can be called multiple times, each time will add a new line to the context.
- `self.ask_if_correct()` : This method displays the context and directly ask the user wheter he validates the requirement or not.

A few helpers can be used in checks:
- `self.get_config(chapter = None)`: Returns a dictionnary of a single configuration block, or the full config
- `self.get_interfaces()`: Returns a list of all the firewall interfaces
- `self.get_zones()`: Returns a list of all the firewall zones
- `self.get_wan_interfaces()`: Returns a list of all the firewall WAN interfaces. If it was configured via the `--wan` flag then it is returned directly. If not, the user is showed the list of interfaces and ask to choose which one are WAN.
- `self.get_policies(srcintfs=None, dstintfs=None, actions=None)`: Returns a list of all the firewall policies. Some filters can be applied.
- `self.get_ips_sensors(names=None)`: Returns a list of all the IPS sensors. Some filters can be applied.
- `self.get_av_profiles(names=None)`: Returns a list of all the IPS sensors. Some filters can be applied.
- `self.get_dnsfilter_profiles(names=None)`: Returns a list of all the DNS profiles. Some filters can be applied.
- `self.get_appcontrol_profiles(names=None)`: Returns a list of all the App Control profiles. Some filters can be applied.
- `self.is_ip(param)`: Checks if `param` is an IP format
- `self.is_fqdn(param)`: Checks if `param` is compliant with a valid FQDN format
- `self.get_service_groups_containing_protocols(protocols=None)`: Returns all service groups that includes a protocol (for instance "Windows AD" is returned when protocols = ["DNS"])

### Example

Here is a single example automatic checker:

```python
from checker import Checker

class Check_Example_Manual(Checker):

    def __init__(self, firewall, display, verbose=False):

        super().__init__(firewall, display, verbose)

        self.id = "1.1.2"
        self.title = "Example Auto Check"
        self.levels = [1, 2]
        self.auto = True
        self.enabled = False # Remove this line to enable
        self.benchmark_author = "Example Org."

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

        self.set_message(f'{config_system_dns["primary"]} {config_system_dns["secondary"]}')

        return True
```
