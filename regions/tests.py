from django.test import TestCase
from .models import *

class RegionTest(TestCase):
    def test_sync(self):
        Region.objects.sync()
