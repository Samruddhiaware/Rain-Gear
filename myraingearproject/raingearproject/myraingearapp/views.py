from django.shortcuts import render, redirect
from .models import User, Product, cart, Order, Payment, Orderdetail
from django.db.models import Q  
from .forms import createform
from datetime import date
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.hashers import make_password, check_password
import razorpay
from raingearproject import settings

# Create your views here.
def register(request):
    if request.method == "GET":
        return render(request, 'register.html')
    elif request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        epassword = make_password(password)
        usertype = request.POST.get('usertype')
        address_line1 = request.POST.get('address1')
        address_line2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        contact = request.POST.get('contact')        
        userobject = User(name=name, email=email, password=epassword, usertype=usertype, address_line1=address_line1, address_line2=address_line2, city=city, state=state, pincode=pincode, contact=contact)
        print(userobject)
        userobject.save()
        return redirect('../login/')
    
def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        username = request.POST.get('email')
        password = request.POST.get('password')

        print(username, password)
        user = User.objects.filter(email = username)
        print("user: ", user)
        if user:
            userobject = User.objects.get(email = username)
            print("userobject: ", userobject)
            flag = check_password(password, userobject.password)
            print("flag", flag)
            if flag:
                request.session['sessionvalue'] = userobject.email
                usertype = userobject.usertype
                username = userobject.name
                if usertype == 'buyer':
                    return redirect('../productlist/')                    
                else:
                    print('in else of flag')
                    productobj = Product.objects.all()                   
                    return redirect('../sellerproductlist/')
            else:
                return render(request, 'login.html', {'message':'Incorrect username or password!'})
        else:
            return render(request, 'login.html', {'message':'Incorrect username or password!'})


def search(request):
    if request.method == "POST":
        searchdata = request.POST.get('searchquery')
        productobj = Product.objects.filter(Q(name__icontains =searchdata)|Q(features__icontains=searchdata))
        return render(request, 'productlist.html', {'productobj': productobj})

class Productlist(ListView):
    model = Product
    template_name = 'productlist.html'
    context_object_name = 'productobj'

    def get_context_data(self, **kwargs):
        data = self.request.session['sessionvalue']
        context = super().get_context_data(**kwargs)
        context['session'] = data
        return context

class Sellerproductlist(ListView):
    model = Product
    template_name = 'sellerproductlist.html'
    context_object_name = 'productobj'

class Addproduct(CreateView):
    model = Product
    form_class = createform
    template_name = "addproduct.html"
    success_url = reverse_lazy('sellerproductlist')

class Updateproduct(UpdateView):
    model = Product
    form_class = createform
    template_name = 'updateproduct.html'
    success_url = reverse_lazy('sellerproductlist')

class Productdetail(DetailView):
    model = Product
    template_name = 'productdetail.html'
    context_object_name = 'i'

class Deleteproduct(DeleteView):
    model = Product
    template_name = 'deleteproduct.html'
    success_url = reverse_lazy('sellerproductlist')

class Userproductdetail(DetailView):
    model = Product
    template_name = 'details.html'
    context_object_name = 'i'
    
    def get_context_data(self, **kwargs):
        data = self.request.session['sessionvalue']
        context = super().get_context_data(**kwargs)
        context['session'] = data
        return context


def addtocart(request):
    product_id = request.POST.get("product_id")
    print(product_id)
    usersession = request.session['sessionvalue']  # email of user
    # date = request.POST.get('servicedate')
    # time = request.POST.get('servicetime')
    userobj = User.objects.get(email = usersession) #fetch record from database table using email from session
    productobj = Product.objects.get(id = product_id)

    flag = cart.objects.filter(user_id = userobj.id, product_id = productobj.id)
    if flag:
        cartobj = cart.objects.get(user_id = userobj.id, product_id = productobj.id)            
        cartobj.quantity = cartobj.quantity + 1
        cartobj.totalamount = productobj.price * cartobj.quantity
        cartobj.save()
    else:
        cartobj = cart(user_id = userobj, product_id = productobj, quantity = 1, totalamount = productobj.price*1 )
        cartobj.save()      
    
    return redirect('../productlist/')

def viewcart(request):   
    usersession = request.session['sessionvalue']  # email of user    
    userobj = User.objects.get(email = usersession)
    cartobj = cart.objects.filter(user_id = userobj.id)

    return render(request, 'cart.html', {'cartobj': cartobj, 'session': usersession})   

def changequantity(request):
    useremail = request.session['sessionvalue']
    product_id = request.POST.get('product_id') 
    userobj = User.objects.get(email = useremail)
    productobj = Product.objects.get(id = product_id)
    cartobj = cart.objects.get(user_id = userobj.id, product_id = productobj.id)

    if request.POST.get('changequantity') == '+':
        cartobj.quantity = cartobj.quantity + 1
        cartobj.totalamount = cartobj.quantity * productobj.price
        cartobj.save()
    
    elif request.POST.get('changequantity') == '-':
        if cartobj.quantity == 1:
            cartobj.delete()
        else:
            cartobj.quantity = cartobj.quantity - 1
            cartobj.totalamount = cartobj.quantity * productobj.price
            cartobj.save()

    return redirect('../viewcart/') 

def removefromcart(request):
    useremail = request.session['sessionvalue']
    product_id = request.POST.get('product_id')
    print(product_id)
    userobj = User.objects.get(email = useremail)
    productobj = Product.objects.get(id = product_id)
    cartobj = cart.objects.get(user_id = userobj.id, product_id = productobj.id)

    if cartobj:
        cartobj.delete()
    return redirect('../viewcart/')

def summary(request):
    usersession = request.session['sessionvalue'] 
    userobj = User.objects.get(email = usersession)
    cartobj = cart.objects.filter(user_id = userobj.id)

    totalbill = 0
    count = 0
    for i in cartobj:
        totalbill = totalbill + i.totalamount
        count = count + 1    
    return render(request, 'summary.html' , {'session': usersession, 'totalbill': totalbill, 'cartobj': cartobj, 'count': count})


def payment(request):
    firstname = request.POST.get('fn')
    lastname = request.POST.get('ln')
    address = request.POST.get('address')
    state = request.POST.get('state')
    city = request.POST.get('city')
    pincode = request.POST.get('pin')
    phonenumber = request.POST.get('phone')
    datevar = date.today()
    orderobj = Order(firstname=firstname, lastname=lastname, address = address, state=state, city=city, pincode=pincode, phonenumber=phonenumber, orderdate=datevar, orderstatus = 'pending')
    orderobj.save()

    orderno = str(orderobj.id)+str(datevar).replace('-','')
    orderobj.ordernumber = orderno
    orderobj.save()
    print('orderobj: ', orderobj) 

    usersession = request.session['sessionvalue'] 
    print('usersession: ', usersession)
    userobj = User.objects.get(email = usersession)
    username = userobj.name
    cartobj = cart.objects.filter(user_id = userobj.id)
    print('cartobj: ', cartobj)

    totalbill = 0
    count = 0
    for i in cartobj:
        totalbill = totalbill + i.totalamount
        count = count + 1
            
    from django.core.mail import EmailMessage
    sm = EmailMessage('Order placed', 'Your order from the pet store app has been placed, total bill is '+str(totalbill), to=['samruddhiaware@gmail.com'])
    sm.send()

    # authorize razorpay client with API Keys.
    razorpay_client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
 

    currency = 'INR'
    amount = 20000  # Rs. 200
 
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount, currency=currency, payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = '../serviceview'
 
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZORPAY_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    print("context: ", context)

    return render(request, 'payment.html', {'orderobj': orderobj, 'session': usersession, 'cartobj': cartobj, 'totalbill': totalbill, 'context':context, 'firstname': firstname,})


def paymentsuccess(request):
    orderno = request.GET.get('order_id')
    tid = request.GET.get('payment_id')
    print('orderid: ', orderno)
    print('tid: ', tid)
    usersession = request.session['sessionvalue'] 
    print('usersession: ', usersession)
    userobj = User.objects.get(email = usersession)
    print('userobj: ', userobj)
    cartobj = cart.objects.filter(user_id = userobj.id)
    print('cartobj: ', cartobj)
    orderobj = Order.objects.get(ordernumber = orderno)
    print('orderobj: ', orderobj)   

    paymentobj = Payment(userid = userobj, orderid = orderobj, paymentmode = 'razorpay', paymentstatus='paid', transactionid = tid)
    paymentobj.save() 
    print('paymentobj: ', paymentobj)

    for i in cartobj:
        orderdetailobj = Orderdetail(ordernumber = orderno, userid = userobj, serviceid=i.service_id, totalprice=i.totalamount,  paymentid=paymentobj)
        orderdetailobj.save()  
        print('orderdetailobj: ', orderdetailobj)
        i.delete()

    return render(request, 'paymentsuccess.html', {'orderdetailobj': orderdetailobj, 'paymentobj': paymentobj, 'session': usersession})

def logout(request):
    del(request.session['sessionvalue'])
    return redirect('../login/')

    
