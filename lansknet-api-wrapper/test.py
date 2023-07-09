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

    def test_login(self):
        api = LansknetAPI("https://api-lansknet.me", "ffc0eda474e848dcbd79b195927d0719")
        self.assertEqual(api.is_logged(), True)
        api = LansknetAPI("https://api-lansknet.me", "wrongToken")
        self.assertEqual(api.is_logged(), False)

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


if __name__ == '__main__':
    unittest.main()
