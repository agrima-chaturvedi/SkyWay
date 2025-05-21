# ✈️ SkyWay - Airline Reservation System

A web-based Airline Reservation System developed using **Flask** (Python) and **MySQL**. This system allows users to search for flights, book tickets, manage bookings.<br>

---

## 🔧 Features

### 👤 User Functionality<br>
- ✅ User registration and login<br>
- 🔍 Flight search (based on source, destination, and date)<br>
- 🧾 Flight booking (with PNR generation)<br>
- 📄 View and download ticket details<br>
- ❌ Cancel bookings<br>
- 🧳 View journey and booking history
<br>


## 🛠️ Tech Stack<br>

| Layer           | Technology          |<br>
|----------------|---------------------|<br>
| Backend         | Flask (Python)      |<br>
| Frontend        | HTML, CSS, JavaScript |<br>
| Database        | MySQL               |<br>
| Authentication  | Flask-Login         |<br>


---

## 📁 Project Structure
Airline-Reservation-System/
├── app/<br>
│ ├── templates/ # HTML Templates<br>
│ ├── static/ # CSS, JS, Images<br>
│ ├── routes/ # Flask route files<br>
│ ├── models/ # Database models<br>
│ └── init.py # App factory<br>
├── config.py # MySQL credentials and app config<br>
├── run.py # App entry point<br>
├── requirements.txt # Project dependencies<br>
└── README.md # Project overview<br>

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+<br>
-  MySQL installed locally and running<br>
- MySQL user with privileges to create databases<br>
- Git<br>

### Setup Instructions

1. **Clone the repository:** <br>
git clone https://github.com/agrima-chaurvedi/SkyWay.git<br>
cd SkyWay<br>

2. Create a virtual environment & activate:

python -m venv venv<br>
source venv/bin/activate     # macOS/Linux<br>
venv\Scripts\activate        # Windows<br>

3.Install dependencies:

pip install -r requirements.txt<br>

Configure MySQL database:<br>

Open MySQL and run the schema SQL script (if provided).<br>
Or manually create the database and tables based on your models.<br>
Update config.py<br>
DB_CONFIG = {
    'host': 'localhost',
    'user': 'your_mysql_username',
    'password': 'your_mysql_password',
    'database': 'your_database_name'
}

## Run the application:

python run.py<br>

## Visit in browser:

http://localhost:5000<br>

📸 Screenshots
![image](https://github.com/user-attachments/assets/35b3e609-5093-4802-8cc9-dc99643d6605)
![image](https://github.com/user-attachments/assets/251286d2-4430-4f30-a581-ac8a930b7975)
![image](https://github.com/user-attachments/assets/754719dc-4458-4932-bb68-6b2b921e26c0)
![image](https://github.com/user-attachments/assets/ad7cdd08-eb8e-4c00-97c6-16c6ee1f1436)
![image](https://github.com/user-attachments/assets/ae29ca01-4cee-400a-a5e3-157c1a0baa5f)
![image](https://github.com/user-attachments/assets/50b8b8f6-2aa4-4fad-a286-0ff0019cc6be)
![image](https://github.com/user-attachments/assets/5f793f68-7f8d-4521-b5bf-a31da6895fba)

🤝 Contributing

Pull requests are welcome! To contribute:<br>

Fork the project<br>
Create your feature branch (git checkout -b feature/YourFeature)<br>
Commit your changes (git commit -m 'Add some feature')<br>
Push to the branch (git push origin feature/YourFeature)<br>
Open a pull request<br>

📃 License

This project is licensed under the MIT License. See LICENSE for details.
