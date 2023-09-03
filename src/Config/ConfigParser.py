import json

class ConfigParser:
    def __init__(self, platform_name):
        self.config_file_path = "Config.json"
        self.platform_name = platform_name.capitalize()
        self.config_file_data = None
        # reading config file data - 
        try:
            file = open(self.config_file_path)
            config_json_data = json.load(file)

            # setting config_file_data to the required platform_name -
            for platform in config_json_data['Platforms']:
                if self.platform_name in platform:
                    self.config_file_data = platform[self.platform_name]
                    break
            
            if self.config_file_data is None:
                raise Exception(f"Config for Platform: {self.platform_name} not found!")
      
        except Exception as e:
            print('Error:', e)
            exit(1)

    def check_config(self):
        # precheck parameters -
        required_params = [
            "language_extension",
            "execution_command"
        ]
        optional_params = {
            "folder_scaffold_path": "",
            "compilation_command": "",
            "enable_watchman": False,
            "template_code_path": "",
            "input_file_extension": "",
            "output_file_extension": "out",
            "default_number_of_file": 10
        }

        # checking required parameters -
        if "required" in self.config_file_data:
            for parameter in required_params:
                if parameter not in self.config_file_data["required"] or self.config_file_data["required"][parameter] == "":
                    print(f"Required Parameter: {parameter} for Platform: {self.platform_name} not defined!")
                    exit(1)
        else:
            print(f"Required Config for Platform: {self.platform_name} not defined!")
            exit(1)

        # updating optional parameters -
        if "optional" in self.config_file_data:
            for parameter in optional_params:
                if parameter in self.config_file_data['optional']:
                    continue
                self.config_file_data['optional'][parameter] = optional_params[parameter]
        else:
            self.config_file_data['optional'] = optional_params
        
        # print(json.dumps(self.config_file_data, indent=2))
        return self.config_file_data
        
# Debugging      
# obj = ConfigParser('atcoder')
# data = obj.check_config()