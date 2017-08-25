from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

import datetime

from .models import Housemate, Payment, Rent


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
        reason=request.POST['reason'],
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
    since = request.GET['from'] if request.GET.get('from', False) else user.date_joined.strftime('%Y-%m-%d')
    to = request.GET['to'] if request.GET.get('to', False) else datetime.date.today().strftime('%Y-%m-%d')
    try:
        rents = Rent.objects.filter(created__range=[since, to])
    except Rent.DoesNotExist:
        rents = None
    payments = (Payment.objects.filter(payment_date__range=[since, to], is_rent=False)
                .order_by('-payment_date'))
    print('payments', payments)
    userPayments = Payment.objects.filter(user=user, payment_date__range=[since, to], is_rent=True)
    return render(request, 'kommunabokhald/overview.html',{
                'rents': rents,
                'payments': payments,
                'user': user,
                'userPayments': userPayments,
                'total': sum(p.amount for p in userPayments),
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
