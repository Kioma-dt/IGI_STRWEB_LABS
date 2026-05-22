from django.test import TestCase
from django.utils import timezone
from decimal import Decimal
from django.contrib.auth.models import User

from analytics.services import StatisticsService
from apps.catalog.models import Category, Product, ProductStock
from apps.orders.models import Order, OrderItem
from apps.users.models import CustomerProfile, EmployeeProfile
from apps.reviews.models import Review
from apps.suppliers.models import Supplier, ProductSupplier

