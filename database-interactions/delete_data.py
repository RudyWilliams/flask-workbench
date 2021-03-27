from app import db, User, Budget

# deleting from the many table
# user2_record = User.query.get(2)
# print([(r.id, r.category) for r in user2_record.budget.all()])

# user2_car_budget_record = user2_record.budget.filter(Budget.category == "car").first()

# db.session.delete(Budget.query.get(user2_car_budget_record.id))
# try:
#     db.session.commit()
# except Exception:
#     db.session.rollback()

# print([(r.id, r.category) for r in user2_record.budget.all()])


# deleting from the one table
print([r.id for r in User.query.all()])
user1_record = User.query.get(1)
print(user1_record.user_name)

db.session.delete(user1_record)
try:
    db.session.commit()
except Exception as e:
    print(e)
    db.session.rollback()

print([r.id for r in User.query.all()])
