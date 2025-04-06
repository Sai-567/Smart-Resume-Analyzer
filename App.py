import os
import re
import io
import PyPDF2
from sklearn.metrics import r2_score # type: ignore
with st.spinner("Loading models..."):
    # heavy setup
    import spacy
    from spacy.cli import download
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        download("en_core_web_sm")
        nlp = spacy.load("en_core_web_sm")
import streamlit as st
st.set_page_config(page_title="Smart Resume Analyzer")
st.title("✅ App is loading... Please wait.")
import pytesseract # type: ignore
from pdf2image import convert_from_path # type: ignore
import email
import base64
from os import name
from sqlite3.dbapi2 import Timestamp
from sqlalchemy import label, values   # type: ignore
import pandas as pd   # type: ignore
import base64,random
import time,datetime
from pyresparser import ResumeParser   # type: ignore
from streamlit import connection   # type: ignore
import Courses
from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams, LTTextBox   # type: ignore
from pdfminer.pdfpage import PDFPage  # type: ignore
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter  # type: ignore
from pdfminer.converter import TextConverter  # type: ignore
import io,random
from streamlit_tags import st_tags   # type: ignore

st.title("Streamlit Tags Example")

tags = st_tags(
    label='Enter Tags:',
    text='Press enter to add more',
    value=['Python', 'Streamlit'],
    suggestions=['Django', 'Flask', 'FastAPI'],
    maxtags=5
)

st.write("Selected Tags:", tags)
from PIL import Image # type: ignore
import pymysql  # type: ignore
from Courses import ds_course, web_course, android_course, ios_course, uiux_course, resume_videos, interview_videos
os.environ["PAFY_BACKEND"] = "internal"  # Use pafy's internal backend instead of youtube-dl
import pafy # type: ignore
import plotly.express as px # type: ignore
import yt_dlp as youtube_dl # type: ignore

def fetch_yt_video(link):
    if not link:  
        print("⚠️ Error: No YouTube link provided")
        return "No Video Available"

    try:
        video = pafy.new(link)
        return video.title
    except Exception as e:
        print(f"⚠️ Error fetching video: {e}")  # ✅ Debugging
        return "No Video Available"

def get_table_download_link(df, filename, text):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode() 
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href

def pdf_reader(file_path):
    """Reads a PDF file and extracts text."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    text = extract_text(file_path)
    if not text.strip():  # If no text extracted, try OCR
        print(" Using OCR as PyPDF2 failed.")
        images = convert_from_path(file_path)
        text = ""
        for img in images:
            text += pytesseract.image_to_string(img)
    return text

def show_pdf(pdf_path):
    """Displays the PDF in Streamlit without decoding as UTF-8."""
    with open(pdf_path, "rb") as f:  
        base64_pdf = base64.b64encode(f.read()).decode('utf-8') 
    
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def course_recommender(course_list):
    st.subheader("**Courses & Certificates Recommendations**")
    c=0
    rec_course = [] 
    no_of_reco = st.slider('Choose Number of Course Recommendations:', 1, 10, 4)   
    random.shuffle(course_list)
    for c_name, c_link in course_list:
        c += 1
        st.markdown(f"({c}) [{c_name}]({c_link})")
        rec_course.append(c_name)
        if c==no_of_reco:
            break
    return rec_course

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='NewPassword123',  # Replace with your actual password
    database='sra'
)

print("Connected successfully!")        

cursor = connection.cursor()


def insert_data(name, email, res_score, timestamp, no_of_pages, reco_field, cand_level, skills, recommended_skills, courses):
    DB_table_name = 'user_data'
    
    insert_sql = f"""INSERT INTO {DB_table_name} 
    (Name, Email_ID, resume_score, Timestamp, Page_no, Predicted_Field, User_level, Actual_skills, Recommended_skills, Recommended_courses)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""  # ✅ 10 placeholders

    rec_values = (name, email, res_score, timestamp, no_of_pages, reco_field, cand_level, skills, recommended_skills, courses)

    # 🔹 Debugging: Print the query and values before executing
    print("SQL Query:", insert_sql)
    print("Values Length:", len(rec_values))  # ✅ Check number of values
    print("Values:", rec_values)

    cursor.execute(insert_sql, rec_values)
    connection.commit()

    

def run():
    st.title("Smart Resume Analyzer")
    st.sidebar.markdown("# Choose User")
    activities = ["Normal User", "Admin"]
    choice = st.sidebar.selectbox("Choose among the givem options:", activities)
    img = Image.open('./Logo/SRA_Logo.ico')
    img = img.resize((250, 250))
    st.image(img)
    
    db_sql = """CREATE DATABASE IF NOT EXISTS SRA;"""
    cursor.execute(db_sql)
    connection.select_db("sra")
    
    DB_table_name = "user_data"
    insert_sql = """INSERT INTO user_data 
                    (name, email, res_score, timestamp, no_of_pages, reco_field, card_level, skills, recommended_skills, courses) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

    rec_values = (name, email, str(r2_score), Timestamp, no_of_pages, reco_field, card_level, skills, recommended_skills, courses) # type: ignore
    cursor.execute(insert_sql, rec_values)
    connection.commit()
    
def run():

    st.title("Smart Resume Analyzer")
    st.sidebar.markdown("# Choose User")
    activities = ["Normal User", "Admin"]
    choice = st.sidebar.selectbox("Choose among the givem options:", activities)
    img = Image.open('./Logo/SRA_Logo.ico')
    img = img.resize((250, 250))
    st.image(img)
    
    db_sql = """CREATE DATABASE IF NOT EXISTS SRA;"""
    cursor.execute(db_sql)
    connection.select_db("sra")
    
    DB_table_name = 'user_data'
    table_sql = "CREATE TABLE IF NOT EXISTS " + DB_table_name + """
                    (ID INT NOT NULL AUTO_INCREMENT,
                     Name varchar(100) NOT NULL,
                     Email_ID VARCHAR(50) NOT NULL,
                     resume_score VARCHAR(8) NOT NULL,
                     Timestamp VARCHAR(50) NOT NULL,
                     Page_no VARCHAR(5) NOT NULL,
                     Predicted_Field VARCHAR(25) NOT NULL,
                     User_level VARCHAR(30) NOT NULL,
                     Actual_skills VARCHAR(300) NOT NULL,
                     Recommended_skills VARCHAR(300) NOT NULL,
                     Recommended_courses VARCHAR(600) NOT NULL,
                     PRIMARY KEY (ID));
                    """
    cursor.execute(table_sql)
    upload_folder = './Uploaded_Resumes/'   
    os.makedirs(upload_folder, exist_ok=True)
    if choice == 'Normal User':
        pdf_file = st.file_uploader("Choose your Resume", type=["pdf"])

        resume_text = ""
        resume_data = None
        if pdf_file is not None:
            save_image_path = os.path.join(upload_folder, pdf_file.name) 
            with open(save_image_path, "wb") as f:
                f.write(pdf_file.getbuffer())
    
            show_pdf(save_image_path)
            try:
                resume_data = ResumeParser(save_image_path).get_extracted_data()
                print("Debug: Extracted resume_data=", resume_data)  
            except Exception as e:
                print("Error parsing resume:", e)  
                resume_data = None

            
            resume_data = ResumeParser(save_image_path).get_extracted_data()
            print("Debug: Extracted resume_data =", resume_data)  # ✅ Check extracted data

            if resume_data is None:                
                print("❌ Error: resume_data is None. Resume parsing failed.")  
            elif not isinstance(resume_data, dict):                
                print("❌ Error: resume_data is not a dictionary. Received:", type(resume_data))
            elif 'skills' not in resume_data:                  
                print("❌ Error: 'skills' key is missing in resume_data.")  
            elif resume_data['skills'] is None or len(resume_data['skills']) == 0:
                print("❌ Error: 'skills' list is empty.")  
            else:
                print("✅ Successfully extracted skills!")
                for i in resume_data['skills']:
                    print("Skill:", i)  # ✅ Print extracted skills


            print("Resume Data:", resume_data) # type: ignore

            if resume_data: # type: ignore
                resume_text = pdf_reader(save_image_path)
                if not resume_text.strip():
                    print("❌ Warning: No text extracted from resume.")  # Debugging
                else:
                    print("✅ Extracted Resume Text:\n", resume_text[:500])  # Print first 500 characters

                st.header("**Resume Analysis**")
                st.success(f"Hello {resume_data.get('name', 'User')}")  # type: ignore
                st.subheader("**Your Basic info**")
                try:
                    st.text('Name: ' + resume_data['name']) # type: ignore
                    st.text('Email: ' + resume_data['email']) # type: ignore
                    st.text('Contact: ' + resume_data['mobile_number']) # type: ignore
                    st.text('Resume pages: ' + str(resume_data['no_of_pages'])) # type: ignore
                except:
                    pass
                cand_level = ''
                if resume_data['no_of_pages'] == 1: # type: ignore
                    cand_level = "Fresher"
                    st.markdown('''<h4 style='text-align: left; color: #d73b5c;'>You are looking Fresher.</h4>''',
                                unsafe_allow_html=True)
                elif resume_data['no_of_pages'] == 2: # type: ignore
                    cand_level = "Intermediate"
                    st.markdown('''<h4 style='text-align: left; color: #1ed760;'>You are at intermediate level!</h4>''',
                                unsafe_allow_html=True)
                elif resume_data['no_of_pages'] >= 3: # type: ignore
                    cand_level = "Experienced"
                    st.markdown('''<h4 style='text-align: left; color: #fba171;'>You are at experience level!''',
                                unsafe_allow_html=True)
                st.subheader("**Skills Recommendation**")
                
                keywords = st_tags(label='### Skills that you have',
                                   text='See our skills recommendation',
                                   value=resume_data['skills'], key='1') # type: ignore
                ds_keyword = ['tensorflow', 'keras', 'pytorch', 'machine learning', 'deep Learning', 'flask', 'streamlit']
                web_keyword = ['react', 'django', 'node jS', 'react js', 'php', 'laravel', 'magento', 'wordpress', 'javascript', 'angular js', 'c#', 'flask']
                android_keyword = ['android', 'android development', 'flutter', 'kotlin', 'xml', 'kivy']
                ios_keyword = ['ios', 'ios development', 'swift', 'cocoa', 'cocoa touch', 'xcode']
                uiux_keyword = ['ux', 'adobe xd', 'figma', 'zeplin', 'balsamiq', 'ui', 'prototyping', 'wireframes',
                                'storyframes', 'adobe photoshop', 'photoshop', 'editing', 'adobe illustrator',
                                'illustrator', 'adobe after effects', 'after effects', 'adobe premier pro',
                                'premier pro', 'adobe indesign', 'indesign', 'wireframe', 'solid', 'grasp',
                                'user research', 'user experience']
                
                recommended_skills = []
                reco_field = ''
                rec_course = ''
                found_category = False  

        resume_score = 0  
        resume_text_lower = resume_text.lower()
        found_category = False  
        
        cur_data = datetime.datetime.now().strftime('%Y-%m-%d')  
        cur_time = datetime.datetime.now().strftime('%H:%M:%S')  
        Timestamp = str(cur_data + '_' + cur_time) 
        if resume_data is None:
            print("Error: resume_data is None.")  # ✅ Debugging
        elif 'skills' not in resume_data:
            print("Error: 'skills' key is missing in resume_data.")  # ✅ Debugging
        elif not resume_data['skills']:
            print("Error: 'skills' list is empty.")  # ✅ Debugging
        else:
            for i in resume_data['skills']: 
                if not found_category:  
                    if i.lower() in ds_keyword:
                        print(i.lower())
                        reco_field = 'Data Science'
                        st.success("** Our analysis says you are looking for Data Science Jobs.**")
                        recommended_skills = ['Data Visualization', 'Predictive Analysis', 'Statistical Modeling',
                                            'Data Mining', 'Clustering & Classification', 'Data Analytics',
                                            'Quantitative Analysis', 'Web Scraping', 'ML Algorithms', 'Keras',
                                            'Pytorch', 'Probability', 'Scikit-learn', 'Tensorflow', "Flask",
                                            'Streamlit']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                                                    text='Recommended skills generated from System',
                                                    value=recommended_skills, key='2')
                        st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding these skills to your resume will boost your chances of getting a Job</h4>''', unsafe_allow_html=True)
                        rec_course = course_recommender(ds_course)
                        found_category = True  
  

                elif i.lower() in web_keyword:
                    print(i.lower())
                    reco_field = 'Web Development'
                    st.success("**Our analysis says you are looking for Web Development Jobs.**")
                    recommended_skills = ['React', 'Django', 'Node JS', 'React JS', 'php', 'laravel', 'Magento', 'wordpress', 'Javascript', 'Angular JS', 'c#', 'Flask', 'SDK']
                    recommended_keywords = st_tags(label='### Recommended skills for you.',
                                                text='Recommended skills generated from System',
                                                value=recommended_skills, key='3')
                    st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost the chances of getting a Job</h4>''', unsafe_allow_html=True)
                    rec_course = course_recommender(android_course)
                    found_category = True  
        
                elif i.lower() in ios_keyword:
                    print(i.lower())
                    reco_field = 'IOS App Development'
                    st.success("**Our analysis says you are looking for IOS App Development Jobs.**")
                    recommended_skills = ['IOS', 'IOS Development', 'Swift', 'Cocoa', 'Cocoa Touch', 'Xcode',
                                        'Objective-C', 'SQLite', 'Plist', 'StoreKit', "UI-Kit", 'AV Foundation',
                                        'Auto-Layout']
                    recommended_keywords = st_tags(label='### Recommended skills for you.',
                                                text='Recommended skills generated from System',
                                                value=recommended_skills, key='5')
                    st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost the chances of getting a Job</h4>''', unsafe_allow_html=True)
                    rec_course = course_recommender(ios_course)
                    found_category = True  

                elif i.lower() in uiux_keyword:
                    print(i.lower())
                    reco_field = 'UI-UX Development'
                    st.success("**Our analysis says you are looking for UI-UX Development Jobs.**")
                    recommended_skills = ['UI', 'User Experience', 'Adobe XD', 'Figma', 'Zeplin', 'Balsamiq',
                                        'Prototyping', 'Wireframes', 'Storyframes', 'Adobe Photoshop', 'Editing',
                                        'Illustrator', 'After Effects', 'Premier Pro', 'Indesign', 'Wireframe',
                                        'Solid', 'Grasp', 'User Research']
                    recommended_keywords = st_tags(label='### Recommended skills for you.',
                                                text='Recommended skills generated from System',
                                                value=recommended_skills, key='6')
                    st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost the chances of getting a Job</h4>''', unsafe_allow_html=True)
                    rec_course = course_recommender(uiux_course)
                    found_category = True  

                    ts = time.time()
                    resume_score = 0  # ✅ Initialize Before Use

                    cur_data = datetime.datetime.now().strftime('%Y-%m-%d')  
                    cur_time = datetime.datetime.now().strftime('%H:%M:%S')  
                    Timestamp = str(cur_data + '_' + cur_time)  # ✅ Define Before Usage

                    print("🔹 Debug: Entering Resume Tips Section")  # ✅ Ensure Code Reaches Here

                    st.subheader("**Resume Tips & Ideas**")
                resume_text = ""

                with open(save_image_path, "rb") as f:
                    reader = PyPDF2.PdfReader(f)
                    for page in reader.pages:
                        page_text = page.extract_text()
                        if page_text:
                            resume_text += page_text + "\n"

                if not resume_text.strip():  
                    print("Using OCR as PyPDF2 extraction failed.")
                    images = convert_from_path(save_image_path)
                    resume_text = ""
                    for img in images:
                        resume_text += pytesseract.image_to_string(img)
                print("Extracted Resume Text:\n", resume_text)
                score_weights = {
                    "objective": 20,     
                    "declaration": 15,    
                    "hobbies": 10,       
                    "achievements": 25,   
                    "projects": 30        
                }

                resume_score = 0

                resume_text_lower = resume_text.lower()

                if any(keyword in resume_text_lower for keyword in ['objective', 'summary', 'career goal']):
                    resume_score += score_weights["objective"]
                    st.markdown('''<h4 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Objective or Summary</h4>''', unsafe_allow_html=True)
                else:
                    st.markdown('''<h4 style='text-align: left; color: #fabc10;'>[-] Please add a career objective or summary.</h4>''', unsafe_allow_html=True)

                if 'declaration' in resume_text_lower:
                    resume_score += score_weights["declaration"]
                    st.markdown('''<h4 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added a Declaration</h4>''', unsafe_allow_html=True)
                else:
                    st.markdown('''<h4 style='text-align: left; color: #fabc10;'>[-] Please add a Declaration to assure the recruiter that your information is true.</h4>''', unsafe_allow_html=True)

                if 'hobbies' in resume_text_lower or 'interests' in resume_text_lower:
                    resume_score += score_weights["hobbies"]
                    st.markdown('''<h4 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Hobbies</h4>''', unsafe_allow_html=True)
                else:
                    st.markdown('''<h4 style='text-align: left; color: #fabc10;'>[-] Consider adding your hobbies or interests.</h4>''', unsafe_allow_html=True)

                if 'achievements' in resume_text_lower:
                    resume_score += score_weights["achievements"]
                    st.markdown('''<h4 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Achievements</h4>''', unsafe_allow_html=True)
                else:
                    st.markdown('''<h4 style='text-align: left; color: #fabc10;'>[-] Please add Achievements to showcase your capabilities.</h4>''', unsafe_allow_html=True)

                if 'projects' in resume_text_lower:
                    resume_score += score_weights["projects"]
                    st.markdown('''<h4 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Projects</h4>''', unsafe_allow_html=True)
                else:
                    st.markdown('''<h4 style='text-align: left; color: #fabc10;'>[-] Please add Projects to demonstrate your work experience.</h4>''', unsafe_allow_html=True)

# Normalize the score out of 100
                max_score = sum(score_weights.values())  # Total possible score
                final_score = (resume_score / max_score) * 100  # Normalize to 100

# Display final score
                st.success(f'**Your Resume Writing Score: {round(final_score, 2)} / 100**')
                st.warning("**Note: This score is calculated based on the content that you have added in your Resume.**")
                st.balloons()

                print(f"Final Resume Score: {resume_score}")

                my_bar = st.progress(0)
                for percent_complete in range(int(resume_score)):  # Convert to integer

                    time.sleep(0.05)  # Reduce sleep time for faster update
                    my_bar.progress(percent_complete + 1)

                st.success(f'**Your Resume Writing Score: {resume_score}**')
                st.warning("**Note: This score is calculated based on the content that you have added in your Resume.**")
                st.balloons()
                
                print(f"Debug: Final Resume Score = {resume_score}")

                if resume_data: # type: ignore
                    name = resume_data.get('name') # type: ignore

                    if not name or name.strip() == "":
                        name = "Unknown"  
    
                    email = resume_data.get('email', 'Unknown') # type: ignore
                    
                    if resume_score is not None:
                        st.success(f'**Your Resume Writing Score: {resume_score}**')
                    else:
                        st.warning("⚠️ Resume score could not be calculated. Please check your resume content.")

                    timestamp = Timestamp if 'Timestamp' in locals() else datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

                    no_of_pages = str(resume_data.get('no_of_pages', 1))   # type: ignore
                    reco_field = reco_field if reco_field else 'Unknown'
                    cand_level = cand_level if cand_level else 'Unknown'
                    skills = str(resume_data.get('skills', []))   # type: ignore
                    recommended_skills = str(recommended_skills if recommended_skills else [])
                    rec_course = str(rec_course if rec_course else [])
                    print("Final Insert Values:", (name, email, resume_score, timestamp, no_of_pages, reco_field, cand_level, skills, recommended_skills, rec_course))
                    insert_data(name, email, resume_score, timestamp, no_of_pages, reco_field, cand_level, skills, recommended_skills, rec_course)

                    st.header("**Bonus Video Recommendations (Max 3)**")

                    num_videos = random.randint(2, 3)  
                    selected_videos = random.sample(resume_videos + interview_videos, num_videos)  

                    for idx, video_url in enumerate(selected_videos, start=1):
                        print(f"🔹 Debug: Selected Video {idx}: {video_url}")  # Debugging
                        video_title = fetch_yt_video(video_url)
                        st.subheader(f"✅ **Video {idx}: {video_title}**")
                        st.video(video_url)

                    print("✅ Video recommendation loop has completed.")  
                    st.success("✅ **Video recommendations have ended. Now displaying final score.**")

                    st.success(f'**Your Resume Writing Score: {resume_score}**')
                    st.warning("**Note: This score is calculated based on the content that you have added in your Resume.**")
                    st.balloons()


                    
                    connection.commit()
                else:
                    st.error('Something went wrong...')
            
            #else:
            #     st.success('Welcome to Admin Side')
                
                
            #     ad_user = st.text_input("Username")
            #     ad_password = st.text_input("Password", type='password')
            #     if st.button('Login'):
            #         if ad_user == 'machine_learning_hub' and ad_password == 'milhub123':
            #             st.success('Welcome Kushal')
            #             #Display Data
            #             cursor.execute('''SELECT*FROM user_data''')
            #             data = cursor.fetchall()
            #             st.header("**User's Data**")
            #             df = pd.DataFrame(data, columns=['ID', 'Name', 'Email', 'Resume Score', 'Timestamp', 'Total Page',
            #                                      'Predicted Field', 'User Level', 'Actual Skills', 'Recommended Skills',
            #                                      'Recommended Course'])
            #             st.dataframe(df)
            #             st.markdown(get_table_download_link(df, 'User_Data.csv', 'Download Report'), unsafe_allow_html=True)
            #             fig = px.pie(df, values=values, names=labels, title='Predicted Field according to Skills')
            #             st.plotly_chart(fig)
                        
            #             ### Pie chart for User's Experienced Level
            #             labels = plot_data.User_level.unique() # type: ignore
            #             values = plot_data.User_level.value_counts() # type: ignore
            #             st.subheader("**Pie-Chart for User's Experienced Level**")
            #             fig = px.pie(values=values, names=labels, title="Pie-Chart for User's Experienced Level")
            #             st.plotly_chart(fig)
                        
            #         else:
            #             st.error("Wrong ID & Password Provided")
                        
run()
