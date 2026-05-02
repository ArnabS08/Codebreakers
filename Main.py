import streamlit as st
import io

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(page_title="cipher_tool", page_icon="🔐", layout="centered")

# ── Custom CSS (mirrors the widget design) ─────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Syne:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
}

/* Header */
.cipher-header {
    display: flex;
    align-items: baseline;
    gap: 12px;
    border-bottom: 0.5px solid #ddd;
    padding-bottom: 1rem;
    margin-bottom: 1.5rem;
}
.cipher-header h1 {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 26px;
    font-weight: 600;
    letter-spacing: -0.5px;
    margin: 0;
}
.cipher-header span {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 13px;
    color: #888;
}

/* Stats row */
.stats-row {
    display: flex;
    gap: 10px;
    margin-top: 10px;
    margin-bottom: 4px;
}
.stat-box {
    flex: 1;
    background: #f5f5f3;
    border-radius: 8px;
    padding: 8px 10px;
    text-align: center;
}
.stat-val {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 16px;
    font-weight: 500;
    color: #1a1a1a;
}
.stat-lbl {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    color: #999;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

/* Result preview */
.result-card {
    border: 0.5px solid #97C459;
    border-radius: 12px;
    padding: 1.25rem;
    background: #EAF3DE;
    margin-top: 1rem;
}
.result-card.decrypt {
    border-color: #85B7EB;
    background: #E6F1FB;
}
.result-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #3B6D11;
    margin-bottom: 8px;
}
.result-card.decrypt .result-label {
    color: #185FA5;
}
.preview-box {
    background: white;
    border: 0.5px solid #ddd;
    border-radius: 8px;
    padding: 12px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    color: #1a1a1a;
    max-height: 120px;
    overflow-y: auto;
    white-space: pre-wrap;
    word-break: break-all;
    line-height: 1.6;
    margin-bottom: 10px;
}

/* Streamlit overrides */
.stRadio > div { gap: 8px; }
div[data-testid="stFileUploader"] { margin-bottom: 0; }
</style>
""", unsafe_allow_html=True)


# ── Cipher logic ───────────────────────────────────────────────────────────────
def caesar_cipher(text: str, shift: int, mode: str = "encrypt") -> str:
    if mode not in ("encrypt", "decrypt"):
        raise ValueError("mode must be 'encrypt' or 'decrypt'")
    direction = 1 if mode == "encrypt" else -1
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('a') if char.islower() else ord('A')
            shifted = (ord(char) - base + direction * shift) % 26 + base
            result += chr(shifted)
        else:
            result += char
    return result


def vigenere_cipher(text: str, password: str, mode: str = "encrypt") -> str:
    if mode not in ("encrypt", "decrypt"):
        raise ValueError("mode must be 'encrypt' or 'decrypt'")
    direction = 1 if mode == "encrypt" else -1
    password = password.lower()
    pw_len = len(password)
    pw_idx = 0
    result = ""
    for char in text:
        if char.isalpha():
            shift = ord(password[pw_idx % pw_len]) - ord('a')
            base = ord('a') if char.islower() else ord('A')
            shifted = (ord(char) - base + direction * shift) % 26 + base
            result += chr(shifted)
            pw_idx += 1
        else:
            result += char
    return result


# ── UI ─────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="cipher-header">
  <h1>cipher_tool</h1>
  <span>caesar · vigenère</span>
</div>
""", unsafe_allow_html=True)

# Cipher type tabs
cipher_type = st.radio(
    "Cipher",
    ["Caesar", "Vigenère"],
    horizontal=True,
    label_visibility="collapsed"
)

# Mode
mode = st.radio(
    "Mode",
    ["Encrypt", "Decrypt"],
    horizontal=True,
    label_visibility="collapsed"
)
mode_key = mode.lower()

st.divider()

# File upload
uploaded = st.file_uploader("Input file", type=["txt"], label_visibility="visible")

file_text = None
if uploaded:
    file_text = uploaded.read().decode("utf-8")
    letters = sum(1 for c in file_text if c.isalpha())
    lines = file_text.count('\n') + 1
    st.markdown(f"""
    <div class="stats-row">
        <div class="stat-box"><div class="stat-val">{len(file_text):,}</div><div class="stat-lbl">chars</div></div>
        <div class="stat-box"><div class="stat-val">{lines:,}</div><div class="stat-lbl">lines</div></div>
        <div class="stat-box"><div class="stat-val">{letters:,}</div><div class="stat-lbl">letters</div></div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Cipher parameters
error = None
param_ok = False

if cipher_type == "Caesar":
    shift = st.number_input("Shift amount (1–25)", min_value=1, max_value=25, value=3, step=1)
    param_ok = True
else:
    keyword = st.text_input("Keyword", placeholder="e.g. SECRET")
    keyword = ''.join(c for c in keyword if c.isalpha())
    if keyword:
        param_ok = True
    else:
        st.caption("Letters only — numbers and symbols are removed automatically.")

# Run button
run = st.button(
    f"{'Encrypt' if mode_key == 'encrypt' else 'Decrypt'} →",
    disabled=(file_text is None or not param_ok),
    use_container_width=True,
    type="primary"
)

# ── Process & output ───────────────────────────────────────────────────────────
if run and file_text is not None:
    base_name = uploaded.name.replace(".txt", "")
    suffix = "Ciphered" if mode_key == "encrypt" else "Deciphered"

    if cipher_type == "Caesar":
        result_text = caesar_cipher(file_text, shift, mode_key)
        out_name = f"Caesar_{suffix}_{base_name}.txt"
    else:
        result_text = vigenere_cipher(file_text, keyword, mode_key)
        out_name = f"Vigenere_{suffix}_{base_name}.txt"

    # Preview (first 300 chars)
    preview = result_text[:300] + ("\n…" if len(result_text) > 300 else "")
    card_class = "decrypt" if mode_key == "decrypt" else ""
    label = "Decrypted output" if mode_key == "decrypt" else "Encrypted output"
    out_letters = sum(1 for c in result_text if c.isalpha())

    st.markdown(f"""
    <div class="result-card {card_class}">
        <div class="result-label">{label}</div>
        <div class="preview-box">{preview}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="stats-row" style="margin-top:10px">
        <div class="stat-box"><div class="stat-val">{len(result_text):,}</div><div class="stat-lbl">chars</div></div>
        <div class="stat-box"><div class="stat-val">{out_letters:,}</div><div class="stat-lbl">letters</div></div>
        <div class="stat-box"><div class="stat-val" style="font-size:11px;padding-top:4px">{out_name}</div><div class="stat-lbl">filename</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.download_button(
        label="Download .txt ↓",
        data=result_text.encode("utf-8"),
        file_name=out_name,
        mime="text/plain",
        use_container_width=True,
    )