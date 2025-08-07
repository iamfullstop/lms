
# 📚 LMS E-learning Platform

A web-based Learning Management System (LMS) built using the Django framework. This platform is designed to deliver and manage educational content such as courses, lessons, and user enrollments. It also provides a RESTful API for frontend integrations or external usage.

---

## 🚀 Features

- 🔐 **User Authentication** – Secure user registration, login, and logout.
- 🎓 **Course Management** – Admins can create, update, and delete courses.
- 📂 **Content Structure** – Courses can be organized into modules and lessons.
- 🌐 **RESTful API** – Built with Django REST Framework for programmatic access to course and user data.
- 🗃️ **Database Integration** – Uses SQLite by default, with flexibility for other databases.

---

## 🛠️ Installation

Follow these steps to set up the project locally for development and testing.

### 1. Clone the Repository

```bash
git clone https://github.com/iamfullstop/lms.git
cd lms
````

### 2. Create and Activate a Virtual Environment

> Using a virtual environment is highly recommended to manage dependencies.

#### macOS/Linux:

```bash
python3 -m venv venv
source .venv/bin/activate
```

#### Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a Superuser (Optional)

```bash
python manage.py createsuperuser
```

Follow the prompts to set up a username, email, and password for the Django admin panel.

---

## ▶️ Usage

Start the development server:

```bash
python manage.py runserver
```

* App: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* Admin Panel: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 🧰 Technologies Used

* **[Django](https://www.djangoproject.com/)** – Main web framework
* **[Django REST Framework](https://www.django-rest-framework.org/)** – API development
* **SQLite** – Default development database (can be changed)

---

## 📝 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙌 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.


```

