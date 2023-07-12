from checker import Checker

class Check_CIS_3_1(Checker):

    def __init__(self, config, verbose=False):
        
        super().__init__(config, verbose)

        self.id = "3.1"
        self.title = "Ensure that unused policies are reviewed regularly"
        self.levels = [2]
        self.auto = False
        self.enabled = True
        self.benchmark_version = "v1.1.0"
        self.benchmark_author = "CIS"


    def do_check(self):

        question = 'Unused policy shall be checked manually by resetting the counters and then checking which rule never matched.'
        question += 'Was that performed and the result was satisfactory? (Y/n)'
        
        answer = self.ask(question)
        if answer == 'n' or answer == 'N':
            self.set_message("Manually set to not compliant")
            return False
        else:
            self.set_message("Manually set to compliant")
            return True
