from django.core.management.base import BaseCommand


from dpwagtail.models import InstanceBuilder
from dpwagtail.utils import form_instance_builders


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        form_instance_builders(InstanceBuilder)
