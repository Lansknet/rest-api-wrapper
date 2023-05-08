# Lansknet API Wrapper

This is a wrapper for the Lansknet API. It is written in Python and is designed to be used with the [Lansknet API](https://api-lansknet.me).

## Installation

To install the wrapper, run the following command:

```bash
pip install lansknet
```

## Usage

To use the wrapper, you must first import it:

```python
from LansknetAPI import LansknetAPI

api = LansknetAPI("https://api-lansknet.me", "api-key")

print(api.get_all_company_campaigns(1))
print(api.get_all_service_campaigns(1, 1))
print(api.get_all_employees(1))
print(api.get_all_services(1))
print(api.create_campaign("TestCampaignAI", 1,
                          "<html><head><title></title></head><body><p>Bonjour {{.FirstName}} {{.LastName}},"
                          "</p><p>&nbsp;</p><p>Une note a &eacute;t&eacute; ajout&eacute;e &agrave; "
                          "l&#39;activit&eacute; <a href=\"{{.URL}}\">Quiz</a> de type CUS -Network</p><p>Pensez "
                          "&agrave; la v&eacute;rifier et &agrave; contacter la personne vous ayant corrig&eacute;e "
                          "en cas d&#39;erreur.</p><p>&nbsp;</p><p>L&#39;intranet</p></body></html>"))


```
