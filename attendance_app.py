from flask import Flask, render_template
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def display_attendance():
    # Get the current date
    date = datetime.now().strftime("%d-%m-%Y")
    
    # Define the file path for today's attendance
    file_path = f"Attendance/Attendance_{date}.csv"
    
    if not os.path.exists(file_path):
        return f"<h1>Attendance file for {date} not found.</h1>"
    
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Check if 'PHOTO' column exists
    if 'PHOTO' not in df.columns:
        return f"<h1>Photo column not found in the attendance file.</h1>"
    
    # Check if 'ROLL NO' column exists
    if 'ROLL NO' not in df.columns:
        return f"<h1>Roll No column not found in the attendance file.</h1>"
    
    # Add a column for full photo paths and rename it to 'STUDENT_PHOTO'
    df['STUDENT_PHOTO'] = df['PHOTO'].apply(lambda x: f"/static/photos/{x}")
    
    # Convert the DataFrame to HTML with image tags
    table_html = df.to_html(
        index=False,
        escape=False,
        classes='table table-striped',
        formatters={
            'STUDENT_PHOTO': lambda x: f'<img src="{x}" alt="Photo" style="height:100px;">'
        },
        columns=['ROLL NO', 'NAME', 'TIME', 'STUDENT_PHOTO']  # Include 'ROLL NO' in the displayed columns
    )
    
    # Render the table in an HTML page
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Attendance for {date}</title>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    </head>
    <body>
        <div class="container">
            <h1 class="my-4">Attendance for {date}</h1>
            {table_html}
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True)
