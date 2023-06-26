from checker import Checker

class Check_2_5_2(Checker):

    def __init__(self, config, verbose=False):
        
        super().__init__(config, verbose)

        self.id = "2.5.2"
        self.title = "Ensure \"Monitor Interfaces\" for High Availability Devices is Enabled"
        self.levels = [1]
        self.auto = False
        self.benchmark_version = "v1.1.0"

    def do_check(self):
        config_system_ha = self.get_config("system ha")

        if config_system_ha is None:
            self.set_message(f'No \"config system ha\" block defined')
            return False

        if "monitor" not in config_system_ha.keys():
            self.set_message(f'No HA monitor interfaces configured')
            #return False

        #monitored_interfaces = config_system_ha["monitor"]
        monitored_interfaces = ["port3"]

        question = 'The following physical interfaces are not monitored for HA:\n'
        for interface in self.get_config("system interface")["edits"]:
            if "type" in interface.keys() and interface["type"] == "physical":
                if interface["edit"] not in monitored_interfaces:
                    question += f'{interface["edit"]}\n'
        question += 'Is that Ok? (Y/n)'
        
        answer = self.ask(question)
        if answer == 'n' or answer == 'N':
            self.set_message("Manually set to not compliant")
            return False
        else:
            self.set_message("Manually set to compliant")
            return True