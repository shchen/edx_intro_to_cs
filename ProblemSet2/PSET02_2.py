def computeBalance(balance, fixedPayment, annualInterestRate):
    monthlyInterestRate = annualInterestRate / 12
    for i in range(1, 13):
        monthlyUnpaid = balance - fixedPayment
        balance = monthlyUnpaid + monthlyInterestRate * monthlyUnpaid
    return round(balance, 2)

step = 10
fixedPayment = 310
balance = 3329
annualInterestRate = 0.2
Unpaid = computeBalance(balance, fixedPayment, annualInterestRate)

while Unpaid > 0:
    balance = 3329
    annualInterestRate = 0.2
    fixedPayment += step
    Unpaid = computeBalance(balance, fixedPayment, annualInterestRate)

print("Lowest Payment: " + str(fixedPayment))
