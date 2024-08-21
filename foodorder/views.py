from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from . models import LoginForm
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request,'home.html')

def adduser(request):
    if request.method == 'POST':
        # Process form submission
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('<script>alert("Registration successful!"); window.location.href = "/";</script>')
    else:
        # Render the form for GET requests
        form = UserCreationForm()
    
    context = {'form': form}
    return render(request, 'adduser.html', context)

def login_view(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        pwd=request.POST.get('password')
        user=authenticate(request,username=uname,password=pwd)
        
        if user is not None:
            request.session['uid']=user.id
            login(request,user)
            return redirect('/')
        else:
            f=LoginForm
            context={'form':f}
            messages.error(request, 'Invalid username or password. Please try again.') 
            return render(request,'login.html',context)
    else:
        f=LoginForm
        context={'form':f}
        return render(request,'login.html',context)
    
def logout_view(request):
    logout(request)
    return redirect('/')

def about(request):
    return render(request,'about.html')


from django.db.models import Q 
from.models import Product,Cart,Category
def product_list(request):
    products = Product.objects.all()
    query = request.GET.get('q')
    
    if query:
        products = products.filter(
            Q(product_name__icontains=query) |
            Q(product_discription__icontains=query) |
            Q(category__category_name__icontains=query)  # Assuming Category model has a field 'category_name'
        )
    
    context = {
        'products': products,
        'query': query  # Pass the query back to the template to pre-fill the search input
    }
    return render(request, 'productlist.html', context)

def add_to_cart(request, pid=None):
    user = request.user
    product = get_object_or_404(Product, id=pid)
    cart_item, created = Cart.objects.get_or_create(user=user, product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('/clist')

from django.conf import settings
def cart_list(request):
    user = request.user
    cl = Cart.objects.filter(user=user)
    
    total_price = sum((item.product.product_price) * item.quantity for item in cl)
    final_price = total_price * 100
    
    context = {'cl': cl, 'total_price': total_price, 'final_price': final_price}
    context['razorpay_key_id']= settings.RAZORPAY_KEY_ID
    return render(request, 'cartlist.html', context)

def remove_from_cart(req, pid):
   item = Cart.objects.get(id=pid)
   # if item.quantity > 1:
   #    item.quantity -= 1
   #    return redirect('/clist')
   # else:
   # item.delete()
   item.delete()
   return redirect('/')

from django.views.decorators.csrf import csrf_exempt
from .models import cloth
import razorpay
def order(request):
    if request.method=='POST':
        name=request.POST.get('name')
        amount=int(request.POST.get('amount')) * 100
        print(name,amount)
        currency = 'INR'
        razorpay_client=razorpay.Client(auth=('rzp_test_6K659PBJWqIij9','kv0VVovqNqD37zzLhjiVVFXM'))
        payment = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='1'))
        print(payment)
        Cloth=cloth(name=name,amount=amount,payment_id = payment['id'])
        Cloth.save()
        return render(request,'order.html',{'payment': payment})
    else:
        return render(request,'order.html')
        
@csrf_exempt

def success_view(request):
    if request.method=='POST':
        a=request.POST
        print(a)
        return render(request,'success.html')
    else:
        return render(request,'success.html')

