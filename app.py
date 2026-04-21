import streamlit as st
import pandas as pd

st.set_page_config(page_title="Modelador AWS para IA", layout="wide")

CASO_BASE = {
    "sector": "Asegurador",
    "documentos_diarios": 18000,
    "usuarios_simultaneos": 220,
    "latencia_max_seg": 4,
    "pii": True,
    "presupuesto": "Medio",
    "variabilidad_demanda": "Media",
    "preferencia_estrategica": "Gestionado",
    "disponibilidad_objetivo": "Alta",
}


def recomendar_inferencia(preferencia_estrategica: str) -> str:
    if preferencia_estrategica == "Gestionado":
        return (
            "Amazon Bedrock para acelerar el despliegue, reducir complejidad operativa "
            "y aprovechar un servicio gestionado."
        )
    return (
        "Amazon SageMaker para mayor control fino del modelo, personalización y ajuste del ciclo de inferencia."
    )



def recomendar_datos(documentos_diarios: int) -> str:
    if documentos_diarios >= 15000:
        return (
            "Repositorio documental corporativo con almacenamiento escalable, indexación y trazabilidad "
            "de versiones para absorber un volumen documental alto."
        )
    return "Repositorio documental interno con indexación básica y control de acceso."



def recomendar_integracion(usuarios_simultaneos: int, latencia_max_seg: int) -> str:
    if usuarios_simultaneos >= 200 or latencia_max_seg <= 4:
        return (
            "Capa de integración orientada a APIs y orquestación ligera, con colas/eventos cuando proceda, "
            "para desacoplar servicios y sostener concurrencia con baja latencia."
        )
    return "Integración por APIs internas con orquestación simple entre fuentes, aplicación y motor de inferencia."



def recomendar_seguridad(pii: bool) -> str:
    if pii:
        return (
            "Controles reforzados: minimización de datos, cifrado, segmentación, revisión humana, "
            "trazabilidad y validación de cumplimiento para el tratamiento de PII."
        )
    return "Controles estándar de acceso, auditoría y gobierno del dato."



def recomendar_observabilidad(variabilidad_demanda: str, presupuesto: str, disponibilidad: str) -> str:
    partes = []
    if variabilidad_demanda == "Alta":
        partes.append("observabilidad reforzada con alertas automáticas de coste, uso y rendimiento")
    elif variabilidad_demanda == "Media":
        partes.append("monitoreo continuo con revisión periódica de consumo y rendimiento")
    else:
        partes.append("observabilidad básica con revisión mensual")

    if disponibilidad in ["Alta", "Muy alta"]:
        partes.append("métricas de resiliencia y continuidad operativa")
    if presupuesto == "Bajo":
        partes.append("control estricto de sobredimensionamiento y gasto")

    return "; ".join(partes).capitalize() + "."



def generar_tradeoff(datos: dict) -> str:
    if datos["preferencia_estrategica"] == "Gestionado":
        return (
            "Se prioriza velocidad de lanzamiento y simplicidad operativa frente a control fino del stack de IA. "
            "La decisión es defendible porque el caso exige respuesta rápida, baja tolerancia al error y gestión "
            "de PII con una carga relevante de usuarios internos."
        )
    return (
        "Se prioriza control fino y personalización frente a rapidez de despliegue. La decisión es defendible si "
        "el equipo necesita ajustar el comportamiento del modelo, a costa de más complejidad operativa."
    )



def generar_resumen(datos: dict) -> str:
    prioridad = []
    if datos["pii"]:
        prioridad.append("seguridad y gobierno del dato")
    if datos["latencia_max_seg"] <= 4:
        prioridad.append("rendimiento")
    if datos["disponibilidad_objetivo"] in ["Alta", "Muy alta"]:
        prioridad.append("continuidad operativa")

    criterio = ", ".join(prioridad) if prioridad else "equilibrio operativo"

    return (
        f"La propuesta aborda la necesidad de un asistente interno para el sector {datos['sector']} capaz de buscar información en documentos, "
        f"preparar borradores y apoyar a gestores humanos. El criterio dominante del diseño es {criterio}, "
        f"sin perder de vista el presupuesto {datos['presupuesto'].lower()} y una demanda {datos['variabilidad_demanda'].lower()}."
    )



def generar_capas(datos: dict) -> dict:
    disponibilidad_texto = {
        "Media": "Arquitectura con continuidad operativa estándar.",
        "Alta": "Arquitectura con redundancia razonable, recuperación planificada y monitoreo continuo.",
        "Muy alta": "Arquitectura con resiliencia reforzada, tolerancia a fallos y objetivos de continuidad más exigentes.",
    }

    capas = {
        "Datos": recomendar_datos(datos["documentos_diarios"]),
        "Integración": recomendar_integracion(datos["usuarios_simultaneos"], datos["latencia_max_seg"]),
        "Inferencia/Modelo": recomendar_inferencia(datos["preferencia_estrategica"]),
        "Aplicación": (
            "Aplicación interna para gestores de siniestros con interfaz simple, flujo guiado, "
            "consulta documental y generación asistida de borradores."
        ),
        "Seguridad y Gobierno": recomendar_seguridad(datos["pii"]),
        "Observabilidad y FinOps": (
            recomendar_observabilidad(
                datos["variabilidad_demanda"],
                datos["presupuesto"],
                datos["disponibilidad_objetivo"],
            )
            + " " + disponibilidad_texto[datos["disponibilidad_objetivo"]]
        ),
    }
    return capas



def generar_riesgos(datos: dict) -> pd.DataFrame:
    riesgos = [
        {
            "Riesgo": "Exposición de datos personales sensibles",
            "Alternativa/Mitigación": "Minimización de datos, control de acceso, cifrado y revisión humana antes de respuestas sensibles",
            "Gobernanza": "Compliance + Responsable de Seguridad",
            "Acción": "Validar tratamiento de PII antes del despliegue y revisar permisos periódicamente",
        },
        {
            "Riesgo": "Latencia superior al objetivo operativo",
            "Alternativa/Mitigación": "Optimizar consultas, medir tiempos extremo a extremo y escalar componentes críticos",
            "Gobernanza": "Arquitecto SI/TI + Responsable de Operación",
            "Acción": "Ejecutar pruebas de rendimiento y fijar umbrales de alerta",
        },
        {
            "Riesgo": "Sobrecoste del servicio de inferencia",
            "Alternativa/Mitigación": "Alertas de consumo, límites de uso y revisión del patrón de consultas",
            "Gobernanza": "FinOps + Responsable de Operación",
            "Acción": "Revisar gasto semanal y ajustar configuración si se supera el umbral",
        },
    ]

    if datos["disponibilidad_objetivo"] == "Muy alta":
        riesgos.append(
            {
                "Riesgo": "Caída del servicio con impacto en continuidad operativa",
                "Alternativa/Mitigación": "Diseño resiliente, monitorización reforzada y procedimientos de contingencia",
                "Gobernanza": "Arquitecto SI/TI + Operaciones",
                "Acción": "Probar escenarios de fallo y recuperación",
            }
        )

    return pd.DataFrame(riesgos[:3])



def generar_slos(datos: dict) -> pd.DataFrame:
    disponibilidad_map = {
        "Media": "99.0% mensual",
        "Alta": "99.5% mensual",
        "Muy alta": "99.9% mensual",
    }

    slos = [
        {
            "Indicador": "Latencia máxima objetivo",
            "Valor propuesto": f"<= {datos['latencia_max_seg']} s en consultas estándar",
        },
        {
            "Indicador": "Disponibilidad del servicio",
            "Valor propuesto": disponibilidad_map[datos["disponibilidad_objetivo"]],
        },
        {
            "Indicador": "Tasa de escalado a humano en casos sensibles o ambiguos",
            "Valor propuesto": "100% de casos con PII sensible o baja confianza deben poder derivarse a revisión humana",
        },
    ]
    return pd.DataFrame(slos)


st.sidebar.header("Parámetros de entrada")
sector = st.sidebar.text_input("Sector", CASO_BASE["sector"])
documentos_diarios = st.sidebar.number_input(
    "Documentos diarios", min_value=0, value=CASO_BASE["documentos_diarios"]
)
usuarios_simultaneos = st.sidebar.number_input(
    "Usuarios simultáneos", min_value=0, value=CASO_BASE["usuarios_simultaneos"]
)
latencia_max_seg = st.sidebar.number_input(
    "Latencia máxima tolerada (segundos)", min_value=1, value=CASO_BASE["latencia_max_seg"]
)
pii = st.sidebar.checkbox("¿Hay datos personales sensibles (PII)?", value=CASO_BASE["pii"])
presupuesto = st.sidebar.selectbox("Presupuesto", ["Bajo", "Medio", "Alto"], index=1)
variabilidad_demanda = st.sidebar.selectbox("Variabilidad de la demanda", ["Baja", "Media", "Alta"], index=1)
preferencia_estrategica = st.sidebar.selectbox("Preferencia estratégica", ["Gestionado", "Control fino"], index=0)
disponibilidad_objetivo = st.sidebar.selectbox("Disponibilidad objetivo", ["Media", "Alta", "Muy alta"], index=1)

datos = {
    "sector": sector,
    "documentos_diarios": documentos_diarios,
    "usuarios_simultaneos": usuarios_simultaneos,
    "latencia_max_seg": latencia_max_seg,
    "pii": pii,
    "presupuesto": presupuesto,
    "variabilidad_demanda": variabilidad_demanda,
    "preferencia_estrategica": preferencia_estrategica,
    "disponibilidad_objetivo": disponibilidad_objetivo,
}

st.title("Modelador de Arquitecturas AWS para IA")
st.write("Propuesta inicial de arquitectura lógica basada en reglas simples y justificables.")

st.subheader("1. Resumen ejecutivo")
st.write(generar_resumen(datos))

st.subheader("2. Arquitectura propuesta por 6 capas")
capas = generar_capas(datos)
for capa, descripcion in capas.items():
    st.markdown(f"**{capa}:** {descripcion}")

st.subheader("3. Trade-off principal")
st.write(generar_tradeoff(datos))

st.subheader("4. Matriz RAGA")
st.dataframe(generar_riesgos(datos), use_container_width=True)

st.subheader("5. SLO/SLA propuestos")
st.dataframe(generar_slos(datos), use_container_width=True)

st.subheader("6. Justificación breve del equipo")
st.info(
    "El equipo decide priorizar una opción gestionada porque el caso combina PII, baja tolerancia al error, "
    "latencia objetivo exigente y necesidad de salida rápida a producción. Aceptamos perder parte del control fino "
    "del stack a cambio de simplicidad operativa, mayor gobernabilidad inicial y menor fricción de despliegue."
)
