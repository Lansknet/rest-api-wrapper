import aiohttp
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
class HTMLError:
    reason: str
    status_code: int


class LansknetAPI:
    def __init__(self, base_url, username):
        self.base_url = base_url
        self.username = username
        self.is_logged_in = False
        self.auth_header = {
            "Authorization": self.__get_jwt_token(),
            "Content-Type": "application/json"
        }

    def is_logged(self):
        return self.is_logged_in

    def __get_jwt_token(self):
        auth = self.username + ":sssss"
        auth = base64.b64encode(auth.encode("ascii"))
        response = self.___post("/api/login", None, {"Authorization": "Basic " + auth.decode("ascii")})
        if response.status_code == 200:
            self.is_logged_in = True
            b64 = base64.b64encode(str(response.json()["token"]).encode("ascii") + b":")
            return "Basic " + b64.decode("ascii")
        return {}

    def ___post(self, path, params=None, headers=None):
        url = self.base_url + path
        if headers is None:
            headers = self.auth_header
        return requests.post(url, json=params, headers=headers)

    async def __post(self, path, params=None, headers=None):
        url = self.base_url + path
        if headers is None:
            headers = self.auth_header
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params, headers=headers) as response:
                return response

    async def __fetch_campaigns(self, path, params=None):
        try:
            response = await self.__post(path, params)
            if response.status == 200:
                campaigns = []
                json_data = await response.json()
                if not json_data:
                    return campaigns
                for campaign in json_data["campaigns"]:
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
            return HTMLError(response.reason, response.status)
        except Exception as e:
            return HTMLError("Error", 500)

    async def get_all_company_campaigns(self, company_id):
        assert isinstance(company_id, int)
        path = "/api/campaign/company/" + str(company_id)
        return await self.__fetch_campaigns(path)

    async def get_all_service_campaigns(self, company_id, service_id):
        assert isinstance(company_id, int)
        assert isinstance(service_id, int)
        path = "/api/campaign/service/" + str(service_id)
        params = {"companyId": company_id}
        return await self.__fetch_campaigns(path, params)

    async def get_all_employees(self, company_id, service_id=None):
        try:
            assert isinstance(company_id, int)
            path = "/api/employees"
            data = {"companyId": company_id}
            if service_id is not None:
                data["serviceId"] = service_id
            response = await self.__post(path, data)
            if response.status == 200:
                employees = []
                json_data = await response.json()
                for employee in json_data["employees"]:
                    employees.append(EmployeeResponse(
                        employee["email"],
                        employee["first_name"],
                        employee["last_name"]
                    ))
                return employees
            return HTMLError(response.reason, response.status)
        except Exception as e:
            return HTMLError("Error", 500)

    async def get_all_services(self, company_id):
        try:
            assert isinstance(company_id, int)
            path = "/api/services"
            params = {"companyId": company_id}
            response = await self.__post(path, params)
            if response.status == 200:
                services = []
                json_data = await response.json()
                for service in json_data["services"]:
                    services.append(ServiceResponse(
                        service["id"],
                        service["name"]
                    ))
                return services
            return HTMLError(response.reason, response.status)
        except Exception as e:
            return HTMLError("Error", 500)

    async def create_campaign(self, campaign_name, service_id, email_template):
        path = "/ai/launch_campaign"
        params = {
            "campaignName": campaign_name,
            "serviceId": service_id,
            "emailTemplate": email_template
        }
        response = await self.__post(path, params)
        if response.status == 200:
            return "Ok"
        return HTMLError(response.reason, response.status)
