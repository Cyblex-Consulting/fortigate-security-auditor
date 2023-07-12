from checker import Checker

class Check_CIS_2_1_6(Checker):

    def __init__(self, firewall, display, verbose=False):
        
        super().__init__(firewall, display, verbose)

        self.id = "2.1.6"
        self.title = "Ensure the latest firmware is installed"
        self.levels = [2]
        self.auto = False
        self.benchmark_version = "v1.1.0"
        self.benchmark_author = "CIS"

    def do_check(self):
        config = self.get_config()

        for block in config:
            if "config-version" in block.keys():
                config_system_status = block
                break

        self.add_question_context(f'Reported firmware is {config_system_status["config-version"]}.')
        self.add_question_context(f'Go to https://docs.fortinet.com/upgrade-tool and check that if is the latest version.')
        answer=self.ask("Is it the latest version and is it still supported? (Y/n)")

        if answer == 'n' or answer == 'N':
            self.set_message("Manually set to not compliant")
            return False
        else:
            self.set_message("Manually set to compliant")
            return True

        return None
