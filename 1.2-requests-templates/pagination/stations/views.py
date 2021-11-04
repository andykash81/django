from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
import csv


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):

    with open('data-398-2018-08-30.csv', 'r', encoding='utf-8') as file_csv:
        read_csv = csv.DictReader(file_csv)
        list_stations = list()
        for row in read_csv:
            row_dict = dict()
            row_dict['Name'] = row['Name']
            row_dict['Street'] = row['Street']
            row_dict['District'] = row['District']
            list_stations.append(row_dict)

    paginator = Paginator(list_stations, 10)
    current_page = request.GET.get('page')
    page = paginator.get_page(current_page)

    context = {
        'bus_stations': page.object_list,
        'page': page,
    }

    return render(request, 'stations/index.html', context)
