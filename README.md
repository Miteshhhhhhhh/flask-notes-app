# Flask Notes App
## 🚀 Live Demo
**[Click here to try the app](https://flask-notes-app-rl4o.onrender.com)**

---
## 📸 Screenshot
<img width="1360" height="695" alt="notes-app" src="https://github.com/user-attachments/assets/cd09a281-3508-46de-9379-9ac93b7d94fa" />


A simple notes app built with Flask. Add and delete notes easily. Deployed on Render.

### **Features**
- Create new notes
- View all notes on homepage
- Edit existing notes
- Delete notes
- Notes stored in SQLite database
- Deployed on Render with Gunicorn
- **User Authentication** - Secure login/register with password hashing
- **Search Notes** - Search by title or content using keywords
- **Sort Notes** - Sort by newest first or oldest first
- **Delete Confirmation** - JS popup to prevent accidental deletes
- **Timestamps** - Auto-track created_at for each note
- **User-specific Data** - Each user sees only their own notes

### **Tech Stack**
**Auth:** Flask Sessions, Werkzeug
Python, Flask, Gunicorn, HTML, Jinja2, SQLite, Render

### **How to Run Locally**
1. **Clone the repo**
```bash
git clone https://github.com/Miteshhhhhhh/flask-notes-app.git
cd flask-notes-app
2. Create virtual environment
   python -m venv venv
   venv\Scripts\activate
3. Install Flask
   pip install -r requirements.txt
4. Run the app
   python notes.py
5. Open http://127.0.0.1.5000 in browser

### **Author**
Mitesh Gaikwad
