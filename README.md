# vehicle-parking-app-mad1
A multi-user parking management system using Flask and SQLite. Users can book 4-wheeler parking spots, and the admin can manage parking lots, users, and reservations.

## Technologies Used

- Flask (Backend)
- SQLite (Database)
- HTML, CSS, Bootstrap, Jinja2 (Frontend)

##  Issues Faced & Resolved (Milestone 1) 

1. **Issue:** I got confused initially about how the models connect to the database. It took me some time to understand how SQLAlchemy maps Python classes to tables.
   **Resolution:** I went through examples and slowly and gradually understood it.

2. **Issue:** I couldn't understand using `ForeignKey` and `db.relationship()`. I wasn’t sure which table should have the foreign key and how exactly the '.realatioship' worked works.
   **Resolution:** After understanding how one-to-many and many-to-one realtionships work, I was able to implement it properly.

##  Issues Faced & Resolved (Milestone 2)

1. **Issue:** I wasn’t confident with how SQLAlchemy ORM works, especially while creating the `User` model. I couldn't understand how classes connect to tables or how columns are actually defined.  
   **Resolution:** I revised the ORM concepts properly. Going through the User model line by line helped a lot, and now it’s much clearer.

2. **Issue:** I didn’t know how to do password hashing properly. I wasn’t sure how `generate_password_hash` and `check_password_hash` actually worked.  
   **Resolution:** I understood how to use Werkzeug’s functions for hashing and checking passwords.

3. **Issue:** I got confused while structuring the auth routes using Blueprints. I wasn’t sure how to separate them and connect everything back to the main app.  
   **Resolution:** After trying a few times, I figured out how to set up the `authentication_bp` and register it correctly in the app.
