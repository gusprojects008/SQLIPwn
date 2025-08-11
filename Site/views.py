from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Good pratice
#from .models import Comment
# from . import models
# comment_model = models()
import sqlite3
import os

# Create your views here.
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "database.db")
#DATABASE_PATH = os.path.join(BASE_DIR, "db.sqlite3")

#print(BASE_DIR, DATABASE_PATH)

def index(request):
    return render(request, "index.html")

@csrf_exempt
def add_comment(request):

    if request.method != "POST":
       return HttpResponse("Bad Method );", status=405)

    username = request.POST.get("username", "").strip()
    comment = request.POST.get("comment", "").strip()

    # intentionally vulnerable to SQLI
    connection_db = sqlite3.connect(DATABASE_PATH)
    cursor = connection_db.cursor()
    cursor.execute("""
      CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        base_username TEXT,
        user_count TEXT UNIQUE,
        user_comment TEXT
      )
    """)
    cursor.execute(f"SELECT COUNT(*) FROM comments WHERE base_username = '{username}'")
    count = cursor.fetchone()[0]
    if count >= 3:
       connection_db.close()
       return HttpResponse("Oops! You've reached the maximum comment limit );")
    username_count = f"{username} quantity:{count + 1}"
    cursor.execute(f"""
      INSERT INTO comments (base_username, user_count, user_comment)
      VALUES ('{username}', '{username_count}', '{comment}')
    """)
    connection_db.commit()
    connection_db.close()
   
    # Good pratice
    '''
    count = Comment.objects.filter(base_username=username).count()

    if count >= 3:
       return HttpResponse("Oops! You've reached the maximum comment limit );")

    username_count = f"{username} quantity:{count + 1}"

    Comment.objects.create(
      base_username=username,
      user_count=username_count,
      user_comment=comment
    )
   '''

    response = {
      "status": "success",
      "message": f"Success! Comment added",
      "username": username,
      "comment": comment
    }
 
    return JsonResponse(response)

def list_comments(request):
    if request.method != "GET":
       return JsonResponse({"status": "error", "message": "Bad method );"})

    # intentionally vulnerable to SQLI   
    db_connection = sqlite3.connect(DATABASE_PATH)
    db_cursor = db_connection.cursor()
    
    db_cursor.execute("SELECT base_username, user_comment FROM comments")
    rows = db_cursor.fetchall()
    comments_response = [{"username": username, "comment": comment} for username, comment in rows]
    db_connection.close()
    return JsonResponse({"status": "success", "message": comments_response})
    
    # Good pratice
    '''
    comments_qs = Comment.objects.values("base_username", "user_comment")
    payload = [{"username": q["base_username"], "comment": q["user_comment"]} for q in comments_qs]
    return JsonResponse({"status": "success", "message": payload})
    '''
