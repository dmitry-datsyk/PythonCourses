from django.core.management.base import BaseCommand
from ProjectMy.models import Shop, Department, Item
import sqlite3


class Command(BaseCommand):
    def handle(self, *args, **options):
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        Item.objects.all().delete()
        Department.objects.all().delete()
        Shop.objects.all().delete()
        cursor.execute(
            """UPDATE sqlite_sequence SET seq=0 WHERE name in (
        'ProjectMy_department', 'ProjectMy_shop', 'ProjectMy_item')""")
        conn.commit()
        shop_1 = Shop.objects.create(
            name='Auchan',
            staff_amount=250)
        shop_2 = Shop.objects.create(
            name='IKEA',
            address='Street Žirnių g. 56, Vilnius, Lithuania',
            staff_amount=500
        )
        departament_1 = Department.objects.create(
            sphere='Furniture',
            staff_amount=250,
            description='Good furniture',
            shop=shop_1
        )
        departament_2 = Department.objects.create(
            sphere='Furniture',
            staff_amount=300,
            description='So-so furniture',
            shop=shop_2
        )
        departament_3 = Department.objects.create(
            sphere='Dishes',
            staff_amount=200,
            description='Best dishes',
            shop=shop_2
        )
        Item.objects.create(
            name='Table',
            description='Cheap wooden table',
            price=300,
            department=departament_1
        )
        Item.objects.create(
            name='Table',
            price=750,
            department=departament_2
        )
        Item.objects.create(
            name='Bed',
            description='Amazing wooden bed',
            price=1200,
            department=departament_2
        )
        Item.objects.create(
            name='Cup',
            price=10,
            department=departament_3
        )
        Item.objects.create(
            name='Plate',
            description='Glass plate',
            price=20,
            department=departament_3)
        self.stdout.write(
            self.style.SUCCESS('Successfully delete and insert data'))
