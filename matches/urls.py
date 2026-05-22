from django.urls import path

from . import views


urlpatterns = [

    path(

        'fixtures/',

        views.fixtures,

        name='fixtures'

    ),

    path(

        'results/',

        views.results,

        name='results'

    ),

    path(

        'generate-fixtures/',

        views.generate_fixtures,

        name='generate_fixtures'

    ),

]