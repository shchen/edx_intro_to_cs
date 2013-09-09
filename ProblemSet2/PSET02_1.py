balance = 4123
annualInterestRate = 0.2
monthlyPaymentRate = 0.04

totalPayment = 0
monthlyInterestRate = annualInterestRate / 12
for i in range(1, 13):
    minPayment = monthlyPaymentRate * balance
    monthlyUnpaid = balance - minPayment
    balance = monthlyUnpaid + monthlyInterestRate * monthlyUnpaid
    totalPayment += minPayment
    print("Month: " + str(i))
    print("Minimum monthly payment: " + str(round(minPayment, 2)))
    print("Remaining balance: " + str(round(balance, 2)))

print("Total paid: " + str(round(totalPayment, 2)))
print("Remaining balance: " + str(round(balance, 2)))
