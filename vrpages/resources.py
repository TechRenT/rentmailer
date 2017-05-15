import csv

from import_export import resources
from .models import PolishedUrl


class PolishedUrlResource(resources.ModelResource):
    class Meta:
        model = PolishedUrl

def handle_uploaded_file(f):
    with open('media/polished_urls.csv', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def csv_reader(filename, list):
    """Open and read a csv file"""
    with open(filename, encoding="utf-8") as csvfile:
        read_csv = csv.reader(csvfile)
        for row in read_csv:
            list.append(row)