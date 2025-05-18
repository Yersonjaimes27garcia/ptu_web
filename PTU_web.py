import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def graficar_reparto(df_resultado):
    df_grafica = df_resultado[df_resultado["Nombre del trabajador"] != "SUMAS"]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(df_grafica["Nombre del trabajador"], df_grafica["Totales"], color='skyblue')
    ax.set_title("PTU Total por Trabajador")
    ax.set_xlabel("Trabajador")
    ax.set_ylabel("Monto de PTU")
    plt.xticks(rotation=45)
    st.pyplot(fig)

def PTU_manualmente():
    st.subheader("Ingreso manual de datos")
    utilidad_base = st.number_input("Ingrese la utilidad base de la empresa:", min_value=0.01)

    n = st.number_input("Ingrese la cantidad de trabajadores:", min_value=1, step=1)
    trabajadores = []

    for i in range(int(n)):
        st.markdown(f"**Trabajador #{i+1}**")
        nombre = st.text_input(f"Nombre del trabajador #{i+1}", key=f"nombre_{i}")
        sueldo = st.number_input(f"Sueldo obtenido del trabajador {nombre}:", key=f"sueldo_{i}", min_value=0.0)
        dias = st.number_input(f"Días trabajados del trabajador {nombre}:", key=f"dias_{i}", min_value=0, max_value=365)
        trabajadores.append({"Nombre del trabajador": nombre, "Días trabajados": dias, "Sueldo": sueldo})

    if st.button("Calcular reparto manual"):
        df = pd.DataFrame(trabajadores)
        porcentaje_10 = round(utilidad_base * 0.1, 5)
        porcentaje_dias = round(porcentaje_10 * 0.5, 5)
        porcentaje_sueldos = round(porcentaje_10 * 0.5, 5)

        suma_dias = df["Días trabajados"].sum()
        suma_sueldos = df["Sueldo"].sum()

        factor_dias = porcentaje_dias / suma_dias
        factor_sueldos = porcentaje_sueldos / suma_sueldos

        df["Días"] = factor_dias * df["Días trabajados"]
        df["Sueldos"] = factor_sueldos * df["Sueldo"]
        df["Totales"] = df["Días"] + df["Sueldos"]

        df_resultado = df[["Nombre del trabajador", "Días", "Sueldos", "Totales"]].copy()
        df_resultado.loc[len(df_resultado)] = [
            "SUMAS",
            df_resultado["Días"].sum(),
            df_resultado["Sueldos"].sum(),
            df_resultado["Totales"].sum()
        ]

        st.subheader("Resultado del reparto de utilidades")
        st.dataframe(df_resultado)
        graficar_reparto(df_resultado)

def PTU_excel():
    st.subheader("Cálculo desde archivo Excel")
    archivo_excel = st.file_uploader("Sube tu archivo Excel", type=["xlsx"])

    if archivo_excel:
        utilidad_base = st.number_input("Ingrese la utilidad base de la empresa:", min_value=0.01)
        df = pd.read_excel(archivo_excel)

        columnas_requeridas = ["Trabajador", "Días trabajados", "Sueldos obtenidos"]
        if not all(col in df.columns for col in columnas_requeridas):
            st.error(f"El archivo debe contener las columnas: {columnas_requeridas}")
            return

        df.rename(columns={"Trabajador": "Nombre del trabajador", "Sueldos obtenidos": "Sueldo"}, inplace=True)

        if st.button("Calcular reparto desde Excel"):
            porcentaje_10 = round(utilidad_base * 0.1, 5)
            porcentaje_dias = round(porcentaje_10 * 0.5, 5)
            porcentaje_sueldos = round(porcentaje_10 * 0.5, 5)

            suma_dias = df["Días trabajados"].sum()
            suma_sueldos = df["Sueldo"].sum()

            factor_dias = porcentaje_dias / suma_dias
            factor_sueldos = porcentaje_sueldos / suma_sueldos

            df["Días"] = factor_dias * df["Días trabajados"]
            df["Sueldos"] = factor_sueldos * df["Sueldo"]
            df["Totales"] = df["Días"] + df["Sueldos"]

            df_resultado = df[["Nombre del trabajador", "Días", "Sueldos", "Totales"]].copy()
            df_resultado.loc[len(df_resultado)] = [
                "SUMAS",
                df_resultado["Días"].sum(),
                df_resultado["Sueldos"].sum(),
                df_resultado["Totales"].sum()
            ]

            st.subheader("Resultado del reparto de utilidades")
            st.dataframe(df_resultado)
            graficar_reparto(df_resultado)

def main():
    st.title("Reparto de Utilidades (PTU)")
    st.markdown("Autor: Yerson Jaimes García")
    st.write("Este programa permite calcular el reparto de utilidades entre trabajadores.")
    opcion = st.selectbox("Selecciona un método de ingreso de datos:", ["Selecciona una opción", "Manual", "Desde archivo Excel"])

    if opcion == "Manual":
        PTU_manualmente()
    elif opcion == "Desde archivo Excel":
        PTU_excel()

if __name__ == "__main__":
    main()





