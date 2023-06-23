from checker import Checker

class Check_3_2(Checker):

    def __init__(self, config, verbose=False):
        
        super().__init__(config, verbose)

        self.id = "3.2"
        self.title = "Ensure that policies do not use \"ALL\" as Service"
        self.levels = [1]
        self.auto = True
        self.benchmark_version = "v1.1.0"

    def do_check(self):
        config_firewall_policy = self.get_config("firewall policy")

        if config_firewall_policy is None:
            self.set_message(f'No \"config firewall policy\" block defined')
            return False

        fail = False
        
        if len(config_firewall_policy['edits']) > 0:
            for edit in config_firewall_policy['edits']:
                if edit['service'] == 'ALL':
                    fail = True
                    self.add_message(f'The policy {edit["uuid"]} is not compliant:')
                    self.add_message(f'\tname: {edit["name"]}')
                    self.add_message(f'\tsrcintf: {edit["srcintf"]}')
                    self.add_message(f'\tdstintf: {edit["dstintf"]}')
                    self.add_message(f'\tsrcaddr: {edit["srcaddr"]}')
                    self.add_message(f'\tdstaddr: {edit["dstaddr"]}')
                    self.add_message(f'\taction: {edit["action"]}')
            fail = True
        else:
            self.add_message('There is no policy defined')

        if not fail:
            self.add_message('There is no policy with set service ALL')

        return not fail
