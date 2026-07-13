# 🚀 Flask Blog Web Application

A full-stack blog web application built using **Flask**, featuring user authentication, blog post management, comments, and a PostgreSQL database.

The application is deployed online and demonstrates backend web development concepts such as authentication, database management, CRUD operations, and production deployment.

---

## 🌐 Live Demo

🔗 **Live Website:** https://flask-blog-with-users-eavp.onrender.com/

---

## 📸 Preview

<img width="955" height="534" alt="Screenshot 2026-07-13 230817" src="https://github.com/user-attachments/assets/ace46df6-6163-441f-8fb9-d0ea5e21343d" />
<img width="959" height="476" alt="Screenshot 2026-07-13 230831" src="https://github.com/user-attachments/assets/10c57533-f7f0-4737-b9bc-65336fa6da63" />
<img width="959" height="500" alt="Screenshot 2026-07-13 230954" src="https://github.com/user-attachments/assets/5f95721c-8c24-451a-b9c4-62a141006117" />
<img width="959" height="499" alt="Screenshot 2026-07-13 231007" src="https://github.com/user-attachments/assets/ab780f89-9abe-4c6a-a85c-0bdc2476feff" />
<img width="959" height="499" alt="Screenshot 2026-07-13 231025" src="https://github.com/user-attachments/assets/e07db3a3-c16a-4781-b8f4-d8574702df9a" />

---

## ✨ Features

* 🔐 User Registration and Login
* 🔑 Secure Password Hashing
* 👤 User Authentication
* 📝 Create Blog Posts
* ✏️ Edit Existing Posts
* 🗑️ Delete Blog Posts
* 💬 Comment on Blog Posts
* 👑 Admin-Only Blog Management
* 🗄️ PostgreSQL Database Integration
* 📱 Responsive Web Design
* ☁️ Deployed on Render

---

## 🛠️ Tech Stack

### Backend

* Python
* Flask
* Flask-SQLAlchemy
* Flask-Login
* Flask-WTF
* WTForms

### Database

* PostgreSQL
* SQLAlchemy ORM

### Frontend

* HTML5
* CSS3
* Bootstrap
* Jinja2

### Deployment

* Render
* Gunicorn

---

## 📂 Project Structure

```text
flask-blog/
│
├── static/
│   ├── assets/
│   └── css/
│
├── templates/
│   ├── header.html
│   ├── footer.html
│   ├── index.html
│   ├── post.html
│   ├── make-post.html
│   ├── login.html
│   ├── register.html
│   └── contact.html
│
├── main.py
├── forms.py
├── requirements.txt
├── Procfile
└── README.md
```

---

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Navigate to the Project Directory

```bash
cd YOUR_PROJECT_FOLDER
```

### 3. Create a Virtual Environment

```bash
python -m venv .venv
```

### 4. Activate the Virtual Environment

**Windows**

```bash
.venv\Scripts\activate
```

**macOS/Linux**

```bash
source .venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure Environment Variables

Create the required environment variables:

```text
SECRET_KEY=your_secret_key
DATABASE_URL=your_postgresql_database_url
```

### 7. Run the Application

```bash
python main.py
```

Open the application in your browser at:

```text
http://127.0.0.1:5000
```

---

## 🗄️ Database

The application uses **PostgreSQL** in production and **SQLAlchemy ORM** for database operations.

The database stores:

* Users
* Blog Posts
* Comments

Database relationships are implemented using SQLAlchemy.

---

## 🔐 Authentication

The application includes a complete authentication system using **Flask-Login**.

Passwords are securely hashed before being stored in the database.

Certain blog management operations are restricted to the administrator.

---

## 🚀 Deployment

The application is deployed on **Render** using **Gunicorn** as the production WSGI server.

The production application uses a PostgreSQL database.

> **Note:** The live deployment may depend on free-tier hosting and database availability.

---

## 📚 What I Learned

While building this project, I gained practical experience with:

* Flask application development
* Backend routing
* User authentication
* Password hashing
* Database relationships
* SQLAlchemy ORM
* PostgreSQL
* CRUD operations
* Jinja templating
* Flask forms and validation
* Environment variables
* Git and GitHub
* Production deployment with Render and Gunicorn

---

## 🔮 Future Improvements

* 🔍 Blog search functionality
* 🏷️ Blog categories and tags
* 👤 User profile pages
* ❤️ Like system
* 🌙 Dark mode
* 📧 Email verification
* 🔄 Password reset functionality

---

## 👨‍💻 Author

**Aradhya Biswas**

B.Tech Computer Science and Engineering Student
Python & Backend Development Enthusiast

---

## ⭐ Support

If you found this project interesting, consider giving the repository a ⭐!

Feedback and suggestions are always welcome.
