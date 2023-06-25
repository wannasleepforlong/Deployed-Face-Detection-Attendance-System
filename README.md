# Face-Detection-Attendance-System-Deployed
Face attendance system with the functions of login and taking, reading and compiling attendance deployed using streamlit.

This has been made with the use of face-recognition moduke.

Before running this, you have to make a mysql database named attendance and create a table named attendance inside it with columns EventDate(type: datetime), Name(type: varchar) and Attendance(type: varchar). After doing this, change the user and password for mysql connector in the python code corrosponding to your device respectively.

You also have to add images in the folder 'Faces' wtih the name of the person as the name of the jpg file.

After installling the necessary modules, after opening cmd on the destination folder of the main python files, run `streamlit run face_gui.py`
The username is wannasleepforlong and the password is uwu but you can change that however you want.

That's all!


Peace out (°꒳°)
