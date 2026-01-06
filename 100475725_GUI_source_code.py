import tkinter as tk
from tkinter import messagebox
import psycopg2

# Database connection details
DB_HOST = "cmpstudb-01.cmp.uea.ac.uk"
DB_NAME = "zks24bbu"
DB_USER = "zks24bbu"
DB_PASSWORD = "DifferentSlowFall45_"

# Database connection
def connect_db():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )



# Function to close the application
def close_app():
    root.destroy()


# Function to add a new student
def add_student():
    sno = sno_entry.get()
    sname = sname_entry.get()
    semail = semail_entry.get()
    
    if not sno or not sname or not semail:
        messagebox.showwarning("All fields are required")
        return
    
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('Set SEARCH_PATH to "Coursework", public;')
        cursor.execute("INSERT into student (sno, sname, semail) VALUES (%s, %s, %s)", (sno, sname, semail))
        conn.commit()
        messagebox.showinfo("Success", "Student added successfully")
    except Exception as e:
        messagebox.showerror("Error", f"An error ocurred: {e}")
        print(e)
    finally:
        if conn:
            conn.close()

# Function to add new exam
def add_exam():
    excode = excode_entry.get()
    extitle = extitle_entry.get()
    exlocation = exlocation_entry.get()
    exdate = exdate_entry.get()
    extime = extime_entry.get()
    
    if not excode or not extitle or not exlocation or not exdate or not extime:
        messagebox.showwarning("All fields are required")
        return
    
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('Set SEARCH_PATH to "Coursework", public;')
        cursor.execute("INSERT into exam (excode, extitle, exlocation, exdate, extime) VALUES (%s, %s, %s, %s, %s)",
                       (excode, extitle, exlocation, exdate, extime))
        conn.commit()
        messagebox.showinfo("Success", "Exam added successfully")
    except Exception as e:
        messagebox.showerror("Error", f"An error occured: {e}")
    finally:
        if conn:
            conn.close()

# Function to add new entry
def add_entry():
    eno = eno_entry.get()
    excode = excode_entry.get()
    sno = sno_entry.get()

    if not eno or not excode or not sno:
        messagebox.showwarning("All fields are required")
        return

    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('Set SEARCH_PATH to "Coursework", public;')
        cursor.execute("INSERT INTO entry (eno, excode, sno) VALUES (%s, %s, %s)",
                       (eno, excode, sno))
        conn.commit()
        messagebox.showinfo("Success", "Entry added successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

# Function to delete student
def delete_student():
    sno = sno_entry.get()
    
    if not sno:
        messagebox.showwarning("Field required")
        return
    
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('Set SEARCH_PATH to "Coursework", public;')
        cursor.execute("DELETE FROM student WHERE sno = %s", (sno,))
        if cursor.rowcount == 0:
            messagebox.showinfo("Message", f"No student found with {sno}")
        else:
            conn.commit()
            messagebox.showinfo("Success", f"Student {sno} deleted")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

# Function to delete examination
def delete_exam():
    excode = excode_entry.get()
    
    if not excode:
        messagebox.showwarning("Field required")
        return
    
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('Set SEARCH_PATH to "Coursework", public;')
        cursor.execute("DELETE FROM exam WHERE excode = %s", (excode,))
        if cursor.rowcount == 0:
            messagebox.showinfo("Message", f"No exam found with {excode}")
        else:
            conn.commit()
            messagebox.showinfo("Success", f"Exam {excode} deleted")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

# Function to update an entry
def update_entry():
    eno = eno_entry.get()
    egrade = egrade_entry.get()

    if not eno or not egrade:
        messagebox.showwarning("All fields are required")
        return

    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('Set SEARCH_PATH to "Coursework", public;')
        cursor.execute("UPDATE entry SET egrade = %s WHERE eno = %s",
                       (egrade, eno))
        conn.commit()
        
        if cursor.rowcount == 0:
            messagebox.showinfo("Message", f"No entry found with {eno}")
        else:
            messagebox.showinfo("Success", "Entry added successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

# Function to view timetables
def view_timetable():
    sno = sno_entry.get()
    
    if not sno:
        messagebox.showwarning("Field required")
        return
    
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('Set SEARCH_PATH to "Coursework", public;')
        cursor.execute("SELECT * FROM timetable WHERE sno = %s", (sno,))
        rows = cursor.fetchall()
        timetable_text.delete(1.0, tk.END)
        
        for row in rows:
            timetable_text.insert(
                tk.END, f"sno: {row[0]}, Name: {row[1]}, Location: {row[2]}, Code: {row[3]}, Title: {row[4]}, Date: {row[5]}, Time: {row[6]}\n")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

# Function to view exam results
def view_all_exam_results():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('Set SEARCH_PATH to "Coursework", public;')
        cursor.execute("SELECT * FROM exam_results")
        rows = cursor.fetchall()
        results_text.delete(1.0, tk.END)
        for row in rows:
            results_text.insert(tk.END, f"Exam Code: {row[0]}, Title: {row[1]}, Name: {row[2]}, Result: {row[3]}\n")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

# Function to view exam results for specific exam
def view_exam_results():
    excode = excode_entry.get()
    
    if not excode:
        messagebox.showwarning("Field required")
        return
    
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('Set SEARCH_PATH to "Coursework", public;')
        cursor.execute("SELECT * FROM exam_results WHERE excode = %s", (excode,))
        rows = cursor.fetchall()
        result_text.delete(1.0, tk.END)
        for row in rows:
            result_text.insert(tk.END, f"Exam Code: {row[0]}, Title: {row[1]}, Name: {row[2]}, Result: {row[3]}\n")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()
            





# GUI Setup
root = tk.Tk()
root.title("Exam Management System")

# Student Input fields
tk.Label(root, text="Student No:").grid(row=0, column=0)
sno_entry = tk.Entry(root)
sno_entry.grid(row=0, column=1)

tk.Label(root, text="Student Name:").grid(row=1, column=0)
sname_entry = tk.Entry(root)
sname_entry.grid(row=1, column=1)

tk.Label(root, text="Email:").grid(row=2, column=0)
semail_entry = tk.Entry(root)
semail_entry.grid(row=2, column=1)


# Exam Input Fields
tk.Label(root, text="Exam Code:").grid(row=3, column=0)
excode_entry = tk.Entry(root)
excode_entry.grid(row=3, column=1)

tk.Label(root, text="Exam Title:").grid(row=4, column=0)
extitle_entry = tk.Entry(root)
extitle_entry.grid(row=4, column=1)

tk.Label(root, text="Exam Location:").grid(row=5, column=0)
exlocation_entry = tk.Entry(root)
exlocation_entry.grid(row=5, column=1)

tk.Label(root, text="Exam Date (YYYY-MM-DD):").grid(row=6, column=0)
exdate_entry = tk.Entry(root)
exdate_entry.grid(row=6, column=1)

tk.Label(root, text="Exam Time (HH:MM:SS):").grid(row=7, column=0)
extime_entry = tk.Entry(root)
extime_entry.grid(row=7, column=1)


# Entry Input Fields
tk.Label(root, text="Entry No:").grid(row=8, column=0)
eno_entry = tk.Entry(root)
eno_entry.grid(row=8, column=1)

tk.Label(root, text="Exam Grade:").grid(row=9, column=0)
egrade_entry = tk.Entry(root)
egrade_entry.grid(row=9, column=1)

# Buttons
tk.Button(root, text="Add Student", command=add_student).grid(row=10, column=0, pady=10)
tk.Button(root, text="Add Exam", command=add_exam).grid(row=10, column=1, pady=10)
tk.Button(root, text="Add Entry", command=add_entry).grid(row=11, column=0, pady=10)
tk.Button(root, text="View Timetable", command=view_timetable).grid(row=11, column=1, pady=10)
tk.Button(root, text="View All Exam Results", command=view_all_exam_results).grid(row=12, column=0, columnspan=1, pady=10)
tk.Button(root, text="View Exam Results", command=view_exam_results).grid(row=13 , column=0 , columnspan=1 , pady=10)
tk.Button(root, text="Delete Student", command=delete_student).grid(row=12, column=1, pady=10)
tk.Button(root, text="Delete Exam", command=delete_exam).grid(row=13, column=1, pady=10)
tk.Button(root, text="Update Entry Grade", command=update_entry).grid(row=16, column=1, pady=10)


# Timetable Display Area
timetable_text = tk.Text(root, height=10, width=50)
timetable_text.grid(row=17, column=0, columnspan=2, padx=10, pady=10)

# Exam Results Display Area
results_text = tk.Text(root, height=10, width=50)
results_text.grid(row=18, column=0, columnspan=2, padx=10, pady=10)

# Singular Exam Results
result_text = tk.Text(root, height=10, width=50)
result_text.grid(row=19, column=0, columnspan=2, padx=10, pady=10)


root.mainloop()