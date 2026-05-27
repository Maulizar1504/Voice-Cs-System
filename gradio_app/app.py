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
API_URL = "http://127.0.0.1:8000/voice-chat"


# =========================================
# PROCESS FUNCTION
# =========================================
def process_audio(audio, text_input, mode, target_lang):

    # =========================
    # VALIDASI INPUT
    # =========================
    if (
        (audio is None or audio == "")
        and
        (text_input is None or text_input.strip() == "")
    ):
        return (
            "Belum ada input.",
            "",
            "-",
            "-",
            "Masukkan audio ATAU teks.",
            None
        )

    try:

        # =====================================
        # MODE TEXT INPUT
        # =====================================
        if text_input and text_input.strip() != "":

            data = {
                "text": text_input,
                "mode": mode,
                "target_lang": target_lang
            }

            response = requests.post(
                f"{API_URL}/text",
                data=data,
                timeout=180
            )

        # =====================================
        # MODE AUDIO INPUT
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
                    API_URL,
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

/* =======================================
FULL WIDTH
======================================= */

.gradio-container {

    max-width: 100% !important;

    padding-left: 40px !important;
    padding-right: 40px !important;
    padding-top: 10px !important;
    padding-bottom: 40px !important;
}

/* =======================================
REMOVE DEFAULT
======================================= */

.block,
.gr-box,
.gr-panel {

    border: none !important;
    box-shadow: none !important;
}

/* =======================================
HERO
======================================= */

.hero-wrapper {

    text-align: center;

    padding-top: 50px;

    padding-bottom: 50px;
}

.hero-badge {

    display: inline-block;

    padding: 8px 20px;

    border-radius: 999px;

    background:
    rgba(59,130,246,0.10);

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

    font-size: 82px;

    font-weight: 900;

    line-height: 1;

    margin-bottom: 25px;

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

    max-width: 980px;

    margin: auto;

    color:
    #94a3b8;

    font-size: 19px;

    line-height: 1.8;
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
    rgba(17,24,39,0.75);

    border:
    1px solid rgba(255,255,255,0.06);

    padding:
    11px 18px;

    border-radius: 14px;

    font-size: 13px;

    font-weight: 600;

    color: white;
}

/* =======================================
MAIN LAYOUT
======================================= */

.main-row {

    width: 100% !important;

    align-items: stretch !important;

    gap: 22px !important;
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
    28px !important;

    padding:
    28px !important;

    backdrop-filter:
    blur(20px);

    margin-bottom:
    18px !important;

    height: 100%;
}

/* =======================================
PANEL TITLE
======================================= */

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
AUDIO BOX
======================================= */

#audio-upload {

    border:
    2px dashed rgba(96,165,250,0.25) !important;

    background:
    rgba(15,23,42,0.95) !important;

    border-radius:
    20px !important;

    padding: 10px !important;
}

/* =======================================
TEXT INPUT BOX
======================================= */

#text-input textarea {

    min-height: 140px !important;

    resize: vertical !important;
}

/* =======================================
INPUT
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

/* =======================================
LABEL
======================================= */

label {

    color:
    #cbd5e1 !important;

    font-size:
    13px !important;

    font-weight:
    600 !important;
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

    transition:
    0.3s ease !important;
}

.btn-generate:hover {

    transform:
    translateY(-2px);

    box-shadow:
    0 12px 35px rgba(59,130,246,0.35) !important;
}

/* =======================================
TEXTBOX OUTPUT
======================================= */

textarea[readonly] {

    background:
    rgba(2,6,23,0.95) !important;
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

    overflow: visible !important;
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

/* =======================================
RESPONSIVE
======================================= */

@media (max-width: 1200px) {

    .hero-title {

        font-size: 58px;
    }
}

@media (max-width: 768px) {

    .gradio-container {

        padding-left: 16px !important;
        padding-right: 16px !important;
    }

    .hero-title {

        font-size: 42px;
    }

    .hero-subtitle {

        font-size: 15px;
    }
}

"""


# =========================================
# UI
# =========================================
with gr.Blocks(
    title="AI Pengalihan Kode Suara",
    css=custom_css
) as demo:

    # =====================================
    # HERO
    # =====================================
    gr.HTML("""

    <div class="hero-wrapper">

        <div class="hero-badge">
            SISTEM NLP MULTIBAHASA WAKTU NYATA
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

            <div class="chip">🇮🇩</div>
            <div class="chip">🇺🇸</div>
            <div class="chip">🇸🇦</div>
            <div class="chip">Real-Time</div>
            <div class="chip">Speech-to-Speech</div>
            <div class="chip">NLP Pipeline</div>

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
        # LEFT PANEL
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

                # =========================
                # AUDIO INPUT
                # =========================
                audio_input = gr.Audio(

                    label="Unggah Audio Suara",

                    type="filepath",

                    sources=[
                        "upload",
                        "microphone"
                    ],

                    elem_id="audio-upload"
                )

                # =========================
                # OR TEXT
                # =========================
                text_input = gr.Textbox(

                    label="✍️ Atau Masukkan Teks",

                    placeholder="""
Contoh:
Halo, bisa bantu jelaskan cara apply visa Saudi?
                    """,

                    lines=5,

                    elem_id="text-input"
                )

                gr.Markdown("""
> ⚠️ Gunakan salah satu input saja:
> Upload audio **ATAU** masukkan teks.
                """)

                # =========================
                # TARGET LANGUAGE
                # =========================
                target_lang = gr.Dropdown(

                    label="🌐 Bahasa Tanggapan",

                    choices=[
                        "Indonesia",
                        "English",
                        "Arabic"
                    ],

                    value="Indonesia"
                )

                # =========================
                # MODE
                # =========================
                mode = gr.Dropdown(

                    label="⚙️ Mode Respons AI",

                    choices=[
                        "preserve",
                        "normalize",
                        "translate"
                    ],

                    value="preserve"
                )

                # =========================
                # BUTTON
                # =========================
                submit_btn = gr.Button(

                    "🚀 Hasilkan Respons AI",

                    elem_classes="btn-generate"
                )

        # =================================
        # RIGHT PANEL
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

                    lines=4,

                    placeholder="Hasil transkrip audio..."
                )

                normalized = gr.Textbox(

                    label="✨ Teks Dinormalisasi",

                    lines=4,

                    placeholder="Hasil normalisasi teks..."
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

                    lines=7,

                    placeholder="Respons AI akan muncul..."
                )

                audio_output = gr.Audio(
                    label="🔊 Output Suara AI",
                    interactive=False
                )

    # =====================================
    # BUTTON EVENT
    # =====================================
    submit_btn.click(

        fn=process_audio,

        inputs=[
            audio_input,
            text_input,
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


# =========================================
# RUN
# =========================================
if __name__ == "__main__":

    demo.queue(max_size=20)

    demo.launch(

        server_name="127.0.0.1",

        server_port=7861,

        inbrowser=True,

        share=False
    )