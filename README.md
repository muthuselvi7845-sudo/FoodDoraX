\# 🍔 FoodDoraX – Online Food Ordering \& Delivery Management System



FoodDoraX is a web-based online food ordering and delivery management system developed using Django and MySQL.



The platform allows customers to browse restaurants and food items, add items to their cart, place orders, make payments, track orders, and manage their addresses. Restaurant and delivery-related operations can also be managed through the system.



\## 🚀 Features



\### 👤 Customer



\* User registration and login

\* Browse restaurants

\* View restaurant menus

\* View food item details

\* Add food items to cart

\* Update cart quantities

\* Place orders

\* Buy food items directly

\* Manage delivery addresses

\* View order history

\* Cancel orders

\* Review food items

\* Payment options



\### 🏪 Restaurant / Admin



\* Manage restaurants

\* Manage food items

\* Manage customer orders

\* Upload food items

\* Manage food item details

\* View order information



\### 🚴 Delivery



\* View available delivery orders

\* Accept/manage delivery orders

\* View delivery-related order information

\* Update delivery status



\## 🛠️ Technologies Used



\* \*\*Frontend:\*\* HTML5, CSS3

\* \*\*Backend:\*\* Python, Django

\* \*\*Database:\*\* MySQL

\* \*\*Payment:\*\* Razorpay

\* \*\*Version Control:\*\* Git \& GitHub



\## 📂 Project Structure



```text

FoodDoraX/

│

├── app/

│   ├── migrations/

│   ├── static/

│   │   └── css/

│   ├── templates/

│   ├── admin.py

│   ├── models.py

│   ├── urls.py

│   ├── views.py

│   └── tests.py

│

├── fooddelivery/

│   ├── settings.py

│   ├── urls.py

│   ├── asgi.py

│   └── wsgi.py

│

├── manage.py

├── .gitignore

└── README.md

```



\## ⚙️ Installation



\### 1. Clone the repository



```bash

git clone https://github.com/muthuselvi7845-sudo/FoodDoraX.git

```



\### 2. Open the project folder



```bash

cd FoodDoraX

```



\### 3. Create a virtual environment



```bash

python -m venv venv

```



\### 4. Activate the virtual environment



Windows:



```bash

venv\\Scripts\\activate

```



\### 5. Install dependencies



```bash

pip install django mysqlclient

```



If the project contains a `requirements.txt` file, use:



```bash

pip install -r requirements.txt

```



\## 🗄️ MySQL Database Setup



Create a MySQL database:



```sql

CREATE DATABASE fooddelivery;

```



Update the database configuration in Django settings using your own MySQL credentials.



Do not upload your MySQL password or other secret credentials to GitHub.



\## 🔄 Run Migrations



```bash

python manage.py makemigrations

python manage.py migrate

```



\## 👨‍💻 Create Superuser



```bash

python manage.py createsuperuser

```



Follow the instructions to create the Django admin account.



\## ▶️ Run the Project



```bash

python manage.py runserver

```



Open the application in your browser:



```text

http://127.0.0.1:8000/

```



\## 🔐 Security



Sensitive information such as:



\* MySQL passwords

\* API keys

\* Razorpay keys

\* Secret keys



should be stored securely and should not be committed to GitHub.



\## 🔮 Future Enhancements



\* Online order tracking

\* Improved delivery management

\* Restaurant dashboard

\* Advanced payment integration

\* Real-time order notifications

\* Mobile application

\* Improved recommendation system



\## 👩‍💻 Developer



\*\*Muthuselvi A\*\*



Python Full Stack Developer



GitHub: https://github.com/muthuselvi7845-sudo



