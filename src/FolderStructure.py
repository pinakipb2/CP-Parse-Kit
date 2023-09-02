import os
import shutil
import structlog
from colorama import init, Fore, Style
from utility import add_newline_if_missing

log = structlog.get_logger(__name__)

init(autoreset=True)


class FolderStructure:
    def __init__(self, folder_name, no_of_problems, all_prob_inp_out, problem_url):
        log.info(f"{self.__class__.__name__} Initiated")
        self.folder_name = folder_name
        self.no_of_problems = no_of_problems
        self.all_prob_inp_out = all_prob_inp_out
        self.problem_url = problem_url
        self.author = "Pinaki Bhattacharjee"
        self.github_url = (
            "https://github.com/pinakipb2/competitive-programming-platform-parser"
        )
        self.version = "0.1.0"

    def __generate_log_file(self):
        with open("log.txt", "w", encoding="utf-8") as log_file:
            from datetime import datetime

            current_datetime = datetime.now()
            formatted_datetime = current_datetime.strftime("%d-%m-%Y %H:%M:%S")
            log_file.write(f"Generated Using {self.github_url} v{self.version}\n\n")
            log_file.write(f"Made with 💻💝 by {self.author}\n\n")
            if "codeforces" in self.problem_url:
                log_file.write(
                    f"Generated for Codeforces ({self.folder_name}) on {formatted_datetime}\n\n"
                )
            if "atcoder" in self.problem_url:
                log_file.write(
                    f"Generated for Atcoder ({self.folder_name}) on {formatted_datetime}\n\n"
                )
            log_file.write(f"Happy Coding ✌\n")
        log.info("Log File Generated !")

    def __generate_cpp_files(self):
        for letter in range(ord("a"), ord("a") + self.no_of_problems):
            cpp_filename = chr(letter) + ".cpp"
            with open(cpp_filename, "w") as cpp_file:
                cpp_file.write(f"// File Generated Using: {self.github_url} \n")
                if "codeforces" in self.problem_url:
                    cpp_file.write(
                        f"// Problem URL: {self.problem_url}{chr(letter).upper()}\n\n"
                    )
                if "atcoder" in self.problem_url:
                    cpp_file.write(
                        f"// Problem URL: {self.problem_url}{chr(letter).lower()}\n\n"
                    )
        log.info("CPP Files Created Successfully !")

    def __generate_input_output_files(self):
        index_count = {}
        for prob in self.all_prob_inp_out:
            problem_index = prob["problem_index"]
            input_data, output_data = prob["input_output"]
            if problem_index in index_count:
                index_count[problem_index] += 1
            else:
                index_count[problem_index] = 1
            input_filename = f"{problem_index}{index_count[problem_index]}"
            with open(input_filename, "w") as inp_file:
                input_data = add_newline_if_missing(input_data)
                inp_file.write(input_data)
            output_filename = f"{problem_index}{index_count[problem_index]}.out"
            with open(output_filename, "w") as out_file:
                output_data = add_newline_if_missing(output_data)
                out_file.write(output_data)
        log.info("Written Input and Output Files !")

    def create(self):
        try:
            os.mkdir(self.folder_name)
        except FileExistsError:
            response = input(
                f"{Fore.YELLOW}The folder '{self.folder_name}' already exists.\nDo you want to override it? (y/n): {Style.RESET_ALL}"
            )
            if response.lower() == "n":
                print(f"{Fore.RED}Aborted.{Style.RESET_ALL}")
                return
            elif response.lower() != "y":
                print(f"{Fore.RED}Invalid response. Aborted.{Style.RESET_ALL}")
                return
            shutil.rmtree(self.folder_name)
            os.mkdir(self.folder_name)

        log.info(f"Folder {self.folder_name} Created Successfully !")
        os.chdir(self.folder_name)

        self.__generate_cpp_files()
        self.__generate_input_output_files()
        self.__generate_log_file()

        log.info("Opening VSCode ...")
        os.system("code .")

        # Start watcher
