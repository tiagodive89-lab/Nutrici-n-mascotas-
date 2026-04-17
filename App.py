import streamlit as st
import math

st.set_page_config(page_title="Nutrición Veterinaria", page_icon="🐾")
st.title("🥩 Nutrición para perros y gatos")

especie = st.selectbox("Especie", ["Perro", "Gato"])
peso = st.number_input("Peso (kg)", min_value=0.2, max_value=100.0, step=0.1)
edad = st.selectbox("Edad", ["Cachorro (< 12 meses)", "Adulto (1-7 años)", "Geronte (> 7 años)"])
raza = st.text_input("Raza (opcional)", "No especificada")
cc = st.slider("Condición corporal (1=delgado, 9=obeso)", 1, 9, 5)

if especie == "Perro":
    ejercicio = st.select_slider("Nivel de ejercicio", options=["Sedentario", "Moderado", "Activo"])
else:
    ejercicio = st.select_slider("Nivel de actividad (gato)", options=["Muy bajo", "Moderado", "Muy activo"])

st.subheader("Alimentación actual")
tipo_alimento = st.selectbox("Tipo de alimento", ["Pienso seco", "Húmedo", "Mixto"])
kcal_por_gramo = st.number_input("Calorías del alimento (kcal/100g)", min_value=50, max_value=600, value=350)
cantidad_actual_gramos = st.number_input("Cantidad actual (gramos/día)", min_value=0, value=100)

# Cálculos
rer = 70 * (peso ** 0.75)

if especie == "Perro":
    if edad == "Cachorro (< 12 meses)": factor = 2.5
    elif edad == "Adulto (1-7 años)":
        factor = 1.4 if ejercicio == "Sedentario" else (1.6 if ejercicio == "Moderado" else 2.0)
    else: factor = 1.2
else:
    if edad == "Cachorro (< 12 meses)": factor = 2.5
    elif edad == "Adulto (1-7 años)":
        factor = 1.2 if ejercicio == "Muy bajo" else (1.4 if ejercicio == "Moderado" else 1.6)
    else: factor = 1.1

if cc < 4: factor *= 0.9
elif cc > 6: factor *= 1.2

der = rer * factor

proteina_min = peso * (2.0 if especie == "Perro" else 4.0)
proteina_max = peso * (4.5 if especie == "Perro" else 6.0)
agua_ml = peso * 50

kcal_actuales = (cantidad_actual_gramos / 100) * kcal_por_gramo
recomendado_gramos = (der / kcal_por_gramo) * 100

st.header("📊 Resultados")
col1, col2 = st.columns(2)
col1.metric("RER (kcal/día)", f"{rer:.0f}")
col2.metric("DER (kcal/día)", f"{der:.0f}")

st.write(f"**Proteínas diarias:** {proteina_min:.0f} – {proteina_max:.0f} g")
st.write(f"**Agua recomendada:** {agua_ml:.0f} ml/día")
st.write(f"**Kcal que recibe ahora:** {kcal_actuales:.0f} / {der:.0f} kcal")
st.write(f"**Cantidad recomendada:** {recomendado_gramos:.0f} gramos/día")

if kcal_actuales < der * 0.9:
    st.error("⚠️ Está comiendo menos de lo necesario.")
elif kcal_actuales > der * 1.1:
    st.warning("📈 Está comiendo más de lo necesario.")
else:
    st.success("✅ Cantidad adecuada.")
