import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox

class HospitalManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System")
        self.root.geometry("1550x820")
        self.create_styles() 
        self.create_database_connection()
        self.create_tabs()
        self.show_doctors()
        
  
        
    def create_styles(self):
        self.style = ttk.Style()
        self.style.configure("TFrame", background="light blue")  # Set background color for frames
        self.style.configure("Large.TButton", font=("Centaur", 30)) 
        #self.style.configure("Doctor.TLabelFrame", font=("Helvetica", 34, "bold"))

    def create_database_connection(self):
        self.conn = sqlite3.connect("NHOSPITAL.sqlite3")
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS patients
            (id INTEGER PRIMARY KEY, name TEXT, gender TEXT, age INTEGER, illness TEXT)''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS doctors
            (id INTEGER PRIMARY KEY, name TEXT, speciality TEXT)''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS appointments
            (id INTEGER PRIMARY KEY, patient_id INTEGER, doctor_id INTEGER, date TEXT)''')
        
        self.conn.commit()

    def create_tabs(self):
        
      # Create a ttk style object to modify the font
      style = ttk.Style()
      style.configure('TNotebook.Tab', font=('Arial', 25))  # Adjust font family and size here

      # Create the tab control
      self.tab_control = ttk.Notebook(root)

      # Create tabs
      self.patient_tab = ttk.Frame(self.tab_control)
      self.doctor_tab = ttk.Frame(self.tab_control)
      self.appointment_tab = ttk.Frame(self.tab_control)

      # Add tabs to the tab control with updated font style
      self.tab_control.add(self.patient_tab, text="Patients")
      self.tab_control.add(self.doctor_tab, text="Doctors")
      self.tab_control.add(self.appointment_tab, text="Appointments")

      # Pack the tab control into the root window
      self.tab_control.pack(expand=1, fill="both")

      # Call methods to populate each tab
      self.create_patient_tab()
      self.create_doctor_tab()
      self.create_appointment_tab()

    def create_patient_tab(self):
        self.patient_frame = ttk.LabelFrame(self.patient_tab, text="Patient Information",)
        self.patient_frame.pack(padx=60, pady=60, fill="both", expand=True)
        
        
        ttk.Label(self.patient_frame, text="Name:",font=('Centaur 30 bold')).grid(row=0, column=0, padx=30, pady=20)
        self.patient_name_entry = ttk.Entry(self.patient_frame,font=("Helvetica", 17))
        self.patient_name_entry.grid(row=0, column=1, padx=10, pady=20)
    
        ttk.Label(self.patient_frame, text="Gender:",font=('Centaur 30 bold')).grid(row=0, column=3, padx=30, pady=20)
        self.patient_gender_combobox = ttk.Combobox(self.patient_frame, values=["Male", "Female"],font=("Helvetica", 17))
        self.patient_gender_combobox.grid(row=0, column=5, padx=30, pady=20)
    
        ttk.Label(self.patient_frame, text="Age:",font=('Centaur 30 bold')).grid(row=2, column=0, padx=30, pady=20)
        self.patient_age_entry = ttk.Entry(self.patient_frame,font=("Helvetica", 17))
        self.patient_age_entry.grid(row=2, column=1, padx=30, pady=20)
    
        ttk.Label(self.patient_frame, text="Illness:",font=('Centaur 30 bold')).grid(row=2, column=3, padx=30, pady=20)
        self.patient_illness_entry = ttk.Entry(self.patient_frame,font=("Helvetica", 17))
        self.patient_illness_entry.grid(row=2, column=5, padx=30, pady=20)
        
        ttk.Button(self.patient_frame, text="Add Patient", width=15, command=self.add_patient, style="Large.TButton").grid(row=5,column=1,pady=30,padx=20)
        ttk.Button(self.patient_frame, text="Show Patients", command=self.show_patients,style="Large.TButton").grid(row=5, column=5, pady=10)
        
        self.patient_listbox = tk.Listbox(self.patient_frame, width=80, height=10,font=("Helvetica",15))
        self.patient_listbox.grid(row=6,column=0,columnspan=10,padx=60, pady=60)


    def create_doctor_tab(self):
        self.doctor_frame = ttk.LabelFrame(self.doctor_tab, text="Doctor Information")
        self.doctor_frame.pack(padx=60, pady=60, fill="both", expand=True)
        
    
        ttk.Label(self.doctor_frame, text="Name:",font=('Centaur 30 bold')).grid(row=0, column=0, padx=30, pady=20)
        self.doctor_name_entry = ttk.Entry(self.doctor_frame,font=("Helvetica", 17))
        self.doctor_name_entry.grid(row=0, column=1, padx=30, pady=20)
    
        ttk.Label(self.doctor_frame, text="Speciality:",font=('Centaur 30 bold')).grid(row=0, column=6, padx=30, pady=20)
        self.doctor_speciality_entry = ttk.Entry(self.doctor_frame,font=("Helvetica", 17))
        self.doctor_speciality_entry.grid(row=0, column=7, padx=30, pady=20)
        
        ttk.Button(self.doctor_frame, text="Add Doctor", command=self.add_doctor,style="Large.TButton").grid(row=2,column=1, pady=10)
        ttk.Button(self.doctor_frame, text="Show Doctor", command=self.show_doctors,style="Large.TButton").grid(row=2, column=7, pady=10)
        
        self.doctor_listbox = tk.Listbox(self.doctor_frame, width=80, height=40,font=("Helvetica",15))
        self.doctor_listbox.grid(row=6,column=0,columnspan=10,padx=60, pady=60)

    def create_appointment_tab(self):
        self.appointment_frame = ttk.LabelFrame(self.appointment_tab, text="Appointment Information")
        self.appointment_frame.pack(padx=60, pady=60, fill="both", expand=True)
    
        ttk.Label(self.appointment_frame, text="Patient ID:",font=('Centaur 30 bold')).grid(row=0, column=0, padx=30, pady=20)
        self.appointment_patient_id_entry = ttk.Entry(self.appointment_frame,font=("Helvetica", 17))
        self.appointment_patient_id_entry.grid(row=0, column=1, padx=30, pady=20)
    
        ttk.Label(self.appointment_frame, text="Doctor ID:",font=('Centaur 30 bold')).grid(row=0, column=3, padx=30, pady=20)
        self.appointment_doctor_id_entry = ttk.Entry(self.appointment_frame,font=("Helvetica", 17))
        self.appointment_doctor_id_entry.grid(row=0, column=4, padx=30, pady=20)
    
        ttk.Label(self.appointment_frame, text="Appointment Date:",font=('Centaur 30 bold')).grid(row=1, column=0, padx=30, pady=20)
        self.appointment_date_entry = ttk.Entry(self.appointment_frame,font=("Helvetica", 17))
        self.appointment_date_entry.grid(row=1, column=1, padx=30, pady=20)
    
        self.appointment_listbox = tk.Listbox(self.appointment_frame, width=80, height=40,font=("Helvetica",15))
        self.appointment_listbox.grid(row=6,column=0,columnspan=10,padx=60, pady=60)

        ttk.Button(self.appointment_frame, text="Create Appointment", command=self.create_appointment,style="Large.TButton").grid(row=3, column=1, pady=10)
        ttk.Button(self.appointment_frame, text="Show Appointment", command=self.show_appointments,style="Large.TButton").grid(row=3, column=4, pady=10)
  
    

    def add_patient(self):
        name = self.patient_name_entry.get()
        gender = self.patient_gender_combobox.get()
        age = int(self.patient_age_entry.get())
        illness = self.patient_illness_entry.get()
    
        self.c.execute("INSERT INTO patients (name, gender, age, illness) VALUES (?, ?, ?, ?)", (name, gender, age, illness))
        self.conn.commit()
    
        messagebox.showinfo("Success", "Patient added successfully")
    
        # Clear entry fields after adding
        self.patient_name_entry.delete(0, tk.END)
        self.patient_gender_combobox.set("")
        self.patient_age_entry.delete(0, tk.END)
        self.patient_illness_entry.delete(0, tk.END)
        
    def show_patients(self):
            self.patient_listbox.delete(0, tk.END)
        
            self.c.execute("SELECT * FROM patients")
            patients = self.c.fetchall()
        
            for patient in patients:
                self.patient_listbox.insert(tk.END, f"ID: {patient[0]}, Name: {patient[1]}, Age: {patient[3]}, Illness: {patient[4]}")
    

    def add_doctor(self):
        name = self.doctor_name_entry.get()
        speciality = self.doctor_speciality_entry.get()
        self.c.execute("INSERT INTO doctors (name, speciality) VALUES (?, ?)", (name, speciality))
        self.conn.commit()
    
        messagebox.showinfo("Success", "Doctor added successfully")
    
        # Clear entry fields after adding
        self.doctor_name_entry.delete(0, tk.END)
        self.doctor_speciality_entry.delete(0, tk.END)

    def show_doctors(self):
        self.doctor_listbox.delete(0, tk.END)
    
        self.c.execute("SELECT * FROM doctors")
        doctors = self.c.fetchall()
    
        for doctor in doctors:
            self.doctor_listbox.insert(tk.END, f"ID: {doctor[0]}, Name: {doctor[1]}, Speciality: {doctor[2]}")

   

    def create_appointment(self):
        patient_id = int(self.appointment_patient_id_entry.get())
        doctor_id = int(self.appointment_doctor_id_entry.get())
        appointment_date = self.appointment_date_entry.get()
    
        self.c.execute("INSERT INTO appointments (patient_id, doctor_id, date) VALUES (?, ?, ?)", (patient_id, doctor_id, appointment_date))
        self.conn.commit()
    
        messagebox.showinfo("Success", "Appointment created successfully")
    
        # Clear entry fields after creating appointment
        self.appointment_patient_id_entry.delete(0, tk.END)
        self.appointment_doctor_id_entry.delete(0, tk.END)
        self.appointment_date_entry.delete(0, tk.END)

    def show_appointments(self):
         self.appointment_listbox.delete(0, tk.END)
     
         self.c.execute("SELECT appointments.id, patients.name, doctors.name, appointments.date FROM appointments "
                        "INNER JOIN patients ON appointments.patient_id = patients.id "
                        "INNER JOIN doctors ON appointments.doctor_id = doctors.id "
                        "ORDER BY appointments.date DESC")
         appointments = self.c.fetchall()
     
         for appointment in appointments:
             self.appointment_listbox.insert(tk.END, f"ID: {appointment[0]}, Patient: {appointment[1]}, Doctor: {appointment[2]}, Date: {appointment[3]}")

   
        
    

if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalManagementApp(root)

    root.mainloop()
