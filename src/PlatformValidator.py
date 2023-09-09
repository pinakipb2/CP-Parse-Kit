import os
import re
import inspect

class PlatformValidator:
    def __init__(self, platform_folder, user_platform_name, contest_id):
        self.platform_folder = platform_folder
        self.platform = ""
        self.module_path = ""
        self.user_platform_name = user_platform_name
        self.contest_id = contest_id
        self.__initiate_validator()

    def __is_valid_platform_file_name(self, input_str):
        pattern = r"^[A-Z][a-z]*([A-Z][a-z]*)*\.py$"
        return re.match(pattern, input_str) is not None

    def __create_instance(self):
        print(f"Loading plugin: {self.platform}")
        
        class_object = globals()[self.platform]
        if self.platform in globals():
            instance = class_object(self.contest_id)  # Call the constructor with the value argument
            return instance
        else:
            raise ValueError(f"Class '{self.platform}' not found")

    def __validate(self):
        required_methods = ['get_input_and_output', 'get_problem_url', 'no_of_problems']
        required_properties = ['contest_id', 'contest_url', 'problem_url', 'contest_response']

        platform_instance = self.__create_instance()
        
        # Check all the functions
        all_class_members = inspect.getmembers(platform_instance)
        callable_members = [member for member in all_class_members if callable(member[1])]
        methods = [members[0] for members in callable_members]
        is_missing = set(required_methods) - set(methods)
        if is_missing:
            raise Exception(f"Missing Method(s): {is_missing}")

        # Check all the properties
        properties = list(vars(platform_instance).keys())
        is_missing = set(required_properties) - set(properties)
        if is_missing:
            raise Exception(f"Missing Variable(s): {is_missing}")

    def __initiate_validator(self):
        all_platform_files = [file for file in os.listdir(self.platform_folder) if file.endswith('.py') and file != '__init__.py']
        print("Platforms found:", all_platform_files)

        for string in all_platform_files:
            if not self.__is_valid_platform_file_name(string):
                print(f"The platform '{string}' does not follow Platform Naming Rules")
                exit(1)

        if not self.user_platform_name.lower() in [plugin[:-3].lower() for plugin in all_platform_files]:
            print(f"Plugin {self.user_platform_name} not found")
            exit(1)

        self.user_platform_name = self.user_platform_name.capitalize()
        self.module_path = f"{self.platform_folder}.{self.user_platform_name}"
        class_name = f"{self.user_platform_name}Parser"

        try:
            exec(f"from {self.module_path} import {class_name}", globals())
            self.platform = f"{class_name}"
            self.__validate()
        except Exception as e:
            print(f"Error loading plugin {self.user_platform_name}: {e}")

# Debugging -
# platform_manager = PlatformValidator('PlatformParser', 'Atcoder', 100)