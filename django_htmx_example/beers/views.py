from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Brewery, BreweryLocation, Beer, Style, Category
from .forms import BeerForm, BeerDescriptionForm, BeerDetailsForm
from django.db.models import Count
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from django.http import HttpResponse

# Create your views here.


def index(request):
    query = request.GET.get("q")
    page = request.GET.get("page", 1)
    template = "beers/list.html"
    if request.htmx:
        template = "beers/includes/beers-table.html"
    if query:
        beers = Beer.objects.search(query)
    else:
        beers = Beer.objects.all().prefetch_related("style", "category")
    return render(
        request,
        template,
        {
            "beers": Paginator(beers, 10).get_page(page),
            "page": page,
            "total": len(beers),
            "query": query,
        },
    )


def detail(request, pk):
    beer = get_object_or_404(Beer, pk=pk)
    return render(request, "beers/detail.html", {"beer": beer})


def add(request):
    ...
    beers = Paginator(Beer.objects.all(), 30)
    return render(request, "beers/list.html", {"beers": beers})


def delete(request):
    ...
    beers = Paginator(Beer.objects.all(), 30)
    return render(request, "beers/list.html", {"beers": beers})


def edit(request, pk):
    beer = get_object_or_404(Beer, pk=pk)
    form = BeerForm(instance=beer)
    template = "beers/edit.html"
    if request.htmx:
        template = "beers/includes/form-row.html"
    if request.method == "POST":
        form = BeerForm(request.POST, instance=beer)
        if form.is_valid():
            beer = form.save()
            if request.htmx:
                message = f"{beer.name} is saved successfully."
                return render(
                    request,
                    "beers/includes/beer-row-edited.html",
                    {"beer": beer, "message": message},
                )
            else:
                return redirect(reverse("beers:click-to-edit"))
        else:
            return render(request, template, {"form": form, "beer": beer})
    else:
        return render(request, template, {"form": form, "beer": beer})


@login_required
@require_http_methods(["DELETE"])
def delete(request, pk):
    beer = get_object_or_404(Beer, pk=pk)
    beer.delete()
    message = f"{beer.name} is deleted."
    return render(request, "beers/includes/delete-success.html", {"message": message})


def active_search(request):
    query = request.GET.get("q")
    page = request.GET.get("p", 1)
    template = "beers/active-search.html"
    if request.htmx:
        template = "beers/includes/beers-table.html"
    if query:
        beers = Beer.objects.search(query)
    else:
        beers = Beer.objects.all().prefetch_related("style", "category")
    return render(
        request,
        template,
        {
            "beers": Paginator(beers, 10).get_page(page),
            "page": page,
            "query": query,
        },
    )


def click_to_edit(request):
    query = request.GET.get("q")
    page = request.GET.get("page", 1)
    template = "beers/click-to-edit.html"
    if request.htmx:
        template = "beers/includes/beers-table.html"
    if query:
        beers = Beer.objects.search(query)
    else:
        beers = Beer.objects.filter(
            category__isnull=False, style__isnull=False, name__isnull=False
        ).prefetch_related("style", "category")
    return render(
        request,
        template,
        {
            "beers": Paginator(beers, 10).get_page(page),
            "page": page,
            "total": len(beers),
            "query": query,
        },
    )


def infinite_scroll(request):
    query = request.GET.get("q")
    page = request.GET.get("page", 1)
    template = "beers/infinite-scroll.html"
    if request.htmx:
        template = "beers/includes/beer-row.html"
    if query:
        beers = Beer.objects.search(query)
    else:
        beers = Beer.objects.all().prefetch_related("style", "category")
    return render(
        request,
        template,
        {
            "beers": Paginator(beers, 50).get_page(page),
            "page": page,
            "infinite_scroll": True,
            "total": len(beers),
            "query": query,
        },
    )


def lazy_loading(request):
    query = request.GET.get("q")
    page = request.GET.get("page", 1)
    template = "beers/lazy-loading.html"
    beers = Beer.objects.none()
    if request.htmx:
        template = "beers/includes/beers-table.html"
        if query:
            beers = Beer.objects.search(query)
        else:
            beers = Beer.objects.filter(
                category__isnull=False,
                style__isnull=False,
                name__isnull=False,
                descript__isnull=False,
            ).prefetch_related("style", "category")
    return render(
        request,
        template,
        {
            "beers": Paginator(beers, 10).get_page(page),
            "page": page,
            "hide_pagination": True,
            "total": len(beers),
            "query": query,
        },
    )


def similar(request, pk):
    beer = get_object_or_404(Beer, pk=pk)
    similar_beers = Beer.objects.filter(
        category=beer.category, style=beer.style
    ).exclude(pk=beer.pk)[:3]
    return render(
        request, "beers/includes/similar.html", {"similar_beers": similar_beers}
    )


def style_select(request):
    c = request.GET.get("c")
    if c and c.strip():
        category = get_object_or_404(Category, pk=c)
        if category:
            styles = Style.objects.filter(category=category)
            return render(
                request, "beers/includes/styles-select.html", {"styles": styles}
            )


def value_select(request):
    s = request.POST.get("s")
    c = request.POST.get("c")
    style = Style.objects.none()
    beers = Beer.objects.none()
    category = Category.objects.none()
    if c and c.strip():
        category = get_object_or_404(Category, pk=c)
    if s and s.strip():
        style = get_object_or_404(Style, pk=s)

    if category and style:
        beers = Beer.objects.filter(style=style, category=category)
        return render(
            request,
            "beers/includes/beer-row.html",
            {
                "beers": Paginator(beers, 10).get_page(1),
                "hide_pagination": True,
                "value_select": True,
                "total": len(beers),
            },
        )
    else:
        return render(
            request,
            "beers/value-select.html",
            {"categories": Category.objects.all(), "value_select": True},
        )


def paginate(request):
    page = request.GET.get("page", 1)
    template = "beers/paginate.html"
    beers = Beer.objects.filter(
        category__isnull=False, style__isnull=False
    ).prefetch_related("style", "category")
    if request.htmx:
        template = "beers/includes/beers-table.html"
    return render(
        request,
        template,
        {
            "beers": Paginator(beers, 10).get_page(page),
            "page": page,
            "total": len(beers),
        },
    )


@login_required()
def create(request, step=1):
    beer, _ = Beer.objects.get_or_create(added_by=request.user, published=False)
    form = BeerForm()
    template = "beers/create.html"
    if request.htmx:
        template = "beers/includes/create-form.html"
    if request.method == "POST":

        if step == 1:
            form = BeerForm(request.POST, instance=beer)
        elif step == 2:
            form = BeerDescriptionForm(request.POST, instance=beer)
        elif step == 3:
            form = BeerDetailsForm(request.POST, instance=beer)

        if form.is_valid():
            beer = form.save(commit=False)
            beer.added_by = request.user
            if step == 3:
                beer.published = True
                beer.save()
                if request.htmx:
                    return HttpResponse(
                        "OK",
                        headers={
                            "HX-Redirect": beer.get_absolute_url(),
                        },
                    )
                return redirect(beer.get_absolute_url())
            else:
                step += 1
            beer.save()
        else:
            return render(request, template, {"form": form, "step": step})

    if step == 1:
        form = BeerForm(instance=beer)
    elif step == 2:
        form = BeerDescriptionForm(instance=beer)
    elif step == 3:
        form = BeerDetailsForm(instance=beer)

    return render(request, template, {"form": form, "step": step})


@require_http_methods(["PUT"])
def favourite(request, pk):
    if request.user.is_authenticated:
        beer = get_object_or_404(Beer, pk=pk)
        if request.user.favourites.filter(pk=beer.pk).exists():
            request.user.favourites.remove(beer)
        else:
            request.user.favourites.add(beer)
        return render(request, "beers/includes/favourite.html", {"beer": beer})


# def click_to_edit(request):
#     beers = Paginator(Beer.objects.all(), 30)
#     return render(request, "beers/list.html", {"beers": beers})


# def click_to_edit(request):
#     beers = Paginator(Beer.objects.all(), 30)
#     return render(request, "beers/list.html", {"beers": beers})
