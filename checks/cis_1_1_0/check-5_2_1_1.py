from checker import Checker

class Check_CIS_5_2_1_1(Checker):

    def __init__(self, firewall, display, verbose=False):
        
        super().__init__(firewall, display, verbose)
        
        self.id = "5.2.1.1"
        self.title = "Ensure Security Fabric is Configured"
        self.levels = [1]
        self.auto = True
        self.benchmark_version = "v1.1.0"
        self.benchmark_author = "CIS"

    def do_check(self):
        self.add_message('Not implemented')
        return None