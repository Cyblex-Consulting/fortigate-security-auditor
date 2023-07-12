import re

class Checker:

    def __init__(self, config, verbose=False):
        self.config = config
        self.verbose = verbose
        self.message = None
        self.manual_entry = False
        self.auto = True
        self.enabled = True
        self.levels = None
        self.benchmark_author = None
        self.question = None

    def __lt__(self, other):
        return self.id < other.id

    def is_valid(self):

        if self.id is None:
            print(f'[!] Error in {self.__class__.__name__}: Check id is not defined')
            return False
        if self.title is None:
            print(f'[!] Error in {self.__class__.__name__}: Check title is not defined')
            return False
        if self.levels is None or len(self.levels) == 0:
            print(f'[!] Error in {self.__class__.__name__}: Levels are not defined')
            return False
        if self.benchmark_author is None or len(self.benchmark_author) == 0:
            print(f'[!] Error in {self.__class__.__name__}: Benchmark author is not defined')
            return False

        return True

    def is_level_applicable(self, levels):
        # Checks it the level asked by the operator is applicable to this check
        for level in levels:
            if int(level) in self.levels:
                return True
        return False

    def print_verbose(self, content):
            print(f'\t| {content}')

    def restore_from_cache(self, cached_result):
        self.result = cached_result["result"]
        self.message = cached_result["message"]
        self.question = cached_result["question"]
        print(f'[{self.get_id()}] {self.title}', end='')
        print(f' : {self.result}')
        if self.verbose and self.question is not None:
            for line in self.question:
                print('\t| ' + line)
        if self.verbose and self.message is not None:
            for line in self.message:
                print('\t| ' + line)

    def skip(self):
        print(f'[{self.get_id()}] {self.title} : SKIP')
        self.result = 'SKIP'

    def run(self):
        
        if not self.is_valid():
            return False

        print(f'[{self.get_id()}] {self.title}', end='')
        self.success = self.do_check()

        if self.success is None:
            self.result = 'UNDF'
        else:
            if self.manual_entry:
                print(f'[{self.get_id()}] {self.title}', end='')

            if self.success:
                self.result = 'PASS'
            else:
                self.result = 'FAIL'
        print(f' : {self.result}')

        if self.verbose and self.message is not None:
            for line in self.message:
                print('\t| ' + line)

    def ask(self, question):
        self.manual_entry = True
        self.question = [question]
        print('\n\t| --------------[ Question ] --------------------')
        print('\t| ' + question.replace("\n", "\n\t| ") + ":", end = '')
        answer = input()
        print('\t| -----------------------------------------------')
        return answer

    def set_message(self, message):
        self.message = [message]

    def add_message(self, message):
        if self.message is None:
            self.message = []
        self.message.append(message)

    def get_id(self):
        return self.id

    def get_result(self):
        return self.result
    
    def get_title(self):
        return self.title
    
    def get_id(self):
        return f'{self.benchmark_author}-{self.id}'
    
    def get_log(self):
        if self.question is not None:
            log = "\n".join(self.question)
            log += "\n"
            log += "\n".join(self.message)
        else:
            log = "\n".join(self.message)
        return log

    # Helper function to get the correct config bloc in config dict
    def get_config(self, chapter=None):
        if chapter is None:
            return self.config
        else:
            for block in self.config:
                if "config" in block.keys() and block["config"] == chapter:
                    return block
            return None

    # Helper function to check if param is an IP
    def is_ip(self, param):
        if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",param):
            return True
        else:
            return False

    # Helper function to check if param is a valid hostname or FQDN
    def is_fqdn(self, param):
        if re.match(r"^(?!:\/\/)(?=.{1,255}$)((.{1,63}\.){1,127}(?![0-9]*$)[a-z0-9-]+\.?)$",param):
            return True
        else:
            return False
