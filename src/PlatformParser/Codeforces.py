import time
import requests
import structlog
from bs4 import BeautifulSoup
from utility import number_to_letter

log = structlog.get_logger(__name__)


class CodeforcesParser:
    def __init__(self, contest_id):
        log.info(f"{self.__class__.__name__} Initiated")
        self.contest_id = contest_id
        self.contest_url = f"https://codeforces.com/api/contest.standings?contestId={self.contest_id}&from=1&count=1&showUnofficial=false"
        self.problem_url = f"https://codeforces.com/contest/{self.contest_id}/problem/"
        self.contest_response = None
        self.__ping_contest()

    def __ping_contest(self):
        log.info(f"Pinging Contest ID : {self.contest_id}")
        response = requests.get(self.contest_url, verify=True)
        data = response.json()
        if response.status_code == 200 and data["status"] == "OK":
            self.contest_response = data
            log.info(f"Ping Success - Contest ID : {self.contest_id}")
        else:
            log.error(f"Ping Failed - Contest ID : {self.contest_id}")
            exit(1)

    def get_problem_url(self):
        return self.problem_url

    def no_of_problems(self):
        total_problems = len(self.contest_response["result"]["problems"])
        log.info(f"Found {total_problems} Problems in Contest ID: {self.contest_id}")
        return total_problems

    def __parse_input_output(self, prob_index, all_prob_inp_out):
        time.sleep(0.3)
        prob_url = self.problem_url + prob_index
        response = requests.get(prob_url, verify=True)
        if response.status_code == 200:
            prob_html = BeautifulSoup(response.text, "html.parser")
            inp = prob_html.findAll("div", attrs={"class": "input"})
            out = prob_html.findAll("div", attrs={"class": "output"})
            prob_input = ""
            prob_output = ""
            for i in range(len(inp)):
                prob_input = ""
                prob_output = ""
                i_html = BeautifulSoup(str(inp[i]), "html.parser")
                o_html = BeautifulSoup(str(out[i]), "html.parser")
                i_pre = i_html.find("pre")
                o_pre = o_html.find("pre")
                i_pre_html = BeautifulSoup(str(i_pre), "html.parser")
                o_pre_html = BeautifulSoup(str(o_pre), "html.parser")
                i_div = i_pre_html.find_all("div")
                for div in i_div:
                    prob_input = prob_input + str(div.get_text().strip()) + "\n"
                if prob_input == "":
                    prob_input = i_pre_html.get_text().strip()
                prob_output = o_pre_html.get_text().strip()
                inp_out_map = {
                    "problem_index": prob_index.lower(),
                    "input_output": [prob_input, prob_output],
                }
                all_prob_inp_out.append(inp_out_map)
            if prob_input == "" or prob_output == "":
                log.error(f"Parsing Failed | URL: {prob_url}")
                return None, None
            log.info(f"Parsing Done | URL: {prob_url}")
            return prob_input, prob_output
        else:
            log.error(f"Parsing Failed | URL: {prob_url}")
            return None, None

    def get_input_and_output(self):
        problem_len = self.no_of_problems()
        all_prob_inp_out = []
        for i in range(problem_len):
            prob_index = number_to_letter(i + 1, "capital")
            prob_url = self.problem_url + prob_index
            prob_input, prob_output = self.__parse_input_output(
                prob_index, all_prob_inp_out
            )
            if prob_input == None or prob_output == None:
                retry = 3
                while retry > 0:
                    log.error(f"Retry Parsing ({3-retry+1} of 3) | URL: {prob_url}")
                    time.sleep(2)
                    prob_input, prob_output = self.__parse_input_output(
                        prob_index, all_prob_inp_out
                    )
                    if prob_input != None and prob_output != None:
                        retry = 0
                    else:
                        retry -= 1
        return all_prob_inp_out
