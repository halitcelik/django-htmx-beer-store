import uuid
from django.db import models
from django.db.models.query import prefetch_related_objects
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.contrib.postgres.aggregates import StringAgg
from django.contrib.postgres.search import (
    SearchQuery,
    SearchRank,
    SearchVector,
    TrigramSimilarity,
    SearchVectorField,
)
from django.conf import settings

search_vectors_def = (
    SearchVector("name", weight="A")
    + SearchVector(StringAgg("style__name", delimiter=" "), weight="B")
    + SearchVector("category__name", weight="C")
    + SearchVector("descript", weight="D")
)


class BeerManager(models.Manager):
    def search(self, text):
        search_query = SearchQuery(text)
        search_rank = SearchRank(search_vectors_def, search_query)
        trigram_similarity = TrigramSimilarity("name", text)
        return (
            self.get_queryset()
            .filter(search_vector=text)
            .annotate(rank=search_rank + trigram_similarity)
            .prefetch_related("style", "category")
            .order_by("-rank")
            .filter(category__isnull=False, style__isnull=False, name__isnull=False)
        )


class Beer(models.Model):
    legacy_id = models.IntegerField(blank=True, null=True)
    brewery = models.ForeignKey(
        "Brewery", on_delete=models.CASCADE, blank=True, null=True
    )
    name = models.CharField(max_length=255, blank=True, null=True)
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, blank=True, null=True
    )
    style = models.ForeignKey("Style", on_delete=models.CASCADE, blank=True, null=True)
    abv = models.FloatField(blank=True, null=True)
    ibu = models.FloatField(blank=True, null=True)
    srm = models.FloatField(blank=True, null=True)
    upc = models.IntegerField(blank=True, null=True)
    filepath = models.CharField(max_length=255, blank=True, null=True)
    descript = models.TextField(blank=True, null=True)
    last_mod = models.DateTimeField(_(""), auto_now_add=True)
    published = models.BooleanField(default=False)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True
    )

    search_vector = SearchVectorField(blank=True, null=True)

    objects = BeerManager()

    class Meta:
        db_table = "beers"
        ordering = ("pk",)

    def __str__(self) -> str:
        return self.name or "n/a"

    def get_absolute_url(self):
        return reverse("beers:detail", kwargs={"pk": self.pk})


class Category(models.Model):
    legacy_id = models.IntegerField(blank=True, null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(_("Name"), max_length=255)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self) -> str:
        return self.name if self.name else "n/a"


class Style(models.Model):
    legacy_id = models.IntegerField(blank=True, null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(_("Name"), max_length=255)

    def __str__(self) -> str:
        return self.name if self.name else "n/a"


class Brewery(models.Model):
    legacy_id = models.IntegerField(blank=True, null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(_("Name"), max_length=255)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    website = models.CharField(max_length=255)
    filepath = models.CharField(max_length=255)
    descript = models.TextField()
    last_mod = models.DateTimeField(_(""), auto_now_add=True)

    class Meta:
        verbose_name = _("Brewery")
        verbose_name_plural = _("Breweries")

    def get_absolute_url(self):
        return reverse("beers:detail", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return self.name if self.name else "n/a"


class BreweryLocation(models.Model):
    legacy_id = models.IntegerField(blank=True, null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    brewery = models.ForeignKey(Brewery, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    accuracy = models.CharField(_("Accuracy"), blank=True, null=True, max_length=50)
