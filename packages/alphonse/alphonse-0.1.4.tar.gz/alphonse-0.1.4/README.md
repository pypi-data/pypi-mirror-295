# Alphonse Database Manager


## What is?

Alphonse is an interface that makes it easier to manage databases using SQLAlchemy.
It provides a set of methods that make complex database queries more performant and easier to write.
For a project already leveraging SQLAlchemy, it only requires a few lines of code to start using it immediately.


---


## Getting started


### Requirements

- SQLAlchemy version `1.4` or higher  (`2.0+` for best performance)
- A SQLAlchemy "Engine" object.
  - This is the connection to the database.  It can be created using the `sqlalchemy.create_engine` method.
- A list of all defined SQLAlchemy models that all inherit from the same instance of a `sqlalchemy.ext.declarative.declarative_base.`


### Example setup

```python
""" Example setup for Alphonse Database Manager """

from alphonse import DbManager
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from my_models import MyModel1, MyModel2, MyModel3


# Create the singelton instance of the engine
db_connection_url: str = "postgresql://user:password@localhost:port/my_db_name"
engine: Engine = create_engine(db_connection_url)

# Create a list of all defined models that all inherit from the same
# instance of a "declarative_base" from sqlalchemy.ext.declarative

model_list: list = [MyModel1, MyModel2, MyModel3]

# Initialize the db_manager
db_manager: DbManager = DbManager(engine, model_list)
```

---


## **Methods and usage**

The main interface to making queries is the singleton `DbManager` object created in the setup.
It provides a set of methods that make database queries more performant and easier to write.
This singleton instance acts as an abstraction layer to prevent circular imports and to provide
a single point of access to the database, ensuring that all sessions are managed correctly.

---


### **`create()`**

The `db_manager.create()` method is used to create new rows in the database. 
A boolean is returned to determine if the creation was successful.


It takes two arguments:
- `table_key`: A string representing the model name.  This will be the same as the class name of the model.
- `req_payload`: A dictionary mapping of the columns and their values representing the row to be created.

##### **Example:**
```python
from db.objects import db_manager

# Create a new row in the "User" table
creation_map: dict = {
	"username": "new_user",
	"password": "password123",
	"email": "test@testing.net"
}

creation_was_successful: bool = db_manager.create("User", creation_map)
# creation_was_successful = True or False depending on if the creation was successful.

```

#### `map()` method
If your table model has specific requirements for creating a new row, you can define a
`map()` method directly on the model.

This method must take in a dictionary mapping of the columns, assign the key value pairs to the
attributes of the model, and return a mapped instance of the model class or `None` if the mapping fails.

The returned class instance must be a valid instance of the model with all required fields populated
(excepting nullable fields and auto-incrementing fields like primary key ids).

The `map()` method will be called automatically when the `db_manger.create()` method is used
and does not need to be called directly.
This means that the `req_payload` dictionary passed to
the `create()` method only needs to include the values to be assigned to the model in the user-defined `map()` method.

##### **Example model:**
```python
""" User table model. """

from typing import Optional

from sqlalchemy import Column, Integer, String, VARCHAR
from sqlalchemy.orm import relationship
# The below imports are theorhetical and are not included in the package.
# --------------------------------------------------------------------
# Base is the instatiated singleton instance of `declarative_base` orignally imported from
# sqlalchemy.ext.declarative.   All models in this theorhetical project should inherit from this same instance.
from db.objects.base import Base 
from utils.logger import logger


class User(Base):
  """ User orm model. """

  __tablename__ = "users"

  id = Column(Integer, primary_key=True, nullable=False)
  name = Column(String(50), unique=True, nullable=False)
  status = Column(String(20), nullable=False)
  website = Column(VARCHAR(255), nullable=True)

  
  @classmethod
  def map(cls, req_payload: dict) -> Optional["User"]:
	"""
	Map the `request_payload` dictionary to the User model.
	:param req_payload: A dictionary mapping of the columns in the table and their values representing the new row to be created.
	:return: A mapped instance of the User model or None if the mapping fails.
	"""
	try:
	# Create a new instance of the User model.
	  new_user: User = User(
	    # Use the `.get()` method to safely access the dictionary values and return None as a default if the key is not found.
		  name=req_payload.get("name"),
		  status=req_payload.get("status"),
		  partner_key=req_payload.get("partner_key"),
		  # In this example, the id column is an auto-incrementing primary key and the website column is nullable. 
          # Therefore, they not required to be filled in when the row is created.  If this method wasn't defined,
          # the `db_manager.create()` method would fail if the `req_payload` dictionary didn't include a `website` value.
	  )
	  # Return the mapped instance of the User model.
	  return new_users

	except (KeyError, AttributeError):
		logger.log_error("Error mapping the request payload to the User model.")
		# If the mapping fails, None is the expected return value to indicate that the mapping failed.
		return None

```

---

### **`create_and_fetch()`**

The `db_manager.create_and_fetch()` method is used to create new rows in the database. 
The newly created db row is returned as a dictionary.


It takes two arguments:
- `table_key`: A string representing the model name.  This will be the same as the class name of the model.
- `req_payload`: A dictionary mapping of the columns and their values representing the row to be created.

##### **Example:**
```python
from db.objects import db_manager

# Create a new row in the "User" table
creation_map: dict = {
	"username": "new_user",
	"password": "password123",
	"email": "test@testing.net"
}

new_user: dict = db_manager.create_and_fetch("User", creation_map)

# new_user = {
# 	"id": 4269,
# 	"username": "new_user",
# 	"password": "password123",
# 	"email": "test@testing.net"
# }

```

#### `map()` method
The map method for the `create_and_fetch()` method works the same way as
described above for the `create()` method.


---


### **`read()`**

The read method is used to retrieve rows from a single table in the database.
A dictionary of result(s) is returned, or None if the query fails.

It takes two required arguments and one optional argument:
- `table_key`: A string representing the model name.  This will be the same as the class name of the model.
- `search_params`: A dictionary mapping of the columns in the table and their values.
  Represents the search criteria for the query.
  See the `search_params argument` section below for more information.
- `select_params` An optional list of strings representing the columns to select from the db.
  Represents the filter parameters for the query.
  See the `select_params argument` section below for more information.

##### -**`search_params` argument**
The values in the `search_params` dictionary are used to filter the results of the query.
You can supply a single value or a list of values for each key in this dictionary (column in the table.)
For example: `{"status": "ACTIVE"}` or `{"status": ["ACTIVE", "SUSPENDED"]}`
Select the rows where the status is "ACTIVE" vs. select the rows where the status is "ACTIVE" or "SUSPENDED."

##### -**`select_params` argument**
The `select_params` argument is an optional list of strings representing the columns to select from the db.
They can be used to return partial data from the table if only certain values are needed.
The strings must match the column names in the table exactly as they are defined on the models.
If a valid list is provided, only the columns in the list will be returned.
Returns the full table row if the list is empty or not provided.
For example: `["id", "status"]`
Whatever the `search_params` return, only return the 'id' and 'status'
columns (and their value) for any results from the queried table.

#### **Example queries:**
```python
from typing import  Optional

from db.objects import db_manager

# =============
# BASIC EXAMPLE
# =============

# Return all rows from the "User" table with the a status of "ACTIVE".
user: Optional[dict] = db_manager.read(
	"User", {"status": "ACTIVE"}
)

# If one result is found:
# user = {
# 	"id": 1,
# 	"name": "test_user",
# 	"status": "ACTIVE",
# 	"website": "www.testwebsite.com"
# }

# If multiple results are found, they will be within a list at a key of "result."
# user = {
# 	"result": [
# 		{"id": 1, "name": "test_user", "status": "ACTIVE", "website": "www.testwebsite.com"},
# 		{"id": 55, "name": "test_user_55", "status": "ACTIVE", "website": None}
# 	]
# }

# If the no rows are found meeting the criteria:
# user = {}

# If an exception was raised during the read operation
# user = None


# ====================================
# EXAMPLE USING MULTIPLE SEARCH PARAMS
# ====================================

# Return all rows from the "User" table with the a status of "ACTIVE" or "SUSPENDED".
user: Optional[dict] = db_manager.read(
	"User", {"status": ["ACTIVE", "SUSPENDED"]}
)

# If multiple results are found,
# user = {
# 	"result": [
# 		{"id": 1, "name": "test_user", "status": "ACTIVE", "website": "www.testwebsite.com"},
#       {"id": 55, "name": "test_user_55", "status": "ACTIVE", "website": None},
# 		{"id": 55, "name": "test_user_56", "status": "SUSPENDED", "website": "www.othertestwebsite.com"}
# 	]
# }

# ===========================
# EXAMPLE USING SELECT PARAMS
# ===========================

# Return the id and status of all active users.
user: Optional[dict] = db_manager.read(
	"User",
	{"status": "ACTIVE"},
	["id", "status",]
)

# If one result is found:
# user = {
# 	"id": 1,
# 	"status": "ACTIVE",
# }

```


---


### **`update()`**

The update method is used to edit existing rows in the database. 
A boolean is returned to determine if the creation was successful.


It takes three arguments:
- `table_key`: A string representing the model name.  This will be the same as the class name of the model.
- `search_params`: A dictionary mapping of parameters pertinent to specifying the query. Represents the search criteria for the query. All columns in the dictionary must be present in the table.  See the `search_params argument` section below for more information.
- `insert_params`: Mapped dictionary of key/value pairs corresponding to db columns to be updated.
All columns in the dictionary must be present in the table.
Operations that leave orphaned rows will not be performed and will result in the operation failing.
##### -**`search_params` argument**
The values in the `search_params` dictionary are used to filter the results of the query.
You can supply a single value or a list of values for each key in this dictionary (column in the table.)
For example: `{"status": "ACTIVE"}` or `{"status": ["ACTIVE", "SUSPENDED"]}`
Select the rows where the status is "ACTIVE" vs. select the rows where the status is "ACTIVE" or "SUSPENDED."

#### **Example queries:**
```python
from db.objects import db_manager

# Find the row in the "User" table with the id of 1 and update the website column.
params_to_update: dict = {"website": "www.newwebsite.com"}
update_was_successful: bool = db_manager.update(
  "User",
  {"id": 1},
  params_to_update
)
# update_was_successful = True or False depending on if the update was successful


# Find the all rows in the "User" table with a status of "ACTIVE" or "SUSPENDED" and update the status column to "DELETED"
update_was_successful: bool = db_manager.update(
  "User",
  {"status": ["ACTIVE", "SUSPENDED"]},
  {"status": "DELETED"}
)
# update_was_successful = True or False depending on if the update was successful
```


---


### **`delete()`**

The delete method is used to remove existing rows from the database. 
A boolean is returned to determine if the creation was successful.

It takes two arguments:
- `table_key`: A string representing the model name.  This will be the same as the class name of the model.
- `search_params`:A dictionary mapping of parameters pertinent to specifying the query. Represents the search criteria for the query. All columns in the dictionary must be present in the table.  See the `search_params argument` section below for more information.
##### -**`search_params` argument**
The values in the `search_params` dictionary are used to filter the results of the query.
You can supply a single value or a list of values for each key in this dictionary (column in the table.)
For example: `{"status": "ACTIVE"}` or `{"status": ["ACTIVE", "SUSPENDED"]}`
Select the rows where the status is "ACTIVE" vs. select the rows where the status is "ACTIVE" or "SUSPENDED."

#### **Example queries:**
```python
from db.objects import db_manager

# Find the row in the "User" table with the id of 1 and delete it.
delete_was_successful: bool = db_manager.delete("User", {"id": 1})
# delete_was_successful = True or False depending on if the delete was successful

# Find all row(s) in the "User" table with a status of "ACTIVE" or "SUSPENDED" and delete them.
delete_was_successful: bool = db_manager.delete("User", {"status": ["DELETE", "SUSPENDED"]})
# delete_was_successful = True or False depending on if the delete was successful
```


---


### **`joined_read()`**

The joined_read method is used to retrieve rows from multiple tables in the database.
A dictionary of results is returned, or None is returned if the query fails.

It takes three required arguments and one optional argument:
- `starting_table`: A string representing the table where the read should start looking.  This will be the same as the class name of the model.
- `ending_table`: A string representing the table where the read should, inclusively, stop looking.  This will be the same as the class name of the model.
- `search_params`: This can be one of two datastructures:
  - A dictionary mapping of the columns in the starting table and their values representing the search criteria for the query.
  - A list of dictionary mappings each representing a table that will be traversed.
    Represents the search criteria for each table (in order traversed) for the query.
See `search_params argument` section below for more information.
- `select_params` An optional list representing the columns to select from the db to be used as filter parameters for the query.
  This can be one of two datastructures:
  - A list of strings representing the columns to select from the starting table.
  - A list of lists containing strings representing the columns to select from each table in the order they are traversed.
See `select_params argument` section below for more information.

#### -**search_params argument**
- If only a single dict of `search_prams` is provided,
    the JOINS statement will find all rows from related tables with a foreign key pointing at the found of the starting table.
    For example, if the `starting_table` is the "User" table, the list of `search_params` could look like:
    ```python
    # In these examples there are three related tables: "User", "Post", "Comments" and "Likes".
    # A User can have many Posts, a Post can have many Comments and a comment can have many Likes.
    db_manager.joined_read(
        "User", "Comments", {"id": 1}
    )
    # Or
      db_manager.joined_read(
        "User", "Comments", [{"id": 1}]
    )
    # This reads as:
    # find the User with an 'id' of 1,
    # then find the all Posts that have a 'user_id' of 1,
    # then find all Comments that have a 'post_id' that matches any of the found Posts.
    ```
    You can also use a list of values to broaden the search criteria, just like in the `read()` method.
    ```python
    db_manager.joined_read(
        "User", "Comments", {"status": ["ACTIVE", "SUSPENDED"]}
    )
    # Or
    db_manager.joined_read(
        "User", "Comments", [{"status": ["ACTIVE", "SUSPENDED"]}]
    )
    # This reads as:
    # find the all Users with a status of "ACTIVE" or "SUSPENDED",
    # then find the all Posts that have a 'user_id's that match any of the found Users,
    # then find all Comments that have a 'post_id' that matches any of the found Posts.
    ```

- If a list of these dictionaries is supplied, it must be the same length as the number of tables to be traversed
in the order that they are traversed.
  An empty dict is supplied if no additional search criteria is needed for a table in the JOINS statement.
For example, if the starting table is "User"
  from the below examples and the ending table is "Likes," the list of `search_param` would look like:

```python
  # In these examples there are three related tables: "User", "Post", "Comments" and "Likes".
  # A User can have many Posts, a Post can have many Comments and a comment can have many Likes.

  db_manager.joined_read(
    "User", "Likes", [{"id": 1}, {"title": "test_post"}, {}]
  )
  # This reads as find the User with an 'id' of 1,
  # then find the Post with a 'user_id' of 1 and a 'title' of "test_post,"
  # then find all Likes that have a 'post_id' that matches the id(s) of the Post called "test_post."

```

#### -**select_params argument**
- If no `select_params` are provided, the full row of each table will be returned.
- If only a single list of `select_params` is provided,
    the JOINS statement will only apply the filter to the first table in the JOINS statement.
    For example, if the `starting_table` is the "User" table from the below examples and
    a filter is applied, the list of select params would look like:
  - `["name"],` or `[["name"]]`
  This reads as, "whatever the `search_params` find,
    only return the 'name' column for any results from the User table."

- If a list of these lists is supplied, the filter is applied in order as the tables are traversed.  For example:

  - `[["name"],[],["id", "content"]]`
    This reads as, "whatever the `search_params` find, only return 
    the 'name' column for any results from the User table,
    the all columns (or the full row) for any results from the Post table,
    and only return the 'id' and 'content' columns for any results from the Comments table."

#### **Example queries:**
```python
from typing import  Optional

from db.objects import db_manager

# In these examples there are three related tables: "User", "Post", "Comments" and "Likes".
# A User can have many Posts, a Post can have many Comments and a comment can have many Likes.

# =============
# BASIC EXAMPLE
# =============

# Return the user with an 'id' of 1, all of the user's posts, & all post's comments.
result_object: Optional[dict] = db_manager.joined_read(
	"User",
    "Comments",
    {"id": 1}
)
# If some results are found:
# result_object: dict = {
# 	"User": [
#         {"id": 1, "name": "test_user", "status": "ACTIVE", "website": "www.testwebsite.com"}
#     ],
#     "Posts": [
#         {"id": 1, "user_id": 1, "title": "test_post", "content": "This is a test post."},
# 	      {"id": 2, "user_id": 1, "title": "test_post_2", "content": "This is a test post."}
#     ],
#     "Comments": [
#         {"id": 1, "post_id": 1, "content": "This is a test comment."},
#         {"id": 2, "post_id": 1, "content": "This is a test comment."},
#         {"id": 3, "post_id": 2, "content": "This is a test comment."},
#     ]
# }

# If no results are found:
# result_object: dict = {}

# If an exception was raised during the read operation
# result_object: dict = None


# ===========================
# EXAMPLE USING SELECT PARAMS
# ===========================

# Return the name of the user with an 'id' of 1, all of the user's posts, & all posts' comments.
result_object: Optional[dict] = db_manager.joined_read(
	"User",
    "Comments",
    {"id": 1},
    ["name"]
)

# If some results are found:
# result_object: dict = {
# 	"User": [{"name": "test_user"}],
#     "Posts": [
#         {"id": 1, "user_id": 1, "title": "test_post", "content": "This is a test post."},
# 	      {"id": 2, "user_id": 1, "title": "test_post_2", "content": "This is a test post."}
#     ],
#     "Comments": [
#         {"id": 1, "post_id": 1, "content": "This is a test comment."},
#         {"id": 2, "post_id": 1, "content": "This is a test comment."},
#         {"id": 3, "post_id": 2, "content": "This is a test comment."},
#     ]
# }

# ====================================
# EXAMPLE USING MULTIPLE SEARCH PARAMS
# ====================================

# Return the the user with the id of 1, the post belonging to the user with a title of "test_post", & all comments belonging to the post.
result_object: Optional[dict] = db_manager.joined_read(
	"User",
    "Comments",
    [{"id": 1}, {"title": "test_post"}, {}],
)

# If some results are found:
# result_object: dict = {
# 	"User": [
#         {"id": 1, "name": "test_user", "status": "ACTIVE", "website": "www.testwebsite.com"}
#     ],
#     "Posts": [
#         {"id": 1, "user_id": 1, "title": "test_post", "content": "This is a test post."},
#     ],
#     "Comments": [
#         {"id": 1, "post_id": 1, "content": "This is a test comment."},
#         {"id": 2, "post_id": 1, "content": "This is a test comment."},
#     ]
# }

# ====================================
# EXAMPLE USING MULTIPLE SELECT PARAMS
# ====================================

# Return the name of the user with an "id" of 1, full rows ofall of that user's posts, & the "id" and "content" of all posts'"comments."
result_object: Optional[dict] = db_manager.joined_read(
	"User",
    "Comments",
    {"id": 1},
    [["name"],[],["id", "content"]]
)

# If some results are found:
# result_object: dict = {
# 	"User": [
#         {"name": "test_user"}
#     ],
#     "Posts": [
#         {"id": 1, "user_id": 1, "title": "test_post", "content": "This is a test post."},
# 	      {"id": 2, "user_id": 1, "title": "test_post_2", "content": "This is a test post."}
#     ],
#     "Comments": [
#         {"id": 1, "content": "This is a test comment."},
#         {"id": 2, "content": "This is a test comment."},
#         {"id": 3, "content": "This is a test comment."},
#     ]
# }

# ===============================================================
# EXAMPLE USING MULTIPLE SEARCH PARAMS AND MULTIPLE SELECT PARAMS
# ===============================================================

# Return the 'name' of the user with an `id` of 1, all posts belonging to the user with a title of "test_post", & and the 'id' and 'conent' of each comment belonging to the post.
result_object: Optional[dict] = db_manager.joined_read(
	"User",
    "Comments",
    [{"id": 1}, {"title": "test_post"}, {}],
    [["name"],[],["id", "content"]]
)

# If some results are found:
# result_object: dict = {
# 	"User": [
#         {"name": "test_user"}
#     ],
#     "Posts": [
#         {"id": 1, "user_id": 1, "title": "test_post", "content": "This is a test post."},
#     ],
#     "Comments": [
#         {"id": 1, "content": "This is a test comment."},
#         {"id": 2, "content": "This is a test comment."},
#         {"id": 3, "content": "This is a test comment."},
#     ]
# }

```


---


### **`count()`**

The count method is used to count existing rows that meet criteria in the database.
A dictionary is returned with a count of the rows that meet the criteria, or None is returned if the count fails.

It takes two arguments:
- `table_key`: A string representing the model name.  This will be the same as the class name of the model.
- `search_params`:A dictionary mapping of parameters pertinent to specifying the query. Represents the search criteria for the query. All columns in the dictionary must be present in the table.  See the `search_params argument` section below for more information.
##### -**`search_params` argument**
The values in the `search_params` dictionary are used to filter the results of the query.
You can supply a single value or a list of values for each key in this dictionary (column in the table.)

#### **Example queries:**
```python
from db.objects import db_manager

# Count the number of rows in the "User" table that have a status of "DELETED".
count: dict = db_manager.count("User", {"status": "DELETED"})

# Count the number of rows in the "User" table that have a status of "DELETED" or "SUSPENDED".
count: dict = db_manager.count("User", {"status": ["DELETED", "SUSPENDED"]})


# If no rows are found meeting the search criteria:
# count = {"count": 0}

# If some rows are found meeting the search criteria:
# count = {"count": 5}

# If an exception was raised during the count operation:
# count = None 
```

---


### **Advanced Options**

Certain methods have additional options that can be used to further specify the query.


#### **search_params options**

- Available to the `read()`, `update()`, `delete()`, `joined_read()`, and `count()` methods.
- equality operators:

  - You can apply equality operators to the search parameters concatenating the operator to the end of the column name key.  The valid operators are:
    - `==` for "equals" (default if no operator is provided)
    - `!=` for "not equals"
    - `<` for "less than"
    - `<=` for "less than or equal to"
    - `>` for "greater than"
    - `>=` for "greater than or equal to"
  
    For example, if you want to return all rows from the "User"
    table where the "id" is greater than 5, you would use: `{"id>": 5}`.

  - If a column name has no operator concatenated to the end of it, the operator will be used instead of the default "==" operator.
  - The data type of the value must be compatible with the operator used.  For example, if you use the "<" operator, the value must be a number or a date. If the operator is not valid for the column type, the query will fail.
  - If an equality operator is used when multiple values are provided for a column,
    the operator will be applied to each value in the list.
  For example, if you use `{"status!=": ["ACTIVE", "SUSPENDED"]}`,
    the query will return all rows where the status is not "ACTIVE"
    or "SUSPENDED."

  #### **Example queries:**

```python
import datetime
from db.objects import db_manager

# Return all rows from the "User" table with the a status is not "ACTIVE" or "SUSPENDED".
users: dict = db_manager.read(
  "User", {"status!=": ["ACTIVE", "SUSPENDED"]}
)

# Delete all rows from the Users table with an "id" that is less than or equal to 4000 and a status of "DELETED."
delete_was_succesful: bool = db_manager.delete(
  "User", {"id<=": 4000, "status": "DELETED"}
)

# Find all rows in the User table that were created on or before October 1, 2021
# with a "status" of "DELETED" or "SUSPENDED" and update each rows' "status" to "ACTIVE".
update_was_successful: bool = db_manager.update(
  "User",
  {"created_date<=": datetime.date(year=2021, month=10, day=1), "status": ["DELETED", "SUSPENDED"]},
  {"status": "ACTIVE"}
)

```

#### **select_params options**

- Available to the `read()` and`joined_read()` methods.
- Distinctly selected columns:
  - You can specify that only distinct rows are returned by using the `%` concatenated
  on to the back of a string value from the `select_params` list.
  For example, if you want to return only distinct rows for the "name" column, you would use: `["name%"]`
  - Distinctly selected columns can be used in conjunction with normal `select_params.` For example,
  if you want to return only distinct rows for the "name" column and all rows for the "id" and "content" columns.
  You would use: `["name%", "id", "content"]`
  - All distinct columns must be at the beginning of the `select_params` list.  If they are not, the query will fail.


  #### **Example queries:**

```python
import datetime
from db.objects import db_manager

# Return the User rows with with an "ACTIVE" status and return distinct "name" values and all "id" and values.
users: dict = db_manager.read(
  "User", {"status": "ACTIVE"}, ["name%", "id",]
)

```


### **Complex Examples**
```python
import datetime
from db.objects import db_manager

# In these examples there are three related tables: "User", "Post", "Comments" and "Likes".

# Return the distinct name and any id of all rows from the Users table that do not have a status of "DELETED" or "SUSPENDED".
# Return the full row of all Posts that have a user_id that matches any of the found Users and were created on or before October 1, 2021.
# Return the id and content of all Comments that have a post_id that matches any of the found Posts.
query_results: dict = db_manager.joined_read(
    "User",
    "Likes",
    [{"status!=": ["DELETED", "SUSPENDED"]}, {"created_date<":datetime.date(year=2021, month=10, day=1)}, {}, {}],
    [["name%", "id"], [], ["id", "content"], []]
)

```