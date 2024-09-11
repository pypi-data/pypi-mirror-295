# CRUD operations for interacting with the DB.
This module provides an interface to interact with the DB.

# Methodology
All crud operations handle their own internal logic. For example, UserAccount.create()
will also set up any required child tables.

--- Omitted invalid CRUD operations
It is not possible to create or delete child tables in cases where it would conflict with the DB schema. 
In these cases, invalid CRUD operations (e.g. deleting the UserLoginTbl for a user, but not the UserAccount) 
are simply not provided as a method.

# Common functions
The following represents the core functionality which will be implemented across most tables.
Note: Many tables will also have their own unique CRUD operations, e.g. getting the password hash.
TODO ^ Apply to individual tables, or to the parent entity?

--- TblName.create()
Create this entity and setup all child tables. This is the default creation method.
Some tables may include optional creation methods.
This method is present on:
  Primary entities (True parents)
  Child tables that are optional (The parent can exist without them)
This method does not exist on:
  Child tables that cannot exist without a parent. Instead, the parent should handle their creation.

--- TblName.update()
Update values in this table. This method should exist on all tables.

--- TblName.delete()
Deletion of child tables should be handled automatically via the ForeignKey ondelete="CASCADE" constraints.
This method is present on:
  Primary entities (True parents)
  Child tables that are optional (The parent can exist without them)
This method does not exist on:
  Child tables that cannot exist without a parent. Instead, the parent should be deleted directly.

--- TODO how to handle gets? get_one? get_many? get_by_attr?
Consider best workflow for getting/reading data. A flexible re-usable approach or per-class approach
with only the necessary implementations (e.g. get_by_email, get_by_project_uuid)
