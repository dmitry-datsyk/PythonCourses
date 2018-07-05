from datetime import datetime

from django.db.models import Q, F
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, CreateView, UpdateView, FormView, \
    DeleteView

from ProjectMy.forms import SimpleForm, ItemCreateForm, SearchForm
from ProjectMy.models import Shop, Department, Item
import json
from django.db.models import Min, Max, Avg, Count
import re
import os

from ProjectMy.utils import upload_file


def factor(request):
    result = 1
    number = 1
    lst = []
    while number < 21:
        for i in range(1, number + 1):
            result *= i
            i += 1
        lst.append(result)
        number += 1
        result = 1
    return render(request, 'index.html', {'lst': lst})


def index_string(request, string, index):
    index = int(index)
    if index > len(string) - 1 or index < 0:
        symbol = None
    else:
        symbol = string[index]
    return render(request, 'string.html', {'symbol': symbol})


def params(request):
    k = request.GET
    dict1 = dict(k)
    dict12 = {i: int(t) for i, j in dict1.items() for t in j}
    dict2 = json.dumps(dict12, indent=4)
    return render(request, 'params.html', {'result': dict2})


def insert_data(request):
    Shop.objects.create(name='Auchan', staff_amount=250)
    Shop.objects.create(
        name='IKEA', address='Street Žirnių g. 56, Vilnius, Lithuania.',
        staff_amount=500
    )
    Department.objects.create(sphere='Furniture', staff_amount=250,
                              shop=Shop.objects.get(id=1))
    Department.objects.create(sphere='Furniture', staff_amount=300,
                              shop=Shop.objects.get(id=2))
    Department.objects.create(sphere='Dishes', staff_amount=200,
                              shop=Shop.objects.get(id=2))
    Item.objects.create(name='Table', description='Cheap wooden table',
                        price=300, department=Department.objects.get(id=1))
    Item.objects.create(name='Table', price=750,
                        department=Department.objects.get(id=2))
    Item.objects.create(name='Bed', description='Amazing wooden bed',
                        price=1200,
                        department=Department.objects.get(id=2))
    Item.objects.create(name='Cup', price=10,
                        department=Department.objects.get(id=3))
    Item.objects.create(name='Plate', description='Glass plate',
                        price=20, department=Department.objects.get(id=3))
    return factor(request)


def index(request):
    all_items = Item.objects.all()
    all_items_query = Item.objects.filter()
    expensive_items = Item.objects.filter(
        price__gte=300, price__lt=1000
    ).all()
    normal_shops = Shop.objects.exclude(address__isnull=True).all()
    sorted_items = Item.objects.order_by('-price')
    ishop_items = Item.objects.filter(department__shop__name__istartswith='i')
    itmes_300_1200 = Item.objects.filter(Q(price=300) | Q(price=1200))
    return render(request, 'res.html', context=locals())


def shops_all(request):
    shops = Shop.objects.all()
    return render(request, 'shops_all.html', {'shops': shops})


def select_data(request):
    items_d = Item.objects.exclude(description__isnull=True).all()
    sphere_200 = Department.objects.filter(staff_amount__gt=200).values(
        'sphere').distinct()
    name_i = Shop.objects.filter(name__istartswith='i').all().values('address')
    items_furniture = Item.objects.filter(department__sphere='Furniture').all()
    shops_desc = Shop.objects.filter(
        departments__items__description__isnull=False).all().distinct()
    tuples = Item.objects.all()
    lst_items = [(i.name, i.department.sphere, i.department.shop.name) for i in
                 tuples]
    ordered_items = Item.objects.order_by('name').all()[1:4]
    ordered_items = [i.id for i in ordered_items]
    aggregated = Item.objects.values('department__shop').annotate(
        amount=Count('id'), max=Max('price'), min=Min('price'), avg=Avg(
            'price')).filter(amount__gt=1).all()
    dict1 = {1: items_d, 2: sphere_200, 3: name_i, 4: items_furniture,
             5: shops_desc, 6: lst_items, 7: ordered_items, 8: aggregated}
    return render(request, 'select_data.html', {'dict1': dict1})


def update_data(request):
    Item.objects.filter(Q(name__startswith='B') | Q(
        name__endswith='e')).update(price=F('price') + 100)
    return shops_all(request)


def delete_data(request):
    Item.objects.filter((Q(price__gt=500) & Q(description__isnull=True)) | Q(
        department__shop__address__isnull=True)).delete()
    return shops_all(request)


# def my_view(request, *args):
# #     if request.method == 'GET':
# #         context = {
# #             'departments': Department.objects.select_related('shop')
# #         }
# #         return render(request,'my_view.html', context)
# #     elif request.method == 'POST':
# #         Item.objects.create(
# #             name=request.POST.get('name'),
# #             description=request.POST.get('description'),
# #             price=int(request.POST.get('price')),
# #             department_id=request.POST.get('department')
# #         )
# #         return redirect('index')

class MyView(View):
    def get(self, request):
        context = {
            'departments': Department.objects.select_related('shop')
        }
        return render(request, 'my_view.html', context)

    def post(self, request):
        item = Item.objects.create(
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            price=int(request.POST.get('price')),
            department_id=request.POST.get('department')
        )
        image = upload_file(request.FILES['image'])
        item.image.save('{}.png'.format(item.id), image)
 #       item.save()
        return redirect('index')


def shops(request):
    return shops_all(request)


class AddShop(TemplateView):
    template_name = "add_shop.html"

    def post(self, request):
        Shop.objects.create(name=request.POST.get("name"),
                            address=request.POST.get("address"),
                            staff_amount=int(request.POST.get("staff_amount")))
        return redirect('index')


def shop_id(request, shop_id):
    try:
        context = {'shops': Shop.objects.get(id=shop_id)}
    except Shop.DoesNotExist:
        return redirect('index')
    return render(request, 'shop_id.html', context)


def dep_add(request, shop_id):
    return render(request, 'new_dep.html', shop_id)


class DepAdd(View):
    def get(self, request, shop_id):
        context = {
            'departments': Department.objects.select_related('shop').filter(
                shop_id=int(shop_id))
        }
        return render(request, 'dep_add.html', context)

    def post(self, request, shop_id):
        sphere = request.POST.get('sphere')
        if re.match(r'^[a-zA-Z-\s]+$', sphere) is None:
            staff_amount = request.POST.get('staff_amount')
            description = request.POST.get('description')
            is_name_valid = True
            return render(request, 'dep_add.html',
                          {'is_name_valid': is_name_valid,
                           'sphere': sphere,
                           'staff_amount': staff_amount,
                           'description': description})
        else:
            Department.objects.create(
                sphere=request.POST.get('sphere'),
                staff_amount=int(request.POST.get('staff_amount')),
                description=request.POST.get('description'),
                shop_id=shop_id
            )
        return redirect('index')

class EditItem(TemplateView):
    template_name = "item_update.html"

    def get_context_data(self, item_id, **kwargs):
        context = super(EditItem, self).get_context_data(**kwargs)
        context['items'] = Item.objects.get(id=item_id)
        return context

    def post(self, request, item_id):
        if request.POST.get("delete_image") == "on":
            Item.objects.filter(id=item_id).update(
                name=request.POST.get("name"),
                description=request.POST.get("description"),
                price=int(request.POST.get("price")),
                department_id=int(request.POST.get("department")))
            Item.objects.get(id=item_id).image.delete()
            return redirect('index')
        else:

            if 'image' in request.FILES:
                image = upload_file(request.FILES['image'])
                Item.objects.get(id=item_id).image.save(
                    '{}.png'.format(item_id), image)
            Item.objects.filter(id=item_id).update(name=request.POST.get("name"),
                description=request.POST.get("description"),
                price=int(request.POST.get("price")),
                department_id=int(request.POST.get("department")))
            return redirect('index')


def delete_object(request,item_id):
    Item.objects.get(id=item_id).delete()
    return redirect('index')


def template(request):
    current_date = datetime.now()
    number_1 = 9
    number_2 = 1.23456
    number_3 = 21
    array = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    dict =  {'a': 1, 'b': 2, 'c': 3}
    return render(request, 'template.html', {
        'current_date': current_date,
        'number_1': number_1,
        'number_2': number_2,
        'number_3': number_3,
        'array': array,
        'dict': dict
    })


class SimpleFormView(View):
    def get(self, request):
        my_form = SimpleForm()
        return render(self.request, 'simple_form.html', {'form': my_form})

    def post(self, request):
        form_obj = SimpleForm(request.POST)
        if not form_obj.is_valid():
            return render(request,'simple_form.html', {'form': form_obj})
        return render(request, 'simle_form_result.html', {
            'data': form_obj.cleaned_data})

class ItemCreateView(CreateView):
    template_name = 'item_create.html'
    success_url = '/'
    model = Item
    form_class = ItemCreateForm

    def get_context_data(self, **kwargs):
        context = super(ItemCreateView, self).get_context_data(**kwargs)
        context['departments'] = Department.objects.all()
        return context
  #  fields = ['name', 'description', 'price', 'image', 'is_sold', 'creation_date']
# #если пеишем field то не пишем form_class
#



class UpdateItemView(UpdateView):
    model = Item
    template_name = 'update_item.html'
    form_class = ItemCreateForm
    success_url = '/'

    def form_valid(self, form):
#        pk = self.request.POST.get('pk')
        image_delete = self.request.POST.get('delete_image')
        if image_delete == 'on':
            if self.object.image:
                os.remove(self.object.image.path)
                self.object.image = None
        return super(UpdateItemView, self).form_valid(form)

class ItemDeleteView(DeleteView):
    model = Item
    success_url = '/'
    template_name = 'delete_item.html'



class Search(FormView):
    template_name = 'search.html'
    form_class = SearchForm

    def form_valid(self, form):
        data = form.cleaned_data
        result = Item.objects.filter(is_sold=data['is_sold'])
        if data['min_price']:
            result = result.filter(price__gte=data['min_price'])
        if data['max_price']:
            result = result.filter(price__lte=data['max_price'])
        if data['part_name']:
            result = result.filter(name__contains=data['part_name'])
        if data['shop']:
            result = result.filter(department__shop=data['shop'])

        return render(self.request, 'search_result.html', {'items':result})

# class Search(FormView):
#     template_name = 'search.html'
#     form_class = SearchForm
#
#
#     def form_valid(self, form):
#         data = form.cleaned_data
#   #      print(data)
#         if data['min_price'] is not None and data['max_price'] is not None and\
#             data['part_name'] is not None and data['shop'] is not None:
#             items = Item.objects.filter(
#              price__gte=form.data['min_price'], price__lte=data['max_price'] ,
#                 name__contains=data['part_name'],
#                 is_sold=data['is_sold'], department__shop=data['shop']).all()
#         return render(self.request, 'search_result.html', locals())
