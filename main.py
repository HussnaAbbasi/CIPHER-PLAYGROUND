import streamlit as st

st.markdown(
    """
    <style>
    /* Background color */
    .stApp {
        background-color: #071e17;
    }

    /* Text color */
    html, body, [class*="css"]  {
        color: white !important;
    }

    /* Input boxes */
    .stTextInput textarea, .stTextArea textarea, .stNumberInput input {
        background-color: #697452 !important;
        color: white !important;
        border-radius: 8px;
        padding: 8px;
    }

    /* Buttons */
    div.stButton > button:first-child {
        background-color: #944131 !important;
        color: white !important;
        border-radius: 12px;
        padding: 10px 20px;
        font-weight: bold;
        border: none;
    }
    div.stButton > button:hover {
        background-color: #732f23 !important; /* darker hover */
        color: #f0f0f0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

import string
def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - start + shift) % 26 + start)
        else:
            result += char
    return result
def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)
def vigenere_encrypt(text, key):
    result = ""
    key = key.lower()
    key_index = 0
    for char in text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('a')
            start = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - start + shift) % 26 + start)
            key_index += 1
        else:
            result += char
    return result
def vigenere_decrypt(text, key):
    result = ""
    key = key.lower()
    key_index = 0
    for char in text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('a')
            start = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - start - shift) % 26 + start)
            key_index += 1
        else:
            result += char
    return result
def generate_playfair_matrix(key):
    key = key.lower().replace("j", "i")
    matrix = []
    used = set()
    for c in key + string.ascii_lowercase:
        if c not in used and c.isalpha():
            matrix.append(c)
            used.add(c)
    return [matrix[i*5:(i+1)*5] for i in range(5)]

def playfair_process_text(text):
    text = text.lower().replace("j", "i")
    pairs = []
    i = 0
    while i < len(text):
        a = text[i]
        if not a.isalpha():
            i += 1
            continue
        b = ''
        if i+1 < len(text):
            b = text[i+1]
        if not b.isalpha() or a == b:
            b = 'x'
            i += 1
        else:
            i += 2
        pairs.append((a, b))
    if len(pairs[-1]) == 1:  
        pairs[-1] = (pairs[-1][0], 'x')
    return pairs
def playfair_encrypt(text, key):
    matrix = generate_playfair_matrix(key)
    pairs = playfair_process_text(text)
    result = []
    for a, b in pairs:
        pos_a = [(r, c) for r in range(5) for c in range(5) if matrix[r][c] == a][0]
        pos_b = [(r, c) for r in range(5) for c in range(5) if matrix[r][c] == b][0]
        if pos_a[0] == pos_b[0]:  # same row
            result.append(matrix[pos_a[0]][(pos_a[1]+1)%5])
            result.append(matrix[pos_b[0]][(pos_b[1]+1)%5])
        elif pos_a[1] == pos_b[1]:  # same col
            result.append(matrix[(pos_a[0]+1)%5][pos_a[1]])
            result.append(matrix[(pos_b[0]+1)%5][pos_b[1]])
        else:  
            result.append(matrix[pos_a[0]][pos_b[1]])
            result.append(matrix[pos_b[0]][pos_a[1]])
    return ''.join(result).upper()
def playfair_decrypt(text, key):
    matrix = generate_playfair_matrix(key)
    text = text.lower().replace("j", "i")
    pairs = [(text[i], text[i+1]) for i in range(0, len(text), 2)]
    result = []
    for a, b in pairs:
        pos_a = [(r, c) for r in range(5) for c in range(5) if matrix[r][c] == a][0]
        pos_b = [(r, c) for r in range(5) for c in range(5) if matrix[r][c] == b][0]
        if pos_a[0] == pos_b[0]:  # same row
            result.append(matrix[pos_a[0]][(pos_a[1]-1)%5])
            result.append(matrix[pos_b[0]][(pos_b[1]-1)%5])
        elif pos_a[1] == pos_b[1]:  # same col
            result.append(matrix[(pos_a[0]-1)%5][pos_a[1]])
            result.append(matrix[(pos_b[0]-1)%5][pos_b[1]])
        else:  
            result.append(matrix[pos_a[0]][pos_b[1]])
            result.append(matrix[pos_b[0]][pos_a[1]])
    return ''.join(result).upper()
st.title("CIPHER PLAYGROUND")
cipher_choice = st.selectbox("Choose a Cipher:", ["Caesar", "Vigenère", "Playfair"])
mode = st.radio("Choose Mode:", ["Encrypt", "Decrypt"])
text = st.text_area("Enter your text:")
if cipher_choice == "Caesar":
    shift = st.slider("Choose shift value", 0, 25, 3)
    if st.button("Run"):
        result = caesar_encrypt(text, shift) if mode == "Encrypt" else caesar_decrypt(text, shift)
        st.subheader("Result")
        st.code(result)
elif cipher_choice == "Vigenère":
    key = st.text_input("Enter key (letters only)", value="lemon")
    if st.button("Run"):
        result = vigenere_encrypt(text, key) if mode == "Encrypt" else vigenere_decrypt(text, key)
        st.subheader("Result")
        st.code(result)
else: 
    key = st.text_input("Enter Playfair key", value="keyword")
    if st.button("Run"):
        result = playfair_encrypt(text, key) if mode == "Encrypt" else playfair_decrypt(text, key)
        st.subheader("Result")
        st.code(result)