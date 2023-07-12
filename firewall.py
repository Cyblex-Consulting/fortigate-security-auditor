class Firewall:
    
    def __init__(self, config, display, verbose=False):
        self.config = config
        self.wan_interfaces = None
        self.display = display
    
    # Helper function to get the correct config bloc in config dict
    def get_config(self, chapter=None):
        if chapter is None:
            return self.config
        else:
            for block in self.config:
                if "config" in block.keys() and block["config"] == chapter:
                    return block
            return None
    
    def get_interfaces(self):
        config_system_interface = self.get_config("system interface")
        interfaces = config_system_interface["edits"]
        return interfaces
        
    def get_wan_interfaces(self):
        if self.wan_interfaces is None:
            question_context = []
            question_context.append('All these interfaces exist on the device:')
            interfaces = self.get_interfaces()
            for interface in interfaces:
                name = interface["edit"]
                question_context.append(f'{name}')
            answer = self.display.ask(question_context, "Enter the WAN interfaces, comma separated (for instance: port1,port2)")
                        
            self.set_wan_interfaces(answer.replace(" ", "").split(","))    
        
        return self.wan_interfaces
    
    def set_wan_interfaces(self, interfaces_names):
        self.wan_interfaces = []
        
        for interface in self.get_interfaces():
            if interface["edit"] in interfaces_names:
                self.wan_interfaces.append(interface)