from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

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
        is_rent=True if request.POST.get('is_rent', False) else False
    )
    p.save()
    return redirect('/index/', permanent=True)

@login_required
def overview(request):
    """
    display page to see overview of payments and rent since user joined
    """
    user = Housemate.objects.get(pk=request.user.pk)
    try:
        rents = Rent.objects.get(created__gte=user.date_joined)
    except Rent.DoesNotExist:
        rents = None
    payments = Payment.objects.filter(payment_date__gte=user.date_joined)
    print(payments[0].amount)
    return render(request, 'kommunabokhald/overview.html', {'rents': rents, 'payments': payments, 'user': user})
