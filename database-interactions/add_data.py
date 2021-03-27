from app import db, User, Budget

u1 = User(
    user_name="rudyw",
    password="p@ssw0rd",
    email="rudy@email.com",
    f_name="Rudy",
    l_name="Williams",
)
db.session.add(u1)
try:
    db.session.commit()
except Exception:
    db.session.rollback()

b1u1 = Budget(user_id=u1.id, super_category="food", category="grocery", amount=400.00)
b2u1 = Budget(user_id=u1.id, super_category="food", category="eat_out", amount=100.00)
b3u1 = Budget(user_id=u1.id, category="rent", amount=600.00)
db.session.add(b1u1)
db.session.add(b2u1)
db.session.add(b3u1)
try:
    db.session.commit()
except Exception:
    db.session.rollback()

# new user

u2 = User(
    user_name="belleb",
    password="pswrd",
    email="belle@email.com",
    f_name="Belle",
)
db.session.add(u2)
try:
    db.session.commit()
except Exception:
    db.session.rollback()

b1u2 = Budget(user_id=u2.id, super_category="food", category="grocery", amount=500.00)
b2u2 = Budget(user_id=u2.id, super_category="food", category="eat_out", amount=150.00)
b3u2 = Budget(user_id=u2.id, category="rent", amount=700.00)
# b4u2 = Budget(user_id=u2.id, super_category="savings", category="travel", amount="200")
# b5u2 = Budget(user_id=u2.id, super_category="savings", category="car", amount="500")
db.session.add(b1u2)
db.session.add(b2u2)
db.session.add(b3u2)
# db.session.add(b4u2)
# db.session.add(b5u2)
try:
    db.session.commit()
except Exception:
    db.session.rollback()

# need to get user_id from query bc the rollback takes away what would be a newly created ID
# ie there is no u2.id at this point since we rollback when seeing already have user_name
b4u2 = Budget(user_id=2, super_category="savings", category="travel", amount="200")
b5u2 = Budget(user_id=2, super_category="savings", category="car", amount="500")
db.session.add(b4u2)
db.session.add(b5u2)
try:
    db.session.commit()
except Exception as e:
    print(e)
    db.session.rollback()