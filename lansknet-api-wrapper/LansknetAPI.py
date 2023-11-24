import requests
import base64
from dataclasses import dataclass
from datetime import datetime


@dataclass
class CampaignResponse:
    clicked: int = 0
    created_date: datetime = None
    name: str = ""
    opened: int = 0
    sent: int = 0
    service_id: int = 0
    submitted_data: int = 0


@dataclass
class EmployeeResponse:
    email: str = ""
    first_name: str = ""
    last_name: str = ""


@dataclass
class ServiceResponse:
    id: int = -1
    name: str = ""


@dataclass
class Company:
    id: int = -1
    name: str = ""


@dataclass
class HTMLError:
    reason: str
    status_code: int


@dataclass
class EmailStatus:
    id: str
    first_name: str
    last_name: str
    email: str
    position: str
    ip: str
    latitude: int
    longitude: int
    status: str


@dataclass
class CampaignTimeline:
    email: str = ""
    time: datetime = None
    message: str = ""
    details: str = ""


class LansknetAPI:
    def __init__(self, base_url, username):
        self.base_url = base_url
        self.username = username
        self.is_logged_in = False
        self.auth_header = \
            {
                "Authorization": self.__get_jwt_token(),
                "Content-Type": "application/json"
            }

    def __get_jwt_token(self):
        auth = self.username + ":sssss"
        auth = base64.b64encode(auth.encode("ascii"))
        response = self.__post("/api/login", None, {"Authorization": "Basic " + auth.decode("ascii")})
        if response.status_code == 200:
            b64 = base64.b64encode(str(response.json()["token"]).encode("ascii") + b":")
            self.is_logged_in = True
            return "Basic " + b64.decode("ascii")
        return {}

    def __post(self, path, params=None, headers=None):
        url = self.base_url + path
        if headers is None:
            headers = self.auth_header
        return requests.post(url, json=params, headers=headers)

    # List all campaigns of specific company.
    # Required query parameter: companyId: id
    def get_all_company_campaigns(self, company_id):
        response = self.__post("/api/campaign/company/" + str(company_id))
        if response.status_code == 200:
            campaigns = []
            if not response.json():
                return campaigns
            for campaign in response.json()["campaigns"]:
                campaigns.append(CampaignResponse(
                    int(campaign["clicked"]),
                    datetime.strptime(campaign["created_date"][:-1], "%Y-%m-%dT%H:%M:%S"),
                    campaign["name"],
                    int(campaign["opened"]),
                    int(campaign["sent"]),
                    int(campaign["service_id"]),
                    int(campaign["submitted_data"])
                ))
            return campaigns
        return HTMLError(response.reason, response.status_code)

    # List all campaigns of specific company and service within.
    # Required query parameter: companyId: id, serviceId: int
    def get_all_service_campaigns(self, company_id, service_id):
        response = self.__post("/api/campaign/service/" + str(service_id), params={"companyId": company_id})
        if response.status_code == 200:
            campaigns = []
            for campaign in response.json()["campaigns"]:
                campaigns.append(CampaignResponse(
                    int(campaign["clicked"]),
                    datetime.strptime(campaign["created_date"][:-1], "%Y-%m-%dT%H:%M:%S"),
                    campaign["name"],
                    int(campaign["opened"]),
                    int(campaign["sent"]),
                    service_id,
                    int(campaign["submitted_data"])
                ))
            return campaigns
        return HTMLError(response.reason, response.status_code)

    # List all employees of specific company, and if asked, of specific service within.
    # Required query parameter: companyId: id. Optional: serviceId: int
    def get_all_employees(self, company_id, service_id=None):
        data = {"companyId": company_id}
        if service_id is not None:
            data["serviceId"] = service_id
        response = self.__post("/api/employees", data)
        if response.status_code == 200:
            employees = []
            for employee in response.json()["employees"]:
                employees.append(EmployeeResponse(
                    employee["email"],
                    employee["first_name"],
                    employee["last_name"]
                ))
            return employees
        return HTMLError(response.reason, response.status_code)

        # List all services of specific company.

    # Required query parameter: companyId: int
    def get_all_services(self, company_id):
        response = self.__post("/api/services", params={"companyId": company_id})
        if response.status_code == 200:
            services = []
            for service in response.json()["services"]:
                services.append(ServiceResponse(
                    service["id"],
                    service["name"]
                ))
            return services
        return HTMLError(response.reason, response.status_code)

    # Create a new campaign.
    def create_campaign(self, campaign_name, service_id, email_template):
        response = self.__post("/ai/launch_campaign", params={"campaignName": campaign_name, "serviceId": service_id,
                                                              "emailTemplate": email_template})
        if response.status_code == 200:
            return "Ok"
        return HTMLError(response.reason, response.status_code)

    def get_all_companies(self):
        try:
            path = "/api/companies"
            response = self.__post(path)
            if response.status_code == 200:
                companies = []
                json_data = response.json()
                for service in json_data:
                    companies.append(Company(
                        int(service["companyId"]),
                        service["companyName"]
                    ))
                return companies
            return HTMLError(response.reason, response.status_code)
        except Exception as e:
            return HTMLError("Error", 500)

    def get_campaign_info(self, campaign_name):
        try:
            path = "/ai/get_campaign_info"
            response = self.__post(path, params={"campaignName": campaign_name})
            if response.status_code == 200:
                json_data = response.json()
                res = []
                for campaign_status in json_data:
                    res.append(EmailStatus(
                        campaign_status["id"],
                        campaign_status["first_name"],
                        campaign_status["last_name"],
                        campaign_status["email"],
                        campaign_status["position"],
                        campaign_status["ip"],
                        campaign_status["latitude"],
                        campaign_status["longitude"],
                        campaign_status["status"],
                    ))
                return res
            return HTMLError(response.reason, response.status_code)
        except Exception as e:
            return HTMLError("Error", 500)
