import streamlit as st
import pandas as pd
import numpy as np
import psutil
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from pathlib import Path
import pickle
import streamlit_authenticator as stauth
import time
import gtts
from playsound import playsound
import os
from pymongo import MongoClient
from playsound import playsound
from pydub import AudioSegment
from pydub.playback import play
#%matplotlib notebook


#im = Image.open('C:/Users/Mcastiblanco/Documents/AGPC/DataScience2020/Streamlit/Arroz/apps/arroz.png')
im2 = Image.open('smf1.jpg')
st.set_page_config(page_title='Pred_App', layout="wide", page_icon=im2)
st.set_option('deprecation.showPyplotGlobalUse', False)
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .checkbox-text {font-size:114px;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

imagel = Image.open('smf1.jpg')
new_image = imagel.resize((300, 100))
new_image2=imagel.resize((300, 150))
#---- USER AUTHENTICATION
names=['Manuel Castiblanco', 'Pedro Gomez']
usernames=['mcastiblanco', 'pgomez']
file_path= Path(__file__).parent/'hashed_pw.pkl'

with file_path.open('rb') as file:
    hashed_passwords=pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    "pre_App", '123456', cookie_expiry_days=30)

name, authentication_status, usernames = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password es incorrecto")

if authentication_status == None:
    st.warning("Por favor introduzca su username y password")

if authentication_status:
    #imagelp2 = Image.open('smf1.jpg')
    #new_image5=imagelp2.resize((120, 40))
    #st.image(new_image5)
    row1_1, row1_2,row1_3 = st.columns((1, 2,1))

    with row1_1:
        image = Image.open('AGP.jpg')#logo.png')
        st.image(image, use_column_width=True)
        #st.image(new_image2)
    with row1_2:
        imagelp = Image.open('predictor.png')
        imagelp2 = Image.open('predictor2.png')
        new_image3=imagelp.resize((240, 80))
        new_image4=imagelp2.resize((240, 80))
        #st.image(new_image2)
        #st.header('PREDIKTOR')
        #new_image5=imagelp2.resize((120, 40))
        #st.image(new_image5)
        st.subheader("""
        SmartFactory
        Esta App controla inteligentemente tu proceso!
        """)

    with row1_3:
        st.image(new_image2)
        #st.markdown('SmartFactory App') #by [GPREnergy](https://www.gprenergy.co/)')
        #st.image(new_image2)
        # with st.expander("Contact us 👉"):
        #     with st.form(key='contact', clear_on_submit=True):
        #         name = st.text_input('Name')
        #         mail = st.text_input('Email')
        #         q = st.text_area("Query")
        #
        #         submit_button = st.form_submit_button(label='Send')
        #         if submit_button:
        #             subject = 'Consulta'
        #             to = 'macs1251@hotmail.com'
        #             sender = 'macs1251@hotmail.com'
        #             smtpserver = smtplib.SMTP("smtp-mail.outlook.com", 587)
        #             user = 'macs1251@hotmail.com'
        #             password = '1251macs'
        #             smtpserver.ehlo()
        #             smtpserver.starttls()
        #             smtpserver.ehlo()
        #             smtpserver.login(user, password)
        #             header = 'To:' + to + '\n' + 'From: ' + sender + '\n' + 'Subject:' + subject + '\n'
        #             message = header + '\n' + name + '\n' + mail + '\n' + q
        #             smtpserver.sendmail(sender, to, message)
        #             smtpserver.close()

    st.header('Aplicación')
    st.markdown('____________________________________________________________________')
    app_des = st.expander('Descripción App')
    with app_des:
        st.write("""Esta aplicación usando IA permite gestionar tu proceso.
        """)

    ####-sidebar

    #st.sidebar.image(new_image, use_column_width=False)
    st.sidebar.header(f" Bienvenido {name}")
    authenticator.logout("Logout", "sidebar")


    i = 0
    x, y = [], []


    st.subheader('Configuración de Límites')
    lms,lmi=st.columns((1,1))
    with lms:
        lmsa=st.slider('Limite de Alerta Amarilla Superior', 0, 100, 40)
        lmsr=st.slider('Limite de Alerta Roja Superior', 0, 100, 80)
    with lmi:
        lmia=st.slider('Limite de Alerta Amarilla Inferior', 0, 100, 20)
        lmir=st.slider('Limite de Alerta Roja Inferior', 0, 100, 10)
    st.subheader('Gráfico de Seguimiento')
    chart = st.line_chart()
    while True:
        x.append(i)
        y.append(psutil.cpu_percent())
        chart.add_rows(y)



        if y[i]>lmsa:
            st.header('Alerta')
            cluster='mongodb+srv://manuel:macs1251@cluster0.3n9ltt2.mongodb.net/Myfirstdata?retryWrites=true&w=majority'
            client=MongoClient(cluster)
            db=client.Myfirstdata
            al=db.Ins.find_one({"Nombre": "Alertas"})
            alerta=list(al.values())[2]
            tts = gtts.gTTS(f'{alerta[3]}. Por favor lea los pasos a seguir y pulse el botón de audio para ejecutarlos, eliminando la anomalía', lang="es")
            with open('alerta.mp3', 'wb') as f:
                tts.write_to_fp(f)
            playsound('alerta.mp3')
            os.remove('alerta.mp3')


            st.warning("Alerta Amarilla: Se Excedio el Límite Superior")
            # df = pd.read_excel('C:/Users/Mcastiblanco/Documents/AGPC/DataScience2020/Streamlit/SmartFactory/AGPGPIN04.40.12 Limpieza Retrofit V2.xlsx')
            # df1=df['Unnamed: 5'].dropna().reset_index()
            # st.subheader('Que hacer')
            # a=[]
            # for i in range(2,len(df1['Unnamed: 5'])):
            #     t=df1['Unnamed: 5'][i].replace('\n','. ')
            #     a.append(t)
            x = db.Ins.find_one({"Nombre": "CELimpieza"})
            a=list(x.values())[2]
            # def dele():
            #     for i in range (20):
            #         try:
            #             os.remove(f"C:/Users/Mcastiblanco/Documents/AGPC/DataScience2020/Streamlit/SmartFactory/ins{i}.mp3")
            #         except:
            #             pass

            # def audio(a):
            #     for i in range(len(a)):
            #         tts = gtts.gTTS(a[i], lang="es")
            #         tts.save(f"C:/Users/Mcastiblanco/Documents/AGPC/DataScience2020/Streamlit/SmartFactory/ins{i}.mp3")

            df = pd.DataFrame(a)
            df.columns=['Acciones']
            #dele()
            time.sleep(1)
            #audio(a)
            c1,c2,c3=st.columns([1,5,1])
            c1.write('**Pasos**')
            c2.write('**Acciones**')
            c3.write('**Audio**')


            for i in range(len(a)-5):
                cols = st.columns([1,5,1],)
                cols[0].write(f'{i+1}')
                cols[1].write(a[i])
                tts = gtts.gTTS(a[i], lang="es")
                with open(f'ins{i}.mp3', 'wb') as f:
                    tts.write_to_fp(f)
                cols[2].audio(f'ins{i}.mp3')

            st.subheader('Registro de eliminación anomalía')
                # Obtener los datos a insertar

                # Insertar los datos en la colección "usuarios"

            with st.form("my_form"):
                id=st.selectbox('Id', 'Realizado Anomalía', 'No realizado' )
                name = st.text_input("Nombre de quien realizó:")
                turno= st.text_input("Turno:")
                submit_button = st.form_submit_button("Enviar")
                if submit_button:
                    db.Ins.insert_one({"nombre": name, "edad": turno, 'date':datetime.datetime.utcnow()})
                    st.success("Datos enviados con éxito")

            # Crear un botón que llame a la función insert_data al ser presionado

            break #print('Alerta')
        time.sleep(1)
        i += 1
