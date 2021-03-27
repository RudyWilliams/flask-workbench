from app import User, Budget

me = User.query.filter(User.user_name == "rudyw").first()
print(me.id)
print(me.user_name)
print(me.f_name)
print(me.l_name)
print(me.email)

print("--- The .budget property in User to go from one table to many table---")
my_budget_records = me.budget.all()
print([r.category for r in my_budget_records])

print("Using the backref to go from many table to one table")
# my_budget_obj = Budget.query.filter(Budget.user_id == me.id).all()
# or can go this route (prob more realistic use case)
my_budget_obj = Budget.query.get(1)
print(my_budget_obj.user.user_name)