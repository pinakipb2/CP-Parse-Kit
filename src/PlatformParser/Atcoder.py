import time
import requests
import structlog
from bs4 import BeautifulSoup
from utility import number_to_letter

log = structlog.get_logger(__name__)

class AtcoderParser:
    def __init__(self, contest_id):
        log.info(f"{self.__class__.__name__} Initiated")
        self.contest_id = contest_id
        self.contest_url = f"https://atcoder.jp/contests/abc{self.contest_id}/tasks"
        self.problem_url = f"https://atcoder.jp/contests/abc{self.contest_id}/tasks/abc{self.contest_id}_"
        self.contest_response = None
        self.__ping_contest()

    def __ping_contest(self):
        log.info(f"Pinging Contest ID : abc{self.contest_id}")
        response = requests.get(self.contest_url, verify=True)
        if response.status_code == 200:
            self.contest_response = response.content
            log.info(f"Ping Success - Contest ID : abc{self.contest_id}")
        else:
            log.error(f"Ping Failed - Contest ID : abc{self.contest_id}")
            exit(1)

    def get_problem_url(self):
        return self.problem_url

    def no_of_problems(self):
        prob_html = BeautifulSoup(self.contest_response, "html.parser")
        prob_table = prob_html.find("table")
        all_td = prob_table.find_all("td")
        total_problems = int(len(all_td) / 4)
        log.info(f"Found {total_problems} Problems in Contest ID: abc{self.contest_id}")
        return total_problems

    def __parse_input_output(self, prob_index, all_prob_inp_out):
        time.sleep(0.3)
        prob_url = self.problem_url + prob_index
        response = requests.get(prob_url, verify=True)
        if response.status_code == 200:
            prob_html = BeautifulSoup(response.content, "html.parser")
            all_div = prob_html.find_all("div", attrs={"class": "part"})
            # Somehow in Atcoder pre tags appear twice
            all_div = all_div[len(all_div) // 2 : len(all_div)]
            # Only take first pre in div as second pre
            # will be alternative solution
            pre_div = []
            for div in all_div:
                if div.find("pre"):
                    pre_div.append(div)
            # Removing the input constraint
            del pre_div[0]
            assert len(pre_div) % 2 == 0
            pre_div = BeautifulSoup(str(pre_div), "html.parser")
            prob_input = ""
            prob_output = ""
            all_pre_tag = []
            for div in pre_div.find_all("div"):
                pre_tag = div.find("pre")
                all_pre_tag.append(pre_tag.get_text())
            for i in range(0, len(all_pre_tag), 2):
                prob_input = all_pre_tag[i]
                prob_output = all_pre_tag[i + 1]
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
            prob_index = number_to_letter(i + 1)
            prob_url = self.problem_url + prob_index
            prob_input, prob_output = self.__parse_input_output(
                prob_index, all_prob_inp_out
            )
            if prob_input == None or prob_output == None:
                retry = 3
                while retry > 0:
                    log.error(f"Retry Parsing | URL: {prob_url}")
                    time.sleep(2)
                    prob_input, prob_output = self.__parse_input_output(
                        prob_index, all_prob_inp_out
                    )
                    if prob_input != None and prob_output != None:
                        retry = 0
                    else:
                        retry -= 1
        return all_prob_inp_out
