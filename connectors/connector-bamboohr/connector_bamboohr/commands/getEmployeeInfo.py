"""GetEmplyoeeInfo."""
import json

import requests


class GetEmployeeInfo:
    """GetPayRate."""

    def __init__(self, employee_id: str, fields: str):
        """__init__."""
        self.employee_id = employee_id
        self.fields = fields

    def execute(self, config, task_data):
        """Execute."""
        api_key = config["BAMBOOHR_API_KEY"]
        subdomain = config["BAMBOOHR_SUBDOMAIN"]

        url = f"https://api.bamboohr.com/api/gateway.php/{subdomain}/v1/employees/{self.employee_id}"
        headers = {"Accept": "application/json"}
        params = {"fields": self.fields, "onlyCurrent": "true"}
        auth = (api_key, "x")

        try:
            raw_response = requests.get(url, params, headers=headers, auth=auth)
            status_code = raw_response.status_code
            parsed_response = json.loads(raw_response.text)
            response = json.dumps(parsed_response)
        except Exception as ex:
            response = json.dumps({"error": str(ex)})
            status_code = 500

        return {
            "response": response,
            "status": status_code,
            "mimetype": "application/json",
        }


#
# Sample response
#

# {
#    "amount": "65000.00",
#    "currency": "USD",
#    "id": "4",
#    "payRate": "65000.00 USD"
# }


class GetPayRate:
    """GetPayRate."""

    def __init__(self, employee_id: str):
        """__init__."""
        self.employee_id = employee_id

    def execute(self, config, task_data):
        """Execute."""
        status_code = 0
        try:
            response = GetEmployeeInfo(self.employee_id, "payRate").execute(
                config, task_data
            )
            parsed_response = json.loads(response["response"])
            pay_rate = parsed_response["payRate"]
            pay_rate_parts = pay_rate.split(" ")
            parsed_response["amount"] = pay_rate_parts[0]
            parsed_response["currency"] = pay_rate_parts[1]
            response = json.dumps(parsed_response)
        except Exception as ex:
            response = json.dumps({"error": str(ex)})
            status_code = 500

        return {
            "response": response,
            "status": status_code,
            "mimetype": "application/json",
        }
