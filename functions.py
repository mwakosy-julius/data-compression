import streamlit as st
import os
import tempfile
import zipfile
import base64
import re

# sequence = 'ACCCTGGAAA'
# sequence = '10111100000111011'

def run_length_encoding(sequence):
    compressed = ''
    count = 1
    for i in range(1, len(sequence)):
        if sequence[i] == sequence[i-1]:
            count += 1
        else:
            compressed += sequence[i-1]
            if count >= 2:
                compressed += str(count)
            count = 1
    compressed += sequence[-1]
    compressed += str(count)
    return compressed

def run_length_decoding(compressed):
    decompressed = ''
    matches = re.findall(r"([A-Z])(\d*)", run)
    print(matches)
    for symbol, count in matches:
        count = int(count) if count else 1
        decompressed += symbol * count
    return decompressed

# def run_length_decoding(compressed):
#     decompressed = ''
#     matches = re.findall(r"([01])(\d)", run)
#     for symbol, count in matches:
#         if count == '0' or count == '1':
#             decompressed += symbol
#             decompressed += count
#         else: 
#             decompressed += symbol * int(count)
#     return decompressed

def encode_sequence(sequence):
        """2-bit encoding of the ACGT nucleotide bases."""
        encoding_map = {'A': '00', 'C': '01', 'G': '10', 'T': '11'}
        encoded_sequence = ''.join(encoding_map.get(base, '00') for base in sequence)
        return encoded_sequence

def decode_sequence(encoded_sequence):
    """Decode 2-bit encoded nucleotide sequence."""
    decoding_map = {'00': 'A', '01': 'C', '10': 'G', '11': 'T'}
    decoded_sequence = ''.join(decoding_map.get(encoded_sequence[i:i+2], 'N') for i in range(0, len(encoded_sequence), 2))
    return decoded_sequence

st.title("Genomic Data Compression Tool")
st.write("Upload a genomic file to compress it.")

uploaded_file = st.file_uploader("Choose a file", type=["txt", "fasta", "fa", "fastq"])
if uploaded_file is not None:
    seq_data = uploaded_file.read().decode('utf-8').upper()

if uploaded_file is not None:
    st.write("File details:")
    st.write(f"Filename: {uploaded_file.name}")
    st.write(f"File type: {uploaded_file.type}")
    st.write(f"File size: {uploaded_file.size} bytes")

    # encoded = encode_sequence(seq_data)

    compressed_data = run_length_encoding(seq_data)
    # st.write(compressed_data)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".compressed") as tmp_file:
        tmp_file.write(compressed_data.encode())
        tmp_file_path = tmp_file.name

    file_size = os.path.getsize(tmp_file_path)
    st.write(f"Compressed File size: {file_size} bytes")

    with open(tmp_file_path, "rb") as f:
        st.download_button(
            label="Download Compressed File",
            data=f,
            file_name="compressed_" + uploaded_file.name,
            mime="application/octet-stream"
        )
    
    os.remove(tmp_file_path)
else:
    st.info("Please upload a file to compress.")