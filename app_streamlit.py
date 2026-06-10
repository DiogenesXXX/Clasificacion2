# Debe direccionar VS Code a la carpeta con los archivos:
# 1.- Archivo
# 2.- Abrir carpeta. Debe dar click en la carpeta que contiene los archivos de interés
#3.- A la izquierda, en el explorador deberá poder visualizar todos los archivos
#------------------------------------------------------------------------------------------------

# CÓDIGO STREAMLIT
# Ir a:   Ver/Terminal
# Crea un ambiente virtual (puedes usar otro nombre en lugar de 'venv'): coloca este código
#   python -m venv venv

#---------------------------------------------------------------------------------------
# Luego de crear el ambiente virtual, lo activas
#   .\venv\Scripts\activate   # En Windows
#---------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------
# Cuando vuelva a iniciar sesión, debe volver a activar el ambiente virtual, ya no lo debe crear.
# En este caso debes abrir la carpeta con los archivos del caso.
#---------------------------------------------------------------------------------------------

# Instala la versión específica de scikit-learn
#   pip install scikit-learn==1.2.2
# Instala otras dependencias, incluyendo Streamlit
#  pip install streamlit pandas joblib
#-------------------------------------------------------------------------------------------------
# Desde la segunda vez: hacer:
# Si da error, debes ir a PowerShell de Window y:
#      Get-ExecutionPolicy                           Si es Restricted; ejecuta
#      Set-ExecutionPolicy RemoteSigned              Colocar Sí
# En consola de VSC:  .\venv\Scripts\activate

import streamlit as st
import pandas as pd
from joblib import load
import numpy as np

# -------------------------PROCESO DE DESPLIEGUE------------------------------
# En consola:
# pip install scikit-learn==1.3.2

# 01 --------------------------Load the model-------------------------------------------
clf = load('modelo_rfchurn_tunning.joblib')

# 02---------------- Variables globales para los campos del formulario-----------------------
i03_options = ['A ninguna comisión', 'A una sola comisión', 'A dos comisiones (o más comisiones)']
i03 = ''

i05_options = ['Sí es de carácter económico', 'No es de carácter económico']
i05 = ''

i06_options = ['Sí tiene incidencia económica directa', 'No tiene incidencia económica directa']
i06 = ''

i08_options = ['Seis congresistas o menos', 'Más de seis congresistas', 'Más de diez congresistas']
i08 = ''

i10_options = ['Es de la mayoría parlamentaria', 'Es de la oposición. Criterio: por lo mínimo mayor a 6 integrantes y menor a la mayoría', 'Ni lo uno ni lo otro. Criterio: por lo máximo 6 integrantes']
i10 = ''

i12_options = ['Sí tiene experiencia parlamentaria previa', 'No tiene experiencia parlamentaria previa']
i12 = ''

i14_options = ['Masculino', 'Femenino']
i14 = ''

i15_options = ['Por lo menos mayor a 1', 'Por lo menos mayor a 20', 'Por lo menos mayor a 80']
i15 = ''


age = 0
balance = 0.0
num_of_products = 1
is_active_member_options = [0, 1]
is_active_member = 0

# 03 Reseteo------------- Flag to track error---------------------------------------
error_flag = False

# Reset inputs function
def reset_inputs():
    global geography, age, balance, num_of_products, is_active_member, error_flag, i03, i05, i06, i08, i10, i12, i14, i15
    geography = ''
    i03 = '' 
    i05 = '' 
    i06 = '' 
    i08 = '' 
    i10 = '' 
    i12 = '' 
    i14 = '' 
    i15 = ''
    age = 0
    balance = 0.0
    num_of_products = 1
    is_active_member = 0
    error_flag = False

# Inicializar variables
reset_inputs()
# -----------------------------------------------------------------------------------------------

# ------------------------Título centrado-------------------------------------------------
st.title("Modelo Predictivo de Proyectos de ley del periodo 2015-2016 del Congreso de la República")
st.markdown("Este modelo predice si un proyecto de ley se convertirá en ley en base a ciertas características.")
st.markdown("Autor: Mg. Diogenes Luis Nazario Huanaco")
st.markdown("---")

# ----------------------- Función para validar los campos del formulario----------------------------
def validate_inputs():
    global error_flag
    if any(val < 0 for val in [age, balance]):
        st.error("No se permiten valores negativos. Por favor, ingrese valores válidos en todos los campos.")
        error_flag = True
    else:
        error_flag = False

# ------------------------------------ Formulario en dos columnas------------------------------------
with st.form("churn_form"):
    col1, col2 = st.columns(2)

    # Input fields en la primera columna
    with col1:
        i03 = st.selectbox("**Comisiones del proyecto de ley: **", i03_options)
        i05 = st.selectbox("**Carácter económico del proyecto de ley: **", i05_options)
        i06 = st.selectbox("**Incidencia económica directa del proyecto de ley: **", i06_options)
        i08 = st.selectbox("**Congresistas que integran el proyecto de ley: **", i08_options)


    # Input fields en la segunda columna
    with col2:   
        i10 = st.selectbox("**Alianza política del congresista del proyecto de ley: **", i10_options)
        i12 = st.selectbox("**Experiencia parlamentaria: **", i12_options)
        i14 = st.selectbox("**Sexo del congresista: **", i14_options)
        i15 = st.selectbox("**Proyecto de ley presentados por el congresista: **", i15_options)

    # ----------------------------------------- Boton de Predecir-------------------------------------------------
    predict_button = st.form_submit_button("Predecir")

# Validar que no haya valores negativos en los campos cuando se presiona el botón
# Si hay error no permita seguir tipeando!!!!!!!!!!!!!!!!!!!
if predict_button and error_flag:
    st.stop()

if predict_button and not error_flag:
    # Crear DataFrame
    data = {

         'Item03': [i03],  
         'Item05': [i05],  
         'Item06': [i06],  
         'Item08': [i08],  
         'Item10': [i10],  
         'Item12': [i12],  
         'Item14': [i14],  
         'Item15': [i15]

    }
    df = pd.DataFrame(data)

    # Realizar predicción
    probabilities_classes = clf.predict_proba(df)[0]

    # Obtener la clase con la mayor probabilidad
    class_predicted = np.argmax(probabilities_classes)

    # Asignar salida y probabilidad según la clase predicha
    # En el script original: #Exited: 0 Cliente retenido;  1 Cliente cerró cuenta
    if class_predicted == 0:
        outcome = "Proyecto de ley con probabilidad de NO convertirse en ley"
        probability_churn = probabilities_classes[0]
        style_result = 'background-color: lightgreen; font-size: larger;'
    else:
        outcome = "Proyecto de ley con probabilidad de SI convertirse en ley"
        probability_churn = probabilities_classes[1]
        style_result = 'background-color: lightcoral; font-size: larger;'

    # Mostrar resultado con estilo personalizado
    result_html = f"<div style='{style_result}'>La predicción fue de clase '{outcome}' con una probabilidad de {round(float(probability_churn), 4)}</div>"
    st.markdown(result_html, unsafe_allow_html=True)

# --------------------------- Boton de Resetear-------------------------------------
if st.button("Resetear"):
    # Resetear inputs
    reset_inputs()

# streamlit run app_streamlit.py       en la consola


#pip freeze > requirements.txt
# genera el archivo requirements para el despliegue web.

