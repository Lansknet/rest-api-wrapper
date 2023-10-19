import httpx
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


class LansknetAPI:
    def __init__(self, base_url, username):
        self.base_url = base_url
        self.username = username
        self.is_logged_in = False
        # 10 seconds for connecting, 30 seconds for reading
        timeout = httpx.Timeout(10.0, read=30.0)
        self.client = httpx.AsyncClient(timeout=timeout)

    async def __get_jwt_token(self):
        auth = self.username + ":sssss"
        auth = base64.b64encode(auth.encode("ascii"))
        response = await self.__post("/api/login", None, {"Authorization": "Basic " + auth.decode("ascii")})
        if response.status_code == 200:
            b64 = base64.b64encode(
                str(response.json()["token"]).encode("ascii") + b":")
            return "Basic " + b64.decode("ascii")
        return {}

    async def __post(self, path, params=None, headers=None):
        url = self.base_url + path
        if headers is None:
            headers = self.auth_header
        return await self.client.post(url, json=params, headers=headers)

    async def connect(self):
        try:
            token = await self.__get_jwt_token()
            if not token:
                raise ValueError("Failed to retrieve JWT token")

            self.auth_header = {
                "Authorization": token,
                "Content-Type": "application/json"
            }
            return True
        except Exception as e:
            print(f"Error connecting: {e}")
            return False

    # List all campaigns of specific company.
    # Required query parameter: companyId: id

    async def get_all_company_campaigns(self, company_id):
        response = await self.__post("/api/campaign/company/" + str(company_id))
        if response.status_code == 200:
            campaigns = []
            if not response.json():
                return campaigns
            for campaign in response.json()["campaigns"]:
                campaigns.append(CampaignResponse(
                    int(campaign["clicked"]),
                    datetime.strptime(
                        campaign["created_date"][:-1], "%Y-%m-%dT%H:%M:%S"),
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
    async def get_all_service_campaigns(self, company_id, service_id):
        response = await self.__post("/api/campaign/service/" + str(service_id), params={"companyId": company_id})
        if response.status_code == 200:
            campaigns = []
            for campaign in response.json()["campaigns"]:
                campaigns.append(CampaignResponse(
                    int(campaign["clicked"]),
                    datetime.strptime(
                        campaign["created_date"][:-1], "%Y-%m-%dT%H:%M:%S"),
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
    async def get_all_employees(self, company_id, service_id=None):
        data = {"companyId": company_id}
        if service_id is not None:
            data["serviceId"] = service_id
        response = await self.__post("/api/employees", data)
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
    async def get_all_services(self, company_id):
        response = await self.__post("/api/services", params={"companyId": company_id})
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
    async def create_campaign(self, campaign_name, service_id, email_template):
        response = await self.__post("/ai/launch_campaign", params={"campaignName": campaign_name, "serviceId": service_id,
                                                                    "emailTemplate": email_template})
        if response.status_code == 200:
            return "Ok"
        return HTMLError(response.reason, response.status_code)

    async def get_all_companies(self):
        try:
            path = "/api/companies"
            response = await self.__post(path)
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

    async def close(self):  # method to close the async httpx client
        await self.client.aclose()
