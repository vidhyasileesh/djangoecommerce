from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from shop.models import Product

from cart.models import Cart, Account,Order




# Create your views here.
@login_required
def cartview(request):
    u = request.user
    cart = Cart.objects.filter(user=u)
    total = 0
    for i in cart:
        total += i.quantity * i.product.price

    return render(request, "cartview.html", {'c': cart, 'total': total})

@login_required
def addtocart(request, n):
    p = Product.objects.get(name=n)
    u = request.user  # current login user

    try:  # more one quantity undo ennu check chyn vendi function use chynm
        cart = Cart.objects.get(user=u, product=p)  # more one product or user undkil kodukn ulla condition
                                                     # if (cart.quantity < cart.product.stock):  # stock quantity vara maartme stock add chyn pattum quantity exceed aykth iriknm kodukunna cade  ulla function
        if(p.stock > 0):
            cart.quantity += 1  # more than one product undkil athu kood increment chyn ulla condition
            cart.save()
            p.stock -=1
            p.save()

    except:
        if (p.stock > 0):
            cart = Cart.objects.create(product=p, user=u, quantity=1)
            cart.save()
            p.stock -=1
            p.save()
    return cartview(request)

@login_required
def cart_remove(request, n):
    p = Product.objects.get(name=n)
    u = request.user
    try:
        cart = Cart.objects.get(user=u, product=p)

        if (cart.quantity > 1):  # quantity teerumbo cartil irunnu delete ay poknm. athnu anu ee function kodukunne
            cart.quantity -= 1
            cart.save()
            p.stock +=1
            p.save()
        else:
            cart.delete()
            p.stock += 1
            p.save()
    except:
        pass

    return cartview(request)

@login_required
def cart_delete(request, n):
    p = Product.objects.get(name=n)
    u = request.user
    try:
        cart = Cart.objects.get(user=u, product=p)
        cart.delete()
        p.stock += cart.quantity
        p.save()

    except:
        pass
    return cartview(request)

@login_required
def orderform(request):
    if (request.method == "POST"):
        a = request.POST['a']
        p = request.POST['p']
        n = request.POST['n']

        u = request.user
        cart = Cart.objects.filter(user=u)

        total = 0
        for i in cart:
            total += i.quantity * i.product.price

        try:
            num = int(n)
            ac = Account.objects.get(acctnum=num)

            if (ac.amount >= total):
                ac.amount = ac.amount - total
                ac.save()
                #return HttpResponse(ac.amount)

                for i in cart:
                    o=Order.objects.create(user=u, product=i.product, address=a, phone=p, no_of_items=i.quantity,ordered_status="paid")
                    o.save()
                cart.delete()
                msg="Your order placed successfully"
                return render(request,'orderdetail.html',{'msg':msg})

            else:

                msg="Insufficient Amount.You can't Place Order"
                return render(request,'orderdetail.html',{'msg':msg})


        except:
            pass

    return render(request, 'orderform.html')


@login_required
def orderview(request):
    u=request.user
    o=Order.objects.filter(user=u)
    return render(request,'orderview.html',{'o':o,'u':u.username})
