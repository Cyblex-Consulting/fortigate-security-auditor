from checker import Checker

class Check_CIS_1_2(Checker):

    def __init__(self, config, verbose=False):
        
        super().__init__(config, verbose)

        self.id = "1.2"
        self.title = "Ensure intra-zone traffic is not always allowed"
        self.levels = [1]
        self.auto = False
        self.benchmark_version = "v1.1.0"
        self.benchmark_author = "CIS"

    def do_check(self):
        config = self.get_config("system zone")

        if config is None:
            self.set_message("No zone seems to be configured so we consider passed.")
            return True

        # TODO Perform Check
        self.set_message(" Not Implemented")
        return None
