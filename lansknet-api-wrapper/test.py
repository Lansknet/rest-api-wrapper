import unittest
from LansknetAPI import LansknetAPI
from LansknetAPI import CampaignResponse
from LansknetAPI import ServiceResponse
from LansknetAPI import EmployeeResponse
from LansknetAPI import HTMLError


class LansknetApiWrapperTest(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        cls.api = LansknetAPI("https://api-lansknet.me", "ffc0eda474e848dcbd79b195927d0719")

    def test_invalid_base_url(self):
        with self.assertRaises(Exception):
            invalid_api = LansknetAPI("https://invalid-api.com", "ffc0eda474e848dcbd79b195927d0719")
            invalid_api.get_all_companies()

    def test_login(self):
        api = LansknetAPI("https://api-lansknet.me", "ffc0eda474e848dcbd79b195927d0719")
        self.assertEqual(api.is_logged(), True)
        api = LansknetAPI("https://api-lansknet.me", "wrongToken")
        self.assertEqual(api.is_logged(), False)

    async def test_get_campaign_info(self):
        campaign_info = await self.api.get_campaign_info("invalid_campaign_name")
        self.assertEqual(self.api.is_logged(), True)
        self.assertEqual(list[EmailStatus], type(campaign_info))
        self.assertEqual(len(campaign_info), 0)  # With an invalid campaign name returning an empty list

    async def test_get_all_company_campaigns(self):
        campaigns = await self.api.get_all_company_campaigns(1)
        self.assertEqual(self.api.is_logged(), True)
        self.assertEqual(list[CampaignResponse], type(campaigns))
        self.assertRaises(Exception, self.api.get_all_company_campaigns, "0")

    async def test_get_all_service_campaigns(self):
        campaigns = await self.api.get_all_service_campaigns(1, 1)
        self.assertEqual(self.api.is_logged(), True)
        self.assertEqual(list[CampaignResponse], type(campaigns))
        self.assertRaises(Exception, self.api.get_all_service_campaigns, "1", "1")
        self.assertEqual(HTMLError, self.api.get_all_service_campaigns("0", "0"))

    async def test_get_all_employees(self):
        employees = await self.api.get_all_employees(1)
        self.assertEqual(self.api.is_logged(), True)
        self.assertEqual(list[EmployeeResponse], type(employees))
        employees = await self.api.get_all_employees(1, 1)
        self.assertEqual(list[EmployeeResponse], type(employees))
        self.assertRaises(Exception, self.api.get_all_employees, "1")
        self.assertEqual(HTMLError, self.api.get_all_employees("0"))

    async def test_get_all_services(self):
        services = await self.api.get_all_services(1)
        self.assertEqual(self.api.is_logged(), True)
        self.assertEqual(list[ServiceResponse], type(services))
        self.assertRaises(Exception, self.api.get_all_services, "1")
        self.assertEqual(HTMLError, self.api.get_all_services("0"))

    async def test_create_campaign(self):
        response = await self.api.create_campaign("test", 1, "str")
        self.assertEqual(self.api.is_logged(), True)
        self .assertEqual(response, "Ok")

    async def test_get_all_company_campaigns_no_campaigns(self):
        campaigns = await self.api.get_all_company_campaigns(2)  # With company with ID 2 have no campaigns
        self.assertEqual(self.api.is_logged(), True)
        self.assertEqual(list[CampaignResponse], type(campaigns))
        self.assertEqual(len(campaigns), 0)

    async def test_get_all_service_campaigns_invalid_service(self):
        with self.assertRaises(HTMLError):
            await self.api.get_all_service_campaigns(1, -1)  # With -1 as an invalid service ID

    async def test_get_all_employees_no_employees(self):
        employees = await self.api.get_all_employees(3)  # With company with ID 3 have no employees
        self.assertEqual(self.api.is_logged(), True)
        self.assertEqual(list[EmployeeResponse], type(employees))
        self.assertEqual(len(employees), 0)

    async def test_create_campaign_invalid_service(self):
        with self.assertRaises(HTMLError):
            await self.api.create_campaign("test", -1, "str")  # With -1 as an invalid service ID

    async def test_get_all_services_no_services(self):
        services = await self.api.get_all_services(4)  # With company with ID 4 have no services
        self.assertEqual(self.api.is_logged(), True)
        self.assertEqual(list[ServiceResponse], type(services))
        self.assertEqual(len(services), 0)

    async def test_create_campaign_invalid_template(self):
        with self.assertRaises(HTMLError):
            await self.api.create_campaign("test", 1, None)  # With None as an invalid email template

    async def test_create_campaign_missing_parameters(self):
        with self.assertRaises(HTMLError):
            await self.api.create_campaign(None, None, None)  # With missing parameters result in an error

    async def test_get_all_companies_unauthorized(self):
        unauthorized_api = LansknetAPI("https://api-lansknet.me", "invalid_token")
        with self.assertRaises(HTMLError):
            unauthorized_api.get_all_companies()

    async def test_get_campaign_info_invalid_campaign_name(self):
        campaign_info = await self.api.get_campaign_info("nonexistent_campaign")
        self.assertEqual(self.api.is_logged(), True)
        self.assertEqual(list[EmailStatus], type(campaign_info))
        self.assertEqual(len(campaign_info), 0)

    async def test_get_all_company_campaigns_no_campaigns(self):
        campaigns = await self.api.get_all_company_campaigns(2)  # With company with ID 2 have no campaigns
        self.assertEqual(self.api.is_logged(), True)
        self.assertEqual(list[CampaignResponse], type(campaigns))
        self.assertEqual(len(campaigns), 0)

    async def test_get_all_service_campaigns_invalid_service(self):
        with self.assertRaises(HTMLError):
            await self.api.get_all_service_campaigns(1, -1)  # With -1 as an invalid service ID

    async def test_get_all_employees_no_employees(self):
        employees = await self.api.get_all_employees(3)  # With company with ID 3 have no employees
        self.assertEqual(self.api.is_logged(), True)
        self.assertEqual(list[EmployeeResponse], type(employees))
        self.assertEqual(len(employees), 0)

    async def test_create_campaign_invalid_service(self):
        with self.assertRaises(HTMLError):
            await self.api.create_campaign("test", -1, "str")  # With -1 as an invalid service ID

    async def test_get_all_services_no_services(self):
        services = await self.api.get_all_services(4)  # With company with ID 4 have no services
        self.assertEqual(self.api.is_logged(), True)
        self.assertEqual(list[ServiceResponse], type(services))
        self.assertEqual(len(services), 0)

    async def test_create_campaign_invalid_template(self):
        with self.assertRaises(HTMLError):
            await self.api.create_campaign("test", 1, None)  # With None as an invalid email template

    async def test_create_campaign_missing_parameters(self):
        with self.assertRaises(HTMLError):
            await self.api.create_campaign(None, None, None)  # With missing parameters result in an error

    async def test_get_all_companies_unauthorized(self):
        unauthorized_api = LansknetAPI("https://api-lansknet.me", "invalid_token")
        with self.assertRaises(HTMLError):
            unauthorized_api.get_all_companies()

    async def test_get_all_companies_valid_response(self):
        companies = await self.api.get_all_companies()
        self.assertEqual(self.api.is_logged(), True)
        self.assertTrue(isinstance(companies, list))
        self.assertTrue(all(isinstance(company, Company) for company in companies))

    async def test_get_all_campaigns_invalid_company_id(self):
        with self.assertRaises(HTMLError):
            await self.api.get_all_company_campaigns("invalid_id")

if __name__ == '__main__':
    unittest.main()
