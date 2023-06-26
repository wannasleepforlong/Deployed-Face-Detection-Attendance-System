import streamlit as st
import mysql.connector
import subprocess
import base64


userlist = [['wannasleepforlong','uwu'],['admin','123']]

class FaceDetectionApp:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="sh221b777",
            password="12345",
            database="attendance"
        )
        self.cursor = self.conn.cursor()

    def run_face_detection(self):
        subprocess.run(["python", "Face_Detection.py"])

    def home(self):
        st.markdown("<h1 style='text-align: center; color: blue; font-size: 50px;'>Face Detection Attendance System</h1>", unsafe_allow_html=True)
        st.write("**Welcome to the Face Detection Attendance System!**")
        st.write("")
        st.write("This is “Face Detection Attendance System” project made with the use of python and sql for the real-time detection of faces of people and marking their attendance.")
        st.write(" ")
        st.write("Peace out!")
        st.write("-wannasleepforlong")
        gif_path = r"C:\Users\HP\Desktop\Programming\Python\Face Detection Attendance\kawaii.gif"  
        st.markdown(f'<img src="data:image/gif;base64,{base64.b64encode(open(gif_path, "rb").read()).decode()}" alt="gif">', unsafe_allow_html=True)
        

    def take_attendance(self):
        st.title(":orange[Take Attendance]")
        st.write("Click the button below to take attendance.")
        if st.button("Take Attendance"):
            self.run_face_detection()

    def show_attendance(self):
        st.title(":green[Total Attendance]")
        st.write("Click the button below to show attendance.")
        if st.button('Show Attendance'):
            select_query = "SELECT * FROM attendance"
            self.cursor.execute(select_query)
            rows = self.cursor.fetchall()
            if len(rows) > 0:
                st.table(rows)
            else:
                st.write("No attendance records found.")

    def compiled_attendance(self):
        st.title(":violet[Compiled Attendance]")
        st.write("Click the button below to show compiled attendance.")
        if st.button('Show Compiled Attendance'):
            conn = mysql.connector.connect(
                host="localhost",
                user="sh221b777",
                password="12345",
                database="attendance"
            )

            cursor = conn.cursor()

            select_query = "SELECT Name, COUNT(*) AS AttendanceCount FROM attendance GROUP BY Name"
            cursor.execute(select_query)

            rows = cursor.fetchall()

            if len(rows) > 0:
                st.table(rows)
            else:
                st.write("No attendance records found.")


    def attendance_record(self):
        st.title(":pink[Daily Attendance Record]")
        st.write("Enter the date to show attendance.")
        selected_date = st.date_input("Date")
        if st.button("Show Attendance"):
            select_query = f"SELECT * FROM attendance WHERE EventDate = '{selected_date}'"
            self.cursor.execute(select_query)
            rows = self.cursor.fetchall()
            if len(rows) > 0:
                st.table(rows)
            else:
                st.write("No attendance records found for the selected date.")
        
    def login(self):
        st.sidebar.title("Login")
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        
        for i in range(len(userlist)):
             if  username==userlist[i][0] and password==userlist[i][1]:
                       return True
        else:
            return False

    def run(self):
        if self.login():
            st.sidebar.title("Menu")
            menu_selection = st.sidebar.selectbox("Select an option", ("Home📚", "Take Attendance📷", "Show Attendance🧿", "Show Compiled Attendance📝","Daily Attendance Record📅"))

            if menu_selection == "Home📚":
                self.home()
            elif menu_selection == "Take Attendance📷":
                self.take_attendance()
            elif menu_selection == "Show Attendance🧿":
                self.show_attendance()
            elif menu_selection == "Show Compiled Attendance📝":
                self.compiled_attendance()
            elif menu_selection == "Daily Attendance Record📅":
                self.attendance_record()
    
        else:
            st.title("Unauthorized Access")
            st.write("Please login as an administrator or student to access the Face Detection Attendance System.")
            st.image('lock.jpg')



if __name__ == "__main__":
    app = FaceDetectionApp()
    app.run()
    app.cursor.close()
    app.conn.close()
