import os
import importlib

class PluginManager:
    def __init__(self, plugin_folder):
        self.plugin_folder = plugin_folder
        self.plugins = {}

    def load_plugins(self, inp):
        plugin_files = [file for file in os.listdir(self.plugin_folder) if file.endswith('.py') and file != '__init__.py']
        
        if not inp in [plugin[:-3].lower() for plugin in plugin_files]:
            print(f"Plugin {inp} not found")
            exit(1)
            
        inp = [inp.capitalize()+".py"]
        
        # for plugin_file in plugin_files:
        for plugin_file in inp:
            plugin_name = os.path.splitext(plugin_file)[0]
            module_path = f'{self.plugin_folder}.{plugin_name}'
            
            try:
                module = importlib.import_module(module_path)
                plugin_class = getattr(module, f'{plugin_name}Parser')
                print(f"Loading plugin: {plugin_name}")
                self.plugins[plugin_name] = plugin_class(100)
            except Exception as e:
                print(f"Error loading plugin {plugin_name}: {e}")

    def get_plugins(self):
        return self.plugins
        

# Load and create plugin objects
plugin_manager = PluginManager('PlatformParser')  # Assuming the folder name is PlatformParser
inp = input("Enter plugin name: ")
plugin_manager.load_plugins(inp)
plugins = plugin_manager.get_plugins()

# Execute plugin actions
for plugin_name, plugin_obj in plugins.items():
    print(f"Running plugin: {plugin_name}")
    # plugin_obj.perform_action()
