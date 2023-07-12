from checker import Checker

class Check_Example_Manual(Checker):

    def __init__(self, firewall, display, verbose=False):
        
        super().__init__(firewall, display, verbose)

        self.id = "1.1.1"
        self.title = "Example Manual Check"
        self.levels = [1, 2]
        self.auto = False
        self.enabled = False # Remove this line to enable
        self.benchmark_author = "Example Org."

    def do_check(self):
        config = self.get_config("system auto-install")

        self.add_question_context("Test Step")

        answer = self.ask("Is it ok? (Y/n)")

        if answer == 'n' or answer == 'N':
            self.set_message("Manually set to not compliant")
            return False
        else:
            self.set_message("Manually set to compliant")
            return True

        return None
