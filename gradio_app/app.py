import asyncio
import sys
import gradio as gr
import requests

# =========================================
# FIX WINDOWS ASYNCIO
# =========================================
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()
    )

# =========================================
# BACKEND API
# =========================================
API_URL = "http://127.0.0.1:8000"


# =========================================
# PROCESS FUNCTION
# =========================================
def process_audio(
    audio,
    text_input,
    text_file,
    mode,
    target_lang
):

    # =====================================
    # VALIDASI INPUT
    # =====================================
    if (
        (audio is None or audio == "")
        and
        (text_input is None or text_input.strip() == "")
        and
        (text_file is None)
    ):

        return (
            "Belum ada input.",
            "",
            "-",
            "-",
            "Masukkan audio, teks, atau file TXT.",
            None
        )

    try:

        # =====================================
        # PRIORITAS INPUT
        # =====================================

        input_text = None

        # =====================================
        # TEXT MANUAL
        # =====================================
        if (
            text_input
            and
            text_input.strip() != ""
        ):

            input_text = text_input.strip()

        # =====================================
        # TXT FILE
        # =====================================
        elif text_file is not None:

            with open(
                text_file,
                "r",
                encoding="utf-8"
            ) as f:

                input_text = f.read()

        # =====================================
        # MODE TEXT
        # =====================================
        if input_text:

            data = {

                "text": input_text,

                "mode": mode,

                "target_lang": target_lang
            }

            response = requests.post(

                f"{API_URL}/text-chat",

                data=data,

                timeout=180
            )

        # =====================================
        # MODE AUDIO
        # =====================================
        else:

            with open(audio, "rb") as f:

                files = {
                    "audio": f
                }

                data = {

                    "mode": mode,

                    "target_lang": target_lang
                }

                response = requests.post(

                    f"{API_URL}/voice-chat",

                    files=files,

                    data=data,

                    timeout=180
                )

        # =====================================
        # ERROR BACKEND
        # =====================================
        if response.status_code != 200:

            return (

                "ERROR",

                "ERROR",

                "ERROR",

                "ERROR",

                f"Backend Error:\n{response.text}",

                None
            )

        result = response.json()

        tags = ", ".join(
            result.get("tags", [])
        )

        return (

            result.get(
                "transcript",
                ""
            ),

            result.get(
                "normalized",
                ""
            ),

            result.get(
                "language",
                ""
            ),

            tags,

            result.get(
                "response",
                ""
            ),

            result.get(
                "audio_path",
                None
            )
        )

    except Exception as e:

        return (

            "SYSTEM ERROR",

            "",

            "",

            "",

            str(e),

            None
        )


# =========================================
# PREMIUM CSS
# =========================================
custom_css = """

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

html,
body,
.gradio-container {

    margin: 0 !important;
    padding: 0 !important;

    min-height: 100vh !important;

    background:
    radial-gradient(circle at top left, #172554 0%, transparent 30%),
    radial-gradient(circle at top right, #3b0764 0%, transparent 30%),
    #020617 !important;

    font-family:
    'Inter',
    sans-serif !important;

    color:
    white !important;
}

.gradio-container {

    max-width: 100% !important;

    padding-left: 40px !important;
    padding-right: 40px !important;
    padding-top: 10px !important;
    padding-bottom: 40px !important;
}

/* =======================================
HERO
======================================= */

.hero-wrapper {

    text-align: center;

    padding-top: 55px;

    padding-bottom: 45px;
}

.hero-badge {

    display: inline-block;

    padding: 8px 20px;

    border-radius: 999px;

    background:
    rgba(59,130,246,0.12);

    border:
    1px solid rgba(59,130,246,0.25);

    color:
    #60a5fa;

    font-size: 11px;

    font-weight: 700;

    letter-spacing: 1.5px;

    margin-bottom: 22px;
}

.hero-title {

    font-size: 78px;

    font-weight: 900;

    line-height: 1;

    margin-bottom: 24px;

    background:
    linear-gradient(
        90deg,
        #60a5fa,
        #8b5cf6,
        #d946ef
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {

    max-width: 950px;

    margin: auto;

    color:
    #94a3b8;

    font-size: 18px;

    line-height: 1.9;
}

/* =======================================
CHIPS
======================================= */

.chip-container {

    display: flex;

    justify-content: center;

    flex-wrap: wrap;

    gap: 14px;

    margin-top: 34px;
}

.chip {

    background:
    rgba(17,24,39,0.72);

    border:
    1px solid rgba(255,255,255,0.06);

    padding:
    11px 18px;

    border-radius: 16px;

    font-size: 13px;

    font-weight: 600;

    color: white;
}

/* =======================================
MAIN
======================================= */

.main-row {

    width: 100% !important;

    gap: 24px !important;

    align-items: stretch !important;
}

/* =======================================
PANEL
======================================= */

.custom-panel {

    background:
    rgba(15,23,42,0.82) !important;

    border:
    1px solid rgba(255,255,255,0.06) !important;

    border-radius:
    30px !important;

    padding:
    28px !important;

    backdrop-filter:
    blur(20px);

    height: 100%;
}

.panel-label {

    font-size: 13px;

    font-weight: 800;

    color:
    #60a5fa;

    letter-spacing: 1.7px;

    margin-bottom: 22px;

    text-transform: uppercase;
}

/* =======================================
INPUTS
======================================= */

textarea,
input,
select {

    background:
    rgba(15,23,42,0.95) !important;

    color:
    white !important;

    border-radius:
    18px !important;

    border:
    1px solid rgba(255,255,255,0.06) !important;

    padding:
    16px !important;

    font-size:
    15px !important;
}

textarea:focus,
input:focus,
select:focus {

    border-color:
    rgba(96,165,250,0.45) !important;

    box-shadow:
    0 0 0 4px rgba(96,165,250,0.08) !important;
}

label {

    color:
    #cbd5e1 !important;

    font-size:
    13px !important;

    font-weight:
    600 !important;
}

/* =======================================
AUDIO INPUT
======================================= */

#audio-upload {

    border:
    2px dashed rgba(96,165,250,0.25) !important;

    background:
    rgba(15,23,42,0.95) !important;

    border-radius:
    20px !important;
}

/* =======================================
TEXT BOX
======================================= */

#text-input textarea {

    min-height: 140px !important;
}

/* =======================================
BUTTON
======================================= */

.btn-generate {

    background:
    linear-gradient(
        90deg,
        #3b82f6,
        #8b5cf6
    ) !important;

    border:
    none !important;

    color:
    white !important;

    font-weight:
    700 !important;

    height:
    58px !important;

    border-radius:
    18px !important;

    margin-top:
    18px !important;

    font-size:
    16px !important;
}

/* =======================================
AUDIO PLAYER
======================================= */

[data-testid="audio"] {

    background:
    rgba(15,23,42,0.95) !important;

    border:
    1px solid rgba(255,255,255,0.06) !important;

    border-radius:
    20px !important;

    padding:
    14px !important;
}

/* =======================================
FOOTER
======================================= */

.footer-text {

    text-align: center;

    margin-top: 45px;

    color:
    #64748b;

    font-size:
    14px;

    padding-bottom:
    20px;
}

"""

# =========================================
# UI
# =========================================
with gr.Blocks(
    title="AI Pengalihan Kode Suara"
) as demo:

    # =====================================
    # HERO
    # =====================================
    gr.HTML("""

    <div class="hero-wrapper">

        <div class="hero-badge">
            REAL-TIME MULTILINGUAL NLP SYSTEM
        </div>

        <div class="hero-title">
            AI Pengalihan Kode Suara
        </div>

        <div class="hero-subtitle">

            Mendukung code-switching Bahasa Indonesia,
            Bahasa Inggris, dan Bahasa Arab secara real-time
            menggunakan Whisper, Gemma, dan XTTS v2.

        </div>

        <div class="chip-container">

            <div class="chip"> Indonesia 🇮🇩 </div>

            <div class="chip"> English 🇺🇸 </div>

            <div class="chip"> Arabic 🇸🇦 </div>

            <div class="chip">⚡ Real-Time</div>

            <div class="chip">🎤 Speech-to-Speech</div>

            <div class="chip">🧠 NLP Pipeline</div>

        </div>

    </div>

    """)

    # =====================================
    # MAIN
    # =====================================
    with gr.Row(
        equal_height=True,
        elem_classes="main-row"
    ):

        # =================================
        # LEFT
        # =================================
        with gr.Column(scale=4):

            with gr.Column(
                elem_classes="custom-panel"
            ):

                gr.HTML("""
                <div class="panel-label">
                🎤 KONFIGURASI MASUKAN
                </div>
                """)

                audio_input = gr.Audio(

                    label="Unggah Audio Suara",

                    type="filepath",

                    sources=[
                        "upload",
                        "microphone"
                    ],

                    elem_id="audio-upload"
                )

                text_input = gr.Textbox(

                    label="✍️ Atau Masukkan Teks",

                    placeholder="""
Contoh:
Halo, bagaimana cuaca hari ini?
                    """,

                    lines=5,

                    elem_id="text-input"
                )

                text_file = gr.File(

                    label="📄 Upload File TXT",

                    file_types=[".txt"],

                    type="filepath"
                )

                gr.Markdown("""

> ⚠️ Gunakan salah satu input:
> Audio, teks, atau file TXT.

                """)

                target_lang = gr.Dropdown(

                    label="🌐 Bahasa Tanggapan",

                    choices=[
                        "Indonesia",
                        "English",
                        "Arabic"
                    ],

                    value="Indonesia"
                )

                mode = gr.Dropdown(

                    label="⚙️ Mode Respons AI",

                    choices=[
                        "preserve",
                        "normalize",
                        "translate"
                    ],

                    value="preserve"
                )

                submit_btn = gr.Button(

                    "🚀 Hasilkan Respons AI",

                    elem_classes="btn-generate"
                )

        # =================================
        # RIGHT
        # =================================
        with gr.Column(scale=6):

            with gr.Column(
                elem_classes="custom-panel"
            ):

                gr.HTML("""
                <div class="panel-label">
                📊 HASIL ANALISIS AI
                </div>
                """)

                transcript = gr.Textbox(

                    label="📄 Transkrip",

                    lines=4
                )

                normalized = gr.Textbox(

                    label="✨ Teks Dinormalisasi",

                    lines=4
                )

                with gr.Row():

                    language = gr.Textbox(
                        label="🌐 Bahasa"
                    )

                    tags = gr.Textbox(
                        label="🏷️ NLP Tags"
                    )

                response_text = gr.Textbox(

                    label="🤖 Respons AI",

                    lines=7
                )

                audio_output = gr.Audio(

                    label="🔊 Output Suara AI",

                    interactive=False,

                    type="filepath"
                )

    # =====================================
    # BUTTON EVENT
    # =====================================
    submit_btn.click(

        fn=process_audio,

        inputs=[
            audio_input,
            text_input,
            text_file,
            mode,
            target_lang
        ],

        outputs=[
            transcript,
            normalized,
            language,
            tags,
            response_text,
            audio_output
        ]
    )

    # =====================================
    # FOOTER
    # =====================================
    gr.HTML("""

    <div class="footer-text">

        Built with FastAPI • Whisper • Gemma • XTTS v2 • Gradio

        <br>

        Multilingual NLP Final Project

    </div>

    """)

# =========================================
# RUN
# =========================================
if __name__ == "__main__":

    demo.queue(max_size=20)

    demo.launch(

        server_name="0.0.0.0",

        server_port=7861,

        inbrowser=True,

        share=True,

        css=custom_css
    )