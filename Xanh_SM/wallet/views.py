from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Wallet, Transaction
from app_admin.models import Student, Driver
from .forms import TransactionForm

def wallet(request):
    return render(request, 'app_home/Wallet/wallet.html')

def wallet_driver(request):
    drivers = Driver.objects.all()
    return render(request, 'app_home/Wallet/wallet_driver.html', {'drivers': drivers})

def wallet_student(request):
    students = Student.objects.all()
    return render(request, 'app_home/Wallet/wallet_student.html', {'students': students})

def wallet_balance(request, user_type, user_id):
    if user_type == 'driver':
        user = get_object_or_404(Driver, driver_id=user_id)
        wallet = Wallet.objects.filter(driver=user).first()  # Lấy ví của tài xế
    else:
        user = get_object_or_404(Student, id=user_id)
        wallet = Wallet.objects.filter(student=user).first()  # Lấy ví của học sinh

    balance = wallet.balance if wallet else 0  # Nếu chưa có ví thì mặc định số dư là 0

    return render(request, 'app_home/Wallet/wallet_balance.html', {
        'user': user,
        'balance': balance,
        'user_type': user_type
    })

# Nạp tiền vào ví
def deposit(request, user_type, user_id):
    if user_type == 'driver':
        driver = get_object_or_404(Driver, pk=user_id) 
        wallet = get_object_or_404(Wallet, driver=driver)  
    elif user_type == 'student':
        student = get_object_or_404(Student, pk=user_id)
        wallet = get_object_or_404(Wallet, student=student)  
    else:
        messages.error(request, "Loại người dùng không hợp lệ.")
        return redirect('wallet')

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.transaction_type = 'deposit'
            transaction.wallet = wallet
            transaction.save()
            
            messages.success(request, f"Đã nạp {transaction.amount} vào ví.")
            return redirect('wallet_balance', user_type=user_type, user_id=user_id)
    else:
        form = TransactionForm()

    return render(request, 'app_home/Wallet/wallet_deposit.html', {'form': form})

# Rút tiền từ ví
def withdraw(request, user_type, user_id):
    if user_type == 'driver':
        driver = get_object_or_404(Driver, pk=user_id)
        wallet = get_object_or_404(Wallet, driver=driver)
    elif user_type == 'student':
        student = get_object_or_404(Student, pk=user_id)
        wallet = get_object_or_404(Wallet, student=student)
    else:
        messages.error(request, "Loại người dùng không hợp lệ.")
        return redirect('wallet')

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.transaction_type = 'withdrawal'
            if wallet.balance >= transaction.amount:
                transaction.wallet = wallet
                transaction.save()
                messages.success(request, f"Đã rút {transaction.amount} từ ví.")
                return redirect('wallet_balance', user_type=user_type, user_id=user_id)
            else:
                messages.error(request, "Số dư không đủ để rút tiền.")
                return redirect('wallet_withdraw', user_type=user_type, user_id=user_id)
    else:
        form = TransactionForm()

    return render(request, 'app_home/Wallet/wallet_withdraw.html', {'form': form})

# Hoàn tiền
def refund(request, user_type, user_id):
    if user_type == 'driver':
        driver = get_object_or_404(Driver, pk=user_id)
        wallet = get_object_or_404(Wallet, driver=driver)
    elif user_type == 'student':
        student = get_object_or_404(Student, pk=user_id)
        wallet = get_object_or_404(Wallet, student=student)
    else:
        messages.error(request, "Loại người dùng không hợp lệ.")
        return redirect('wallet')

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.transaction_type = 'refund'
            transaction.wallet = wallet
            transaction.save()
            messages.success(request, f"Đã hoàn tiền {transaction.amount} cho ví.")
            return redirect('wallet_balance', user_type=user_type, user_id=user_id)
    else:
        form = TransactionForm()

    return render(request, 'app_home/Wallet/wallet_refund.html', {'form': form})

# Xem lịch sử giao dịch
def wallet_transaction_history(request, user_type, user_id):
    if user_type == 'driver':
        driver = get_object_or_404(Driver, pk=user_id)
        wallet = get_object_or_404(Wallet, driver=driver)
    elif user_type == 'student':
        student = get_object_or_404(Student, pk=user_id)
        wallet = get_object_or_404(Wallet, student=student)
    else:
        messages.error(request, "Loại người dùng không hợp lệ.")
        return redirect('wallet')

    transactions = Transaction.objects.filter(wallet=wallet)  # Sửa lỗi lấy transaction
    return render(request, 'app_home/Wallet/wallet_transaction_history.html', {'transactions': transactions})