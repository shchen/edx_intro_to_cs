def computeBalance(balance, fixedPayment, monthlyInterestRate):
    for i in range(1, 13):
        monthlyUnpaid = balance - fixedPayment
        balance = monthlyUnpaid + monthlyInterestRate * monthlyUnpaid
    return round(balance, 2)

balance = 999999
annualInterestRate = 0.18
monthlyInterestRate = annualInterestRate / 12

low = balance / 12
high = (balance * (1 + monthlyInterestRate) ** 12) / 12
fixedPayment = (low + high) / 12
step = 0.01
Unpaid = computeBalance(balance, fixedPayment, monthlyInterestRate)

while Unpaid > 0:
    balance = 999999
    annualInterestRate = 0.18
    fixedPayment += step
    Unpaid = computeBalance(balance, fixedPayment, monthlyInterestRate)

print("Lowest Payment: " + str(round(fixedPayment, 2)))
