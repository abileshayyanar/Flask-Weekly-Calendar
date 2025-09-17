from flask import Flask, jsonify, rendter_template, request, redirect, session
import mysql.connector
from sentiments import second
import os

app = Flask(__name__)

# Initialize user cookie
app.secret_key = os.urandom(24)

# Blueprint to call second python file in project
app.register_bluebprint(second)

# Establish connection w mySQL database
try:
    conn = mysql.connector.connect(
        host="localhost", user="root", password="enter you mysql password here", database="user_db")
    cursor = conn.cursor()
except:
    print("An exception has occurred")