from checker import Checker

class Check_CIS_2_1_8(Checker):

    def __init__(self, config, verbose=False):
        
        super().__init__(config, verbose)

        self.id = "2.1.8"
        self.title = "Disable static keys for TLS"
        self.levels = [2]
        self.auto = True
        self.benchmark_version = "v1.1.0"
        self.benchmark_author = "CIS"

    def do_check(self):
        config_system_global = self.get_config("system global")

        if "ssl-static-key-ciphers" not in config_system_global.keys():
            self.set_message(f'ssl-static-key-cipher not defined')
            return False

        if not config_system_global["ssl-static-key-ciphers"] == "disable":
            self.set_message(f'ssl-static-key-cipher not disabled')
            return False

        return True
