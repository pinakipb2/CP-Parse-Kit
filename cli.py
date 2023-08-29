import argparse
from colorama import init, Fore, Style
from enum import Enum
from PlatformParser.Atcoder import AtcoderParser
from PlatformParser.Codeforces import CodeforcesParser
from FolderStructure import FolderStructure
import structlog

log = structlog.get_logger(__name__)

init(autoreset=True)

class Platform(Enum):
    CODEFORCES = "codeforces"
    ATCODER = "atcoder"

def main():
    parser = argparse.ArgumentParser(description=f"{Fore.LIGHTGREEN_EX}Competitive Programming Platform Parser (Made by Pinaki Bhattacharjee){Style.RESET_ALL}")
    parser.add_argument('platform', choices=[platform.value for platform in Platform], help='Enter Platform')
    parser.add_argument('contestID', type=int, help='Contest ID (E.g: 1812) [Must be Integer]')
    parser.add_argument("-w", "--watch", action="store_true", help="Enable Watch Mode (Compile on File Change)")
    
    args = parser.parse_args()
    
    if args.platform == Platform.ATCODER.value:
      atcoderParserObj = AtcoderParser(args.contestID)
      all_prob_inp_out = atcoderParserObj.get_input_and_output()
      folder_name = f"abc_{args.contestID}"
      no_of_problems = atcoderParserObj.no_of_problems()
      problem_url = atcoderParserObj.get_problem_url()
      folderStructureObj = FolderStructure(folder_name, no_of_problems, all_prob_inp_out, problem_url)
      folderStructureObj.create()
    if args.platform == Platform.CODEFORCES.value:
      codeforcesParserObj = CodeforcesParser(args.contestID)
      all_prob_inp_out = codeforcesParserObj.get_input_and_output()
      folder_name = f"cf_{args.contestID}"
      no_of_problems = codeforcesParserObj.no_of_problems()
      problem_url = codeforcesParserObj.get_problem_url()
      folderStructureObj = FolderStructure(folder_name, no_of_problems, all_prob_inp_out, problem_url)
      folderStructureObj.create()
      
    if args.watch:
       print("Watching")
      
    log.info("Process Completed ! Happy Coding :)")

if __name__ == "__main__":
    main()
