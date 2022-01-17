import csv
import os
from django.core.management.base import BaseCommand
from beers.models import Beer, Category, Style, Brewery, BreweryLocation


class Command(BaseCommand):
    help = "My shiny new management command."

    def handle(self, *args, **options):
        pwd = os.getcwd()

        open_files = []
        try:
            with open(
                f"{pwd}/django_htmx_example/beers/management/commands/categories.csv"
            ) as csvDataFile:
                csvReader = csv.reader(csvDataFile)
                print("IMPORTING CATEGORIES")
                for i, row in enumerate(csvReader):
                    print(i)
                    if i > 0:
                        Category.objects.get_or_create(legacy_id=row[0], name=row[1])
            with open(
                f"{pwd}/django_htmx_example/beers/management/commands/styles.csv"
            ) as csvDataFile:
                csvReader = csv.reader(csvDataFile)
                print("IMPORTING Styles")
                for i, row in enumerate(csvReader):
                    print(i)
                    if i > 0:
                        cat = Category.objects.get(legacy_id=row[1])
                        Style.objects.get_or_create(
                            legacy_id=row[0], name=row[2], category=cat
                        )
            with open(
                f"{pwd}/django_htmx_example/beers/management/commands/breweries.csv"
            ) as csvDataFile:
                csvReader = csv.reader(csvDataFile)
                print("IMPORTING breweries")
                for i, row in enumerate(csvReader):
                    print(i, row)
                    if i > 0:
                        Brewery.objects.get_or_create(
                            legacy_id=row[0],
                            name=row[1],
                            address1=row[2],
                            address2=row[3],
                            city=row[4],
                            state=row[5],
                            code=row[6],
                            country=row[7],
                            phone=row[8],
                            website=row[9],
                            filepath=row[10],
                            descript=row[11],
                        )
            with open(
                f"{pwd}/django_htmx_example/beers/management/commands/breweries_geocode.csv"
            ) as csvDataFile:
                csvReader = csv.reader(csvDataFile)
                print("IMPORTING locations")
                for i, row in enumerate(csvReader):
                    if i > 0:
                        brewery = Brewery.objects.filter(legacy_id=row[1])
                        if brewery.exists():
                            brewery = brewery.first()
                            BreweryLocation.objects.get_or_create(
                                legacy_id=row[0],
                                brewery=brewery,
                                latitude=row[2],
                                longitude=row[3],
                                accuracy=row[4],
                            )
            with open(
                f"{pwd}/django_htmx_example/beers/management/commands/styles.csv"
            ) as csvDataFile:
                csvReader = csv.reader(csvDataFile)
                print("changing Styles")
                for i, row in enumerate(csvReader):
                    print(i)
                    if i > 0:
                        cat = Category.objects.get(legacy_id=row[1])
                        style = Style.objects.get(legacy_id=row[0])
                        style.name = row[2]
                        style.save()
            with open(
                f"{pwd}/django_htmx_example/beers/management/commands/beer.csv"
            ) as csvDataFile:
                csvReader = csv.reader(csvDataFile)
                open_files.append(csvDataFile)
                for i, row in enumerate(csvReader):
                    if i > 0:
                        print(i, row)
                        brewery = None
                        if row[1] and row[1].isdigit():
                            brewery = Brewery.objects.get(legacy_id=row[1])
                        style = None
                        cat = None
                        if row[3] and row[3] != "-1" and row[3].isdigit():
                            cat = Category.objects.get(legacy_id=row[3])
                        if row[4] and row[4] != "-1" and row[4].isdigit():
                            style = Style.objects.get(legacy_id=row[4])
                        Beer.objects.get_or_create(
                            legacy_id=row[0] if row[0] and row[0].isdigit() else None,
                            brewery=brewery,
                            name=row[2],
                            category=cat,
                            style=style,
                            abv=row[5] if row[5] else None,
                            ibu=row[6] if row[6] else None,
                            srm=row[7] if row[7] else None,
                            upc=row[8] if row[8] else None,
                            filepath=row[9] if row[9] else None,
                            descript=row[10] if row[10] else None,
                        )
        except Exception as e:
            for file in open_files:
                file.close()
            raise e
        finally:
            for file in open_files:
                file.close()
