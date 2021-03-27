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

<hr/>

**Deleting Records**

Here are the model definitions:
```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_name = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(35), unique=True, nullable=False)
    f_name = db.Column(db.String(25), nullable=False)
    l_name = db.Column(db.String(25), nullable=True)
    budget = db.relationship("Budget", backref="user", lazy="dynamic")


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

> First, deleting a record from the many table (Budget)

Say we want to delete the second user's 'car' category (maybe she bought a car and doesn't need to save for it anymore). First let's grab that user's record:
```python
user2_record = User.query.get(2)
```
We can use the `.budget` property to access user2's Budget data. For example, to see the `id` and `category` fields:
```python
print([(r.id, r.category) for r in user2_record.budget.all()])
```
Output:
```
[(8, 'car'), (5, 'eat_out'), (4, 'grocery'), (6, 'rent'), (7, 'travel')]
```
We see that the `id` for the 'car' `category` is 8. We don't need to know this but it's nice to check that we have the correct id for deleting.
```python
user2_car_budget_record = user2_record.budget.filter(Budget.category == "car").first()
print(user2_car_budget_record.id)
print(user2_car_budget_record.category)
```
Output:
```
8
car
```
Confirms we have the correct method for getting the car record for the second user. Our actual code can then look like:
```python
user2_record = User.query.get(2)
# to see in action
print([(r.id, r.category) for r in user2_record.budget.all()])

user2_car_budget_record = user2_record.budget.filter(Budget.category == "car").first()
db.session.delete(Budget.query.get(user2_car_budget_record.id))
try:
    db.session.commit()
except Exception:
    db.session.rollback()

# to see in action
print([(r.id, r.category) for r in user2_record.budget.all()])
```
Output:
```
[(8, 'car'), (5, 'eat_out'), (4, 'grocery'), (6, 'rent'), (7, 'travel')]
[(5, 'eat_out'), (4, 'grocery'), (6, 'rent'), (7, 'travel')]
```

> Now Deleting From the One Table (User)

```python
user1_record = User.query.get(1)
print(user1_record.user_name)

db.session.delete(user1_record)
try:
    db.session.commit()
except Exception as e:
    print(e)
    db.session.rollback()
```
Output:
```
(sqlite3.IntegrityError) NOT NULL constraint failed: budget.user_id
[SQL: UPDATE budget SET user_id=? WHERE budget.id = ?]
[parameters: ((None, 1), (None, 2), (None, 3))]
(Background on this error at: http://sqlalche.me/e/14/gkpj)
```
"SQLAlchemy’s default behavior is to instead de-associate address1 and address2 from user1 by setting their foreign key reference to NULL." - [sqlalchemy docs](https://docs.sqlalchemy.org/en/14/orm/cascades.html#unitofwork-cascades)

We need to deal with cascading. This is needed anyways so that when we delete a user, the Budget records are also removed. Also from  the docs

> `delete` cascade on one-to-many relationships is often combined with `delete-orphan` cascade, which will emit a DELETE for the related row if the “child” object is deassociated from the parent. The combination of delete and delete-orphan cascade covers both situations where SQLAlchemy has to decide between setting a foreign key column to NULL versus deleting the row entirely.

> An additional option, `all` indicates shorthand for "save-update, merge, refresh-expire, expunge, delete", and is often used as in "all, delete-orphan" to indicate that related objects should follow along with the parent object in all cases, and be deleted when de-associated.

We need to update the model definitions. Well actually just the User model. But we delete the old DB to start fresh and re-initialize everything.

```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_name = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(35), unique=True, nullable=False)
    f_name = db.Column(db.String(25), nullable=False)
    l_name = db.Column(db.String(25), nullable=True)
    budget = db.relationship(
        "Budget", backref="user", lazy="dynamic", cascade="all, delete, delete-orphan"
    )
```

The `cascade="all, delete, delete-orphan"` is the only change. Now if we run the code:

```python
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
```
Output:
```
[1, 2]
rudyw
[2]
```

Looking at the tables shows that user 1 was deleted along with all records of user 1 in the Budget table.