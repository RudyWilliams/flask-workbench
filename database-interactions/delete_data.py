from app import db, User, Budget

# say we want to delete user2's car savings (bought a car!)
# we first query for her budget item's id
user2_record = User.query.get(2)
print([(r.id, r.category) for r in user2_record.budget.all()])

user2_car_budget_record = user2_record.budget.filter(Budget.category == "car").first()
print(user2_car_budget_record.id)
print(user2_car_budget_record.category)

# delete that record from budget
db.session.delete(Budget.query.get(user2_car_budget_record.id))
try:
    db.session.commit()
except Exception:
    db.session.rollback()

print([(r.id, r.category) for r in user2_record.budget.all()])