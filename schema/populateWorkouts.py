import sqlite3

print("Starting script...")

# Connect to SQLite database
conn = sqlite3.connect('all_the_exercise.db')
cursor = conn.cursor()
print("Connected sucesssfully...")

# Enable foreign keys support
cursor.execute("PRAGMA foreign_keys = ON;")
print("Executed something...")

# Create tables
cursor.executescript('''
CREATE TABLE IF NOT EXISTS exercise_library (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS programs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    library_id INTEGER,
    name TEXT UNIQUE,
    FOREIGN KEY (library_id) REFERENCES exercise_library(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS weeks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    program_id INTEGER,
    week_number INTEGER,
    FOREIGN KEY (program_id) REFERENCES programs(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS days (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    week_id INTEGER,
    name TEXT,
    FOREIGN KEY (week_id) REFERENCES weeks(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS exercises (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    day_id INTEGER,
    name TEXT,
    reps TEXT,
    rpe TEXT,
    rest TEXT,
    load TEXT,
    warmUpSets TEXT,
    workingSets TEXT,
    notes TEXT,
    FOREIGN KEY (day_id) REFERENCES days(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS substitutions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    exercise_id INTEGER,
    substitution_name TEXT,
    FOREIGN KEY (exercise_id) REFERENCES exercises(id) ON DELETE CASCADE
);
''')

# Commit and close
conn.commit()
conn.close()

print("Database schema created successfully!")
