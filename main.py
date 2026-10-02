from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import models
from database import engine, get_db

app = FastAPI()

# Эндпоинт 1: Получение всех заметок
@app.get("/api/notes/", response_model=list[models.NoteResponse])
def get_notes(db: Session = Depends(get_db)):
    return db.query(models.Note).all()

# Эндпоинт 2: Создание новой заметки
@app.post("/api/notes/", response_model=models.NoteResponse)
def create_note(note: models.NoteCreate, db: Session = Depends(get_db)):
    db_note = models.Note(title=note.title, content=note.content)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

# Минимальный фронтенд (HTML+JS)
@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Мои Заметки</title>
    </head>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
        <h2>Добавить заметку</h2>
        <input id="title" placeholder="Заголовок" style="display:block; margin-bottom:5px;">
        <textarea id="content" placeholder="Текст" style="display:block; margin-bottom:5px;"></textarea>
        <button onclick="addNote()">Сохранить</button>
        <h2>Список заметок</h2>
        <ul id="notes-list"></ul>

        <script>
            async function loadNotes() {
                const response = await fetch('/api/notes/');
                const notes = await response.json();
                const list = document.getElementById('notes-list');
                list.innerHTML = '';
                notes.forEach(note => {
                    const li = document.createElement('li');
                    li.innerText = note.title + " — " + note.content;
                    list.appendChild(li);
                });
            }
            
            async function addNote() {
                const title = document.getElementById('title').value;
                const content = document.getElementById('content').value;
                await fetch('/api/notes/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ title, content })
                });
                loadNotes();
            }
            
            loadNotes();
        </script>
    </body>
    </html>
    """