### Notes: Flask + DBs

<hr />

**db.relationship()**

[Docs here](https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/#simple-example)

```python
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    addresses = db.relationship('Address', backref='person', lazy=True)

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'),
        nullable=False)
```

In Person, we told it to create a column that references the Address class(model). By default it is a one-to-many relationship (for one-to-one uselist=False).
 - backref='person' -> declares a new property on the Address class. So you can reference person from Address by .person. E.g. you can use my_address.person to get the person at that address.
 - lazy= ... -> defines when the SQLAlchemy will load the data from the database.


<hr />

**Want to create a unique constraint on a combination of columns**
```python

class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    super_category = db.Column(db.String(15), nullable=True)
    category = db.Column(db.String(15))
    amount = db.Column(db.Float)
    __table_args__ = (
        db.UniqueConstraint(
            "user_id", "category", name="user_category_uniq_constraint"
        ),
    )
```
However, this code doesn't keep from adding new entries to the Budget table, it just creates NULL for the user_id.

Sol'n: Make ```nullable=False``` for user_id:
```python
class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    super_category = db.Column(db.String(15), nullable=True)
    category = db.Column(db.String(15), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    __table_args__ = (
        db.UniqueConstraint(
            "user_id", "category", name="user_category_uniq_constraint"
        ),
    )
```
This, along with the constraints on the User column, will keep data from being duplicated.

<hr/>

**Why adding new entries after the fact was not working**

```python
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
```

<hr/>

**Querying using relationship property and backref**

The property that is defined with `.relationship()` in the one table can reference the data in the many table by calling that property.
```python
me = User.query.filter(User.user_name == "rudyw").first()
my_budget_records = me.budget.all()
print([r.category for r in my_budget_records])
```
Output:
```
['eat_out', 'grocery', 'rent']
```

To go from the many table to the one table, we use what was defined as backref in the `.relationship()`.
```python
my_budget_obj = Budget.query.get(1)
print(my_budget_obj.user.user_name)
```
Output:
```
rudyw
```