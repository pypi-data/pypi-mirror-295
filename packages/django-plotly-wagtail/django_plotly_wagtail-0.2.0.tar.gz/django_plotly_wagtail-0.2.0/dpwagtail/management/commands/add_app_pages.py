from django.core.management.base import BaseCommand

from dpwagtail.models import DjangoPlotlyDashPage, DjangoPlotlyDashIndexPage
from dpwagtail.utils import form_app_pages

from wagtail.models.sites import Site

from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        form_app_pages(ContentType, DjangoPlotlyDashIndexPage, DjangoPlotlyDashPage, Site)
