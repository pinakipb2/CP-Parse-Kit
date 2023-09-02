import os
import re
# import importlib

def is_valid_platform_file_name(input_str):
    pattern = r"^[A-Z][a-z]*([A-Z][a-z]*)*\.py$"
    return re.match(pattern, input_str) is not None

class PlatformValidator:
    def __init__(self, platform_folder):
        self.platform_folder = platform_folder
        self.platforms = {}

    def validate(self):
        platform_files = [file for file in os.listdir(self.platform_folder) if file.endswith('.py') and file != '__init__.py']
        
        print("Platforms found", platform_files)
        
        for string in platform_files:
          if not is_valid_platform_file_name(string):
            print(f"The platform '{string}' does not follow Platform Naming Rules")
            exit(1)
        
        
        # if not inp in [plugin[:-3].lower() for plugin in plugin_files]:
        #     print(f"Plugin {inp} not found")
        #     exit(1)
            
        # inp = [inp.capitalize()+".py"]
        
        # # for plugin_file in plugin_files:
        # for plugin_file in inp:
        #     plugin_name = os.path.splitext(plugin_file)[0]
        #     module_path = f'{self.plugin_folder}.{plugin_name}'
            
        #     try:
        #         module = importlib.import_module(module_path)
        #         plugin_class = getattr(module, f'{plugin_name}Parser')
        #         print(f"Loading plugin: {plugin_name}")
        #         self.plugins[plugin_name] = plugin_class(100)
        #     except Exception as e:
        #         print(f"Error loading plugin {plugin_name}: {e}")

 
platform_manager = PlatformValidator('PlatformParser')
platform_manager.validate()