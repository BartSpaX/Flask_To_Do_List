# 📌 Flask To-Do List 

## 📚 Opis  
Projekt **Flask To-Do List** to aplikacja do zarządzania zadaniami z panelem administratora oraz panelem użytkownika.  
Administrator może zarządzać użytkownikami, dodawać, edytować i usuwać ich konta, a także przypisywać im zadania.  
Użytkownik może dodawać i usuwać zadania oraz oznaczać zadania jako wykonane. Dodatkowo użytkownicy mają dostęp do panelu użytkownika gdzie mogą zmienić swój login.

---

## ⚡ Jak uruchomić projekt?  

### 1️⃣ **Pobranie repozytorium**  
Najpierw sklonuj repozytorium na swój komputer:  
```bash
git clone https://github.com/BartSpaX/Flask_To_Do_List.git
cd Flask_To_Do_List
```

### 2️⃣ **Utworzenie i aktywacja wirtualnego środowiska**  
Dla systemu **Windows (cmd/powershell)**:  
```bash
python -m venv venv
venv\Scripts\activate
```
Dla systemu **Linux/macOS**:  
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ **Instalacja zależności**  
Zainstaluj wszystkie wymagane biblioteki:  
```bash
pip install -r requirements.txt
```

### 4️⃣ **Utworzenie bazy danych**  
Baza danych zostanie utworzona automatycznie przy pierwszym uruchomieniu aplikacji (python app.py).

---

## 🛠 **Dodanie konta administratora**  
Aby dodać konto administratora, uruchom poniższy skrypt w Pythonie:  

```bash
python
```
A następnie wpisz:  
```python
from app import db, User, bcrypt

admin_user = User(
    username="admin",
    password=bcrypt.generate_password_hash("admin123").decode("utf-8"),
    role="admin"
)
db.session.add(admin_user)
db.session.commit()
exit()
```
**Domyślne dane logowania:**  
- **Login:** `admin`  
- **Hasło:** `admin123`  

---

## 🚀 **Uruchomienie aplikacji**  
Aby uruchomić serwer Flask, użyj:  
```bash
python app.py
```
Teraz aplikacja jest dostępna pod adresem:  
👉 **http://127.0.0.1:5000/**  

---

## 🎯 **Funkcjonalności**
👉 **Użytkownicy**  
- Mogą się rejestrować i logować  
- Tworzyć listy To-Do  
- Zarządzać swoimi zadaniami  
- Mogą zmienić swój login

👉 **Administratorzy**  
- Mogą przeglądać listę użytkowników  
- Tworzyć nowych użytkowników  
- Edytować dane użytkowników  
- Usuwać użytkowników  
- Przypisywać zadania  

---

## 📝 **Technologie użyte w projekcie**  
💡 **Flask** - framework backendowy  
💡 **Flask-SQLAlchemy** - ORM do zarządzania bazą danych  
💡 **Flask-Login** - zarządzanie sesjami użytkowników  
💡 **Flask-Bcrypt** - hashowanie haseł  
💡 **Bootstrap** - stylowanie interfejsu  

---

## 📩 **Autor**
👤 **BartSpaX**  
📁 **Repozytorium:** [GitHub - Flask To-Do List](https://github.com/BartSpaX/Flask_To_Do_List)  

🚀 **Dziękuję za korzystanie z projektu! Jeśli masz pomysły na rozwój lub chcesz pomóc, skontaktuj się ze mną! Jeśli projekt Ci się podoba, zostaw ⭐ na GitHubie, aby zwiększyć jego widoczność! 😊**

