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
                
    def get_policies(self, srcintfs=None, dstintfs=None, actions=None):
        config_firewall_policy = self.get_config("firewall policy")
        if config_firewall_policy is None:
            return []
        
        policies = config_firewall_policy['edits']

        result = []        
        for policy in policies:
            if srcintfs is not None:
                if policy["srcintf"] not in [x["edit"] for x in srcintfs]:
                    continue
                
            if dstintfs is not None:
                if policy["dstintf"] not in [x["edit"] for x in dstintfs]:
                    continue
                
            if actions is not None:
                if "action" not in policy.keys():
                    continue
                
                if policy["action"] not in actions:
                    continue
            
            result.append(policy)

        return result
    
    def get_ips_sensors(self, names=None):
        config_ips_sensors = self.get_config("ips sensor")
        if config_ips_sensors is None:
            return []
        
        ips_sensors = config_ips_sensors['edits']
        
        result = []
        for ips_sensor in ips_sensors:
            if names is not None:
                if ips_sensor["edit"] not in names:
                    continue
            
            result.append(ips_sensor)
            
        return result
    
    def get_av_profiles(self, names=None):
        config_av_profiles = self.get_config("antivirus profile")
        if config_av_profiles is None:
            return []
        
        av_profiles = config_av_profiles['edits']
        
        result = []
        for av_profile in av_profiles:
            if names is not None:
                if av_profile["edit"] not in names:
                    continue
            
            result.append(av_profile)
            
        return result