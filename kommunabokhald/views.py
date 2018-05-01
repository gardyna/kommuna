from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from datetime import timedelta, date

from .models import Housemate, Payment, Rent, GroceryItem


# Create your views here.
def index(request):
    user = None
    if request.user.is_authenticated():
        user = Housemate.objects.get(pk=request.user.pk)
    return render(request, 'kommunabokhald/index.html', {'user': user})


@login_required
def payment(request):
    """
    takes post request and creates a payment with given information
    :return:
    """
    p = Payment(
        amount=int(request.POST['amount']),
        reason=request.POST.get('reason', ''),
        user=Housemate.objects.get(pk=request.user.pk),
        # is_rent is optional and can be None. therefore make an explicit check
        is_rent=True if request.POST.get('is_rent', False) else False
    )
    p.save()
    return redirect('/index/', permanent=True)


@login_required
def overview(request):
    """
    display page to see overview of payments and rent since user joined or according to params
    """
    user = Housemate.objects.get(pk=request.user.pk)
    # use max to limit searchable timespan to after user joined commune
    num_items = 0 if request.GET.get('from', False) else 15
    since = request.GET['from'] if request.GET.get('from', False) else user.date_joined.strftime('%Y-%m-%d')
    to = request.GET['to'] if request.GET.get('to', False) else date.today().__add__(timedelta(1)).strftime('%Y-%m-%d')
    try:
        rents = Rent.objects.filter(created__range=[since, to]).order_by('-created')[:num_items or None]
    except Rent.DoesNotExist:
        rents = None
    payments = (Payment.objects.filter(payment_date__range=[since, to], is_rent=False)
                .order_by('-payment_date'))[:num_items or None]
    user_payments = Payment.objects.filter(user=user, payment_date__range=[since, to], is_rent=True) \
                    .order_by('-payment_date')[:num_items or None]

    return render(request, 'kommunabokhald/overview.html', {
        'rents': rents,
        'payments': payments,
        'user': user,
        'userPayments': user_payments,
        'total': int(sum(r.house_rent / r.housemates_this_month for r in rents)),
        'from': since,
        'to': to,
    })


@login_required
def payments_in_timespan(request):
    """
    get all payments within requested timespan
    expect json: {from: date, to: date}
    date in format "yyyy-mm-dd"
    :return: json response
    """
    payments = Payment.objects.filter(payment_date__range=[request.GET['from'], request.GET['to']])
    return JsonResponse(payments)


@login_required
def grocery_list(request):
    """
    get the grocery list
    :param request:
    :return:
    """
    items = GroceryItem.objects.all()
    return render(request, 'kommunabokhald/groceries.html', {
        'items': items
    })


@login_required
def add_grocery_item(request):
    """
    add item to grocery list
    :param request:
    :return:
    """
    item = GroceryItem(
        name=request.POST['item']
    )
    item.save()
    return redirect('/groceries/')


@login_required
def remove_grocery_item(request, id):
    item = GroceryItem.objects.filter(pk=id)
    item.delete()
    return redirect('/groceries/')
