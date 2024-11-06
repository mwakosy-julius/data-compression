import streamlit as st
import os
import tempfile
import base64
import re
from collections import defaultdict

reference = "ACGTCGTA" 
sequence = "ACGCCTAA"

def delta_compress(sequence, reference):
    """Delta compress by encoding differences from the reference sequence."""
    if not reference:
        raise ValueError("Reference sequence is required for delta compression.")
    differences = []
    for i, (ref_base, seq_base) in enumerate(zip(reference, sequence)):
        if ref_base != seq_base:
            differences.append(f"{i}:{seq_base}")
    return '|'.join(differences)

def delta_decompress(compressed):
    """Decompress a sequence delta-encoded against the reference."""
    sequence = list(reference)
    for diff in compressed.split('|'):
        if diff:
            pos, base = diff.split(':')
            sequence[int(pos)] = base
    return ''.join(sequence)

# compressor = delta_compress(sequence, reference)
# print(compressor)
# decompressor = delta_decompress(compressor)
# print(decompressor)

st.title("Genomic Delta Compression Tool")

st.write("Upload a genomic file to compress it.")

uploaded_file = st.file_uploader("Choose a file", type=["txt", "fasta", "fa", "fastq"], key='sequence_file')
if uploaded_file is not None:
    sequence = uploaded_file.read().decode('utf-8').upper()

st.write("Upload a reference file for compression.")

reference_file = st.file_uploader("Choose a file", type=["txt", "fasta", "fa", "fastq"], key='reference_file')
if reference_file is not None:
    reference = reference_file.read().decode('utf-8').upper()

if uploaded_file and reference_file is not None:
    st.write("File details:")
    st.write(f"Filename: {uploaded_file.name}")
    st.write(f"File type: {uploaded_file.type}")
    st.write(f"File size: {uploaded_file.size} bytes")

    compressed_data = delta_compress(sequence, reference)

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