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
-- Create users table (if not exists)
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id TEXT UNIQUE
);

-- Track user progress on programs
CREATE TABLE IF NOT EXISTS program_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    program_id INTEGER,
    completed BOOLEAN DEFAULT 0,
    UNIQUE(user_id, program_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (program_id) REFERENCES programs(id) ON DELETE CASCADE
);

-- Track user progress on weeks
CREATE TABLE IF NOT EXISTS week_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    week_id INTEGER,
    completed BOOLEAN DEFAULT 0,
    UNIQUE(user_id, week_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (week_id) REFERENCES weeks(id) ON DELETE CASCADE
);

-- Track user progress on days
CREATE TABLE IF NOT EXISTS day_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    day_id INTEGER,
    completed BOOLEAN DEFAULT 0,
    UNIQUE(user_id, day_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (day_id) REFERENCES days(id) ON DELETE CASCADE
);

-- Track user progress on exercises
CREATE TABLE IF NOT EXISTS exercise_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    exercise_id INTEGER,
    date TEXT DEFAULT (DATE('now')),
    completed BOOLEAN DEFAULT 0,
    weight_used TEXT,
    UNIQUE(user_id, exercise_id, date),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (exercise_id) REFERENCES exercises(id) ON DELETE CASCADE
);

''')

# Commit and close
conn.commit()
conn.close()

print("Database schema created successfully!")
