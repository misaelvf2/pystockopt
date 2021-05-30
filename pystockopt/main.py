from datetime import date, timedelta
import option as opt
import trade as td
import riskprofile as rp

my_call = opt.Option('call', 7.33, 50.00, date.today() + timedelta(days=60))
my_trade = td.Trade(my_call, "long")

my_risk = rp.RiskProfile(my_trade)
print(my_risk.profile)
print(my_risk.profit(price=25.00))
