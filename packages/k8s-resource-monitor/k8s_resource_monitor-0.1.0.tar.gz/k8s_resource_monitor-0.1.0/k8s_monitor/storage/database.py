import sqlite3
from datetime import datetime, timedelta

DB_FILE = "k8s_resource_monitor.db"

def init_db():
    """
    Initialize the SQLite database, creating necessary tables.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create a table for storing pod resource usage
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pod_usage (
        id INTEGER PRIMARY KEY,
        pod_name TEXT,
        namespace TEXT,
        cpu_usage TEXT,
        memory_usage TEXT,
        timestamp TEXT
    )
    ''')

    conn.commit()
    conn.close()

def log_pod_usage(pod_name, namespace, cpu_usage, memory_usage):
    """
    Log pod resource usage into the database with a timestamp.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute('''
    INSERT INTO pod_usage (pod_name, namespace, cpu_usage, memory_usage, timestamp)
    VALUES (?, ?, ?, ?, ?)
    ''', (pod_name, namespace, cpu_usage, memory_usage, timestamp))

    conn.commit()
    conn.close()

def get_average_usage(pod_name, namespace, minutes):
    """
    Get the average CPU and memory usage for a pod over the past 'minutes' time period.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Calculate the time window
    time_threshold = (datetime.now() - timedelta(minutes=minutes)).strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute('''
    SELECT AVG(CAST(cpu_usage AS INTEGER)), AVG(CAST(memory_usage AS INTEGER)) FROM pod_usage
    WHERE pod_name = ? AND namespace = ? AND timestamp >= ?
    ''', (pod_name, namespace, time_threshold))

    result = cursor.fetchone()
    conn.close()

    return result


def get_historical_usage(pod_name, namespace, duration_minutes=60):
    """
    Fetch historical CPU and memory usage for a pod over a specified time period from the database.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Calculate the time window
    time_threshold = (datetime.now() - timedelta(minutes=duration_minutes)).strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute('''
    SELECT CAST(cpu_usage AS INTEGER), CAST(memory_usage AS INTEGER) FROM pod_usage
    WHERE pod_name = ? AND namespace = ? AND timestamp >= ?
    ORDER BY timestamp ASC
    ''', (pod_name, namespace, time_threshold))

    result = cursor.fetchall()
    conn.close()

    # Convert the result to a list of dictionaries
    history = [{'cpu': cpu, 'memory': memory} for cpu, memory in result]
    return history

