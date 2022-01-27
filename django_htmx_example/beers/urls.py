from django.urls import path
from .views import (
    click_to_edit,
    index,
    mini_detail,
    similar,
    detail,
    delete,
    create,
    edit,
    active_search,
    infinite_scroll,
    lazy_loading,
    favourite,
    style_select,
    value_select,
    paginate,
)


app_name = "beers"

urlpatterns = [
    path("list", index, name="all"),
    path("<int:pk>", detail, name="detail"),
    path("mini/<int:pk>", mini_detail, name="mini-detail"),
    path("edit/<int:pk>", edit, name="edit"),
    path("delete/<int:pk>", delete, name="delete"),
    path("favourite/<int:pk>", favourite, name="favourite"),
    path("similar/<int:pk>", similar, name="similar"),
    path("click-to-edit", click_to_edit, name="click-to-edit"),
    path("active-search", active_search, name="active-search"),
    path("infinite-scroll", infinite_scroll, name="infinite-scroll"),
    path("lazy-loading", lazy_loading, name="lazy-loading"),
    path("value-select", value_select, name="value-select"),
    path("style-select", style_select, name="style-select"),
    path("paginate", paginate, name="paginate"),
    path("tabs-and-forms", create, name="create"),
    path("tabs-and-forms/<int:step>", create, name="create"),
]
