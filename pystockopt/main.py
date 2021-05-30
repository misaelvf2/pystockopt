from datetime import date, timedelta
import option as opt
import position as pos
import riskprofile as rp

my_call = opt.Option('call', 7.33, 50.00, date.today() + timedelta(days=60))
print(my_call)

my_position = pos.Position(my_call, "long")

my_risk = rp.RiskProfile(my_position)
print(my_risk.profile)
print(my_risk.profit(price=25.00))
