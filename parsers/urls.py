from django.urls import path

from parsers.views import ScrapeSiteView

app_name = "parsers"

urlpatterns = [
    path("scrape-site/", ScrapeSiteView.as_view(), name="parsers_scrape_site")
]
