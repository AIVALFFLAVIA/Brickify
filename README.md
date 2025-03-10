Brickify
Overview
Brickify is a web-based application for construction company leaders to manage their business efficiently. It provides tools for handling companies, projects, tasks, employees, materials, suppliers, financial transactions, and equipment.
Features
•	User Authentication: Login, register, and logout functionality.
•	Role-Based Access Control: Company leaders manage only their data.
•	CRUD Operations: Manage companies, projects, tasks, employees, clients, materials, suppliers, and transactions.
•	Dashboard: Separate views for admins and company leaders.
•	Responsive UI: User-friendly design with an intuitive layout.
Tech Stack
•	Backend: Django (Python)
•	Frontend: HTML, CSS, JavaScript
•	Database: SQLite (default), PostgreSQL/MySQL (optional for production)
Installation
1.	Clone the repository: 
2.	git clone https://github.com/AIVALFFLAVIA/Brickify.git
3.	cd Brickify
4.	Set up a virtual environment: 
5.	python -m venv venv  
6.	source venv/bin/activate  # On Windows: venv\Scripts\activate  
7.	Install dependencies: 
8.	pip install -r requirements.txt  
9.	Apply migrations: 
10.	python manage.py migrate  
11.	Create a superuser: 
12.	python manage.py createsuperuser  
13.	Run the server: 
14.	python manage.py runserver  
15.	Access the application at: http://127.0.0.1:8000/
Troubleshooting
•	Migrations issue? Run: 
•	python manage.py makemigrations && python manage.py migrate  
•	Static files not loading? Run: 
•	python manage.py collectstatic  
•	Permission issues? Check user roles in the admin panel.

