from django.urls import path

from parsers.views import GetAveragePricePerUnitView

app_name = "parsers"

urlpatterns = [
    path(
        "get-average-price-per-unit/",
        GetAveragePricePerUnitView.as_view(),
        name="parsers_get_average_price_per_unit",
    )
]
