# lib/db.py
import sqlite3

# Connect to database (creates file if it doesn't exist)
CONN = sqlite3.connect("company.db")
CURSOR = CONN.cursor()
