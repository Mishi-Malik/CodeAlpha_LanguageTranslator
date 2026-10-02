import io
from deep_translator import MyMemoryTranslator
from gtts import gTTS
from languages import LANGUAGES
import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Language Translation Tool | CodeAlpha",
    page_icon="🌐",
    layout="centered",
)


# --- LOAD EXTERNAL CSS FILE ---
def local_css(file_name):
  try:
    with open(file_name) as f:
      st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
  except Exception:
    pass


local_css("style.css")

# --- HEADER SECTION ---
st.markdown(
    """
    <div class="header-container">
        <h1>🌐 AI Language Translation Tool</h1>
        <p>CodeAlpha AI Internship — Professional Task 1 Submission</p>
    </div>
""",
    unsafe_allow_html=True,
)

language_names = list(LANGUAGES.keys())

# --- SIDEBAR FOR LANGUAGE PREFERENCES (LEFT SIDE) ---
with st.sidebar:
  st.markdown("### ⚙️ Language Settings")
  source_options = ["Select Source Language..."] + language_names
  source_lang = st.selectbox(
      "📤 Source Language:", source_options, index=0, key="src_sel"
  )

  target_options = ["Select Target Language..."] + language_names
  target_lang = st.selectbox(
      "📥 Target Language:", target_options, index=0, key="tgt_sel"
  )
  st.markdown("---")
  st.info(
      "Tip: Select your source and target languages here, then translate in the"
      " main panel."
  )

# --- MAIN PANEL FOR TEXT INPUT & OUTPUT ---
st.markdown("### ✍️ Enter Content to Translate")
text_to_translate = st.text_area(
    "Type or paste your text below:",
    placeholder="Write or paste your text here...",
    height=140,
    label_visibility="collapsed",
)

st.markdown("<br>", unsafe_allow_html=True)

# --- TRANSLATION LOGIC ---
if st.button("🚀 Translate Text Now"):
  if source_lang == "Select Source Language...":
    st.warning("⚠️ Please select a valid Source Language in the sidebar!")
  elif target_lang == "Select Target Language...":
    st.warning("⚠️ Please select a valid Target Language in the sidebar!")
  elif not text_to_translate.strip():
    st.warning("⚠️ Please enter some text to translate!")
  else:
    with st.spinner("🔄 Translating your text... Please wait."):
      try:
        src_code = (
            LANGUAGES[source_lang] if source_lang in LANGUAGES else "en-GB"
        )
        tgt_code = LANGUAGES[target_lang]

        # Translation Execution
        translator = MyMemoryTranslator(source=src_code, target=tgt_code)
        translated_text = translator.translate(text_to_translate)

        if translated_text:
          st.markdown("---")
          st.success("✨ Translation Completed Successfully!")

          st.markdown("### 🎯 Translated Output (with Built-in Copy):")
          # st.code provides output block with a built-in copy button on the top right
          st.code(translated_text, language="text")

          # Audio Feature (Text-to-Speech)
          try:
            tts_lang = src_code.split("-")[0]
            if len(tgt_code.split("-")[0]) == 2:
              tts_lang = tgt_code.split("-")[0]

            tts = gTTS(text=translated_text, lang=tts_lang, slow=False)
            audio_bytes = io.BytesIO()
            tts.write_to_fp(audio_bytes)
            audio_bytes.seek(0)

            st.markdown("### 🔊 Listen to Pronunciation:")
            st.audio(audio_bytes, format="audio/mp3")
          except Exception:
            pass
        else:
          st.error(
              "❌ Translation returned empty response. Please try again."
          )

      except Exception as e:
        st.error(f"❌ Translation Error: {e}")