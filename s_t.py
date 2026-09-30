import os
import time
import streamlit as st

from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events

from PIL import Image
from gtts import gTTS
from googletrans import Translator


# ---------------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# ---------------------------------------------------------

st.set_page_config(
    page_title="Traductor Mágico",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------------------------------------------------
# ESTILOS PERSONALIZADOS
# ---------------------------------------------------------

st.markdown("""
<style>

/* Fondo general */
.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(124, 58, 237, 0.30), transparent 35%),
        radial-gradient(circle at 90% 20%, rgba(236, 72, 153, 0.25), transparent 35%),
        radial-gradient(circle at 50% 90%, rgba(59, 130, 246, 0.20), transparent 40%),
        #0b1020;

    color: white;
}

/* Quitar espacio superior excesivo */
.block-container {
    padding-top: 2rem;
    padding-bottom: 4rem;
    max-width: 1150px;
}

/* Títulos */
.main-title {
    font-size: 3.6rem;
    font-weight: 900;
    text-align: center;
    margin-bottom: 0px;

    background: linear-gradient(
        90deg,
        #c084fc,
        #f472b6,
        #60a5fa
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    text-align: center;
    color: #cbd5e1;
    font-size: 1.15rem;
    margin-top: 5px;
    margin-bottom: 30px;
}

/* Tarjetas */
.glass-card {
    background: rgba(255, 255, 255, 0.07);
    border: 1px solid rgba(255, 255, 255, 0.12);

    border-radius: 25px;
    padding: 28px;

    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);

    box-shadow:
        0px 20px 50px rgba(0,0,0,0.25);

    margin-bottom: 20px;
}

/* Tarjeta pequeña */
.mini-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.10);
    padding: 18px;
    border-radius: 18px;
    margin-bottom: 12px;
}

/* Texto */
.description-text {
    color: #dbeafe;
    font-size: 1rem;
    line-height: 1.7;
}

/* Badge */
.badge {
    display: inline-block;
    padding: 7px 14px;

    border-radius: 50px;

    background: linear-gradient(
        90deg,
        rgba(168,85,247,0.25),
        rgba(236,72,153,0.25)
    );

    border: 1px solid rgba(255,255,255,0.15);

    color: #f8fafc;
    font-size: 0.85rem;

    margin-bottom: 15px;
}

/* Divisor */
.custom-line {
    height: 1px;

    background: linear-gradient(
        90deg,
        transparent,
        rgba(255,255,255,0.35),
        transparent
    );

    margin: 25px 0;
}


/* Inputs Streamlit */
div[data-baseweb="select"] > div {
    background-color: rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
}

/* Botones de Streamlit */
.stButton > button {
    width: 100%;
    border-radius: 14px;

    background: linear-gradient(
        90deg,
        #8b5cf6,
        #ec4899
    );

    color: white;

    font-weight: 700;

    border: none;

    padding: 0.7rem 1rem;

    transition: all 0.25s ease;
}

.stButton > button:hover {

    transform: translateY(-2px);

    box-shadow:
        0 10px 25px rgba(236,72,153,0.3);
}

/* Sidebar */
section[data-testid="stSidebar"] {

    background:
        linear-gradient(
            180deg,
            rgba(15,23,42,0.98),
            rgba(30,27,75,0.98)
        );
}

/* Footer */
.footer {
    text-align: center;
    margin-top: 40px;

    color: #64748b;
    font-size: 0.8rem;
}

/* Imagen */
[data-testid="stImage"] img {
    border-radius: 25px;

    box-shadow:
        0px 20px 45px rgba(0,0,0,0.30);
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.markdown("## 🌎 Traductor")

    st.markdown("""
    Convierte tu voz en texto y tradúcela fácilmente.

    **¿Cómo funciona?**

    🎤 Presiona **Escuchar**

    🗣️ Habla claramente

    🌍 Selecciona el idioma

    ✨ Obtén tu traducción

    🔊 Escucha el resultado
    """)

    st.divider()

    st.markdown("### ⚙️ Configuración")

    idioma_destino = st.selectbox(
        "Traducir a:",
        [
            "Inglés 🇺🇸",
            "Francés 🇫🇷",
            "Italiano 🇮🇹",
            "Portugués 🇧🇷",
            "Alemán 🇩🇪"
        ]
    )

    st.caption("✨ Tu asistente de idiomas")


# ---------------------------------------------------------
# ENCABEZADO
# ---------------------------------------------------------

st.markdown(
    '<div class="main-title">🎙️ Traductor Mágico</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Habla. Traduce. Escucha. 🌎✨'
    '</div>',
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# CONTENIDO PRINCIPAL
# ---------------------------------------------------------

col1, col2 = st.columns([1, 1.3], gap="large")


# ---------------------------------------------------------
# COLUMNA DE IMAGEN
# ---------------------------------------------------------

with col1:

    try:

        imagen = Image.open("fotico.jpg")

        st.image(
            imagen,
            use_container_width=True
        )

    except:

        st.warning(
            "⚠️ No encontré `fotico.jpg`. "
            "Asegúrate de que esté en la misma carpeta del programa."
        )

    st.markdown("""
    <div class="mini-card">

    <span class="badge">✨ Traducción inteligente</span>

    <div class="description-text">

    🎧 Reconoce tu voz directamente desde el navegador.

    🌎 Traduce tus palabras a diferentes idiomas.

    🔊 También puede leer la traducción por ti.

    </div>

    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------
# COLUMNA DEL TRADUCTOR
# ---------------------------------------------------------

with col2:

    st.markdown("""
    <div class="glass-card">

    <span class="badge">🎤 RECONOCIMIENTO DE VOZ</span>

    <h2 style="margin-top:0;">
        ¿Qué quieres traducir?
    </h2>

    <p class="description-text">
        Toca el micrófono y comienza a hablar.
        Cuando termines, tu voz aparecerá automáticamente
        como texto.
    </p>

    </div>
    """, unsafe_allow_html=True)


    # -----------------------------------------------------
    # BOTÓN BOKEH PARA RECONOCIMIENTO DE VOZ
    # -----------------------------------------------------

    stt_button = Button(
        label="🎙️  ESCUCHAR",
        width=420,
        height=60,
        button_type="success"
    )


    stt_button.js_on_event(
        "button_click",
        CustomJS(code="""

        var recognition = new webkitSpeechRecognition();

        recognition.continuous = false;
        recognition.interimResults = true;

        // Idioma de entrada
        recognition.lang = 'es-ES';


        recognition.onstart = function() {

            console.log("🎤 Escuchando...");

        };


        recognition.onresult = function(e) {

            var value = "";

            for (
                var i = e.resultIndex;
                i < e.results.length;
                ++i
            ) {

                if (e.results[i].isFinal) {

                    value +=
                        e.results[i][0].transcript;

                }

            }


            if (value != "") {

                document.dispatchEvent(

                    new CustomEvent(
                        "GET_TEXT",
                        {
                            detail: value
                        }
                    )

                );

            }

        };


        recognition.onerror = function(event) {

            console.log(
                "Error:",
                event.error
            );

        };


        recognition.onend = function() {

            console.log(
                "Reconocimiento detenido"
            );

        };


        recognition.start();

        """)
    )


    result = streamlit_bokeh_events(

        stt_button,

        events="GET_TEXT",

        key="listen",

        refresh_on_update=False,

        override_height=75,

        debounce_time=0

    )


# ---------------------------------------------------------
# PROCESAMIENTO DEL TEXTO
# ---------------------------------------------------------

if result:

    if "GET_TEXT" in result:

        texto_original = result.get("GET_TEXT")

        st.markdown(
            '<div class="custom-line"></div>',
            unsafe_allow_html=True
        )

        st.markdown("### 🗣️ Esto fue lo que entendí")

        st.success(texto_original)


        # -------------------------------------------------
        # IDIOMAS
        # -------------------------------------------------

        idiomas = {

            "Inglés 🇺🇸": "en",
            "Francés 🇫🇷": "fr",
            "Italiano 🇮🇹": "it",
            "Portugués 🇧🇷": "pt",
            "Alemán 🇩🇪": "de"

        }


        codigo_idioma = idiomas[
            idioma_destino
        ]


        # -------------------------------------------------
        # TRADUCCIÓN
        # -------------------------------------------------

        try:

            translator = Translator()

            traduccion = translator.translate(

                texto_original,

                src="es",

                dest=codigo_idioma

            )


            texto_traducido = traduccion.text


            st.markdown("### 🌎 Traducción")

            st.markdown(
                f"""
                <div class="glass-card">

                    <div style="
                        font-size:0.85rem;
                        color:#94a3b8;
                        margin-bottom:10px;
                    ">

                    TRADUCIDO A {idioma_destino.upper()}

                    </div>

                    <div style="
                        font-size:1.6rem;
                        font-weight:700;
                        line-height:1.5;
                    ">

                    {texto_traducido}

                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


            # ---------------------------------------------
            # TEXTO A VOZ
            # ---------------------------------------------

            audio_file = "traduccion.mp3"

            tts = gTTS(

                text=texto_traducido,

                lang=codigo_idioma,

                slow=False

            )

            tts.save(audio_file)


            st.markdown("### 🔊 Escucha la pronunciación")

            st.audio(audio_file)


        except Exception as e:

            st.error(
                "😢 Hubo un problema realizando la traducción."
            )

            st.caption(str(e))


# ---------------------------------------------------------
# MENSAJE CUANDO TODAVÍA NO HAY TEXTO
# ---------------------------------------------------------

else:

    st.info(
        "🎤 Presiona **ESCUCHAR** y di una frase en español."
    )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown("""
<div class="footer">

✨ Traductor Mágico • Diseñado con Streamlit • 2026

</div>
""", unsafe_allow_html=True)
