import requests
import xml.etree.ElementTree as ET
from django.shortcuts import render
from typing import List
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Mark, Model
from .forms import MarkForm


def mark_view(request):
    """
    Если метод запроса — POST, он обрабатывает данные формы
        и возвращает ответ со связанными моделями.
    Если форма действительна, она извлекает выбранную отметку
        из данных формы, фильтрует связанные модели и отображает
        шаблон mark_form.html со связанными моделями и формой.
    Если метод запроса GET, он отображает шаблон
        mark_form.html вместе с формой.
    """
    if request.method == 'POST':
        form = MarkForm(request.POST)
        if form.is_valid():
            selected_mark = form.cleaned_data['name']
            associated_models = Model.objects.filter(mark=selected_mark)
            return render(request, 'mark_form.html',
                          {'models': associated_models,
                           'form': form})
    else:
        form = MarkForm()
    return render(request, 'mark_form.html', {'form': form})


class CarsView(APIView):
    """
    Представление для получения данных об автомобиле из XML-файла и сохранения
    их в базе данных.

    Атрибуты:
    url: str — URL-адрес XML-файла, который необходимо получить.

    Методы:
    get(self, request) -> Response — обрабатывает HTTP-запрос GET, извлекает
        файл XML из URL-адреса
        (не реализовано, смотрите в TFind проекте),
        обрабатывает данные XML и сохраняет их в базе данных.
        Возвращает ответ в формате JSON,
        содержащий количество уникальных марок и моделей автомобилей,
        сохраненных в базе данных.

    Зависимости:
    - requests: используется для выполнения HTTP-запросов.
    - xml.etree.ElementTree: используется для анализа данных XML.
    - rest_framework: используется для определения APIView и обработки ответов.
    - .models: содержит модели Mark и Model для взаимодействия с базой данных.

    Обработка ошибок:
    Если во время HTTP-запроса возникает ошибка,
    возвращается ответ 500 Internal Server Error,
    содержащий сообщение об ошибке.
    """
    def get(self, request) -> Response:
        try:
            url: str = 'https://auto-export.s3.yandex.net/auto/price-list/catalog/cars.xml'
            response = requests.get(url)
            response.raise_for_status()
            xml_doc: bytes = response.content
            root = ET.fromstring(xml_doc)
            Mark.objects.all().delete()
            Model.objects.all().delete()
            i: List[int] = [0, 0]
            for mark in root.findall('mark'):
                i[0] += 1
                mark_name: str = mark.get('name')
                mark_name_obj, created = Mark.objects.get_or_create(name=mark_name)
                model_name_old: str = ''
                for folder in mark.findall('folder'):
                    model_name: str = folder.get('name').split(',')[0]
                    if model_name_old != model_name:
                        i[1] += 1
                        model_name_old = model_name
                        Model.objects.create(name=model_name, mark=mark_name_obj)
            return Response({'mark': i[0], 'models': i[1]}, status=status.HTTP_200_OK)
        except requests.RequestException:
            return Response({'error': 'Failed to retrieve the XML file from the URL'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception:
            return Response({'error': 'Failed to write to the database'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
