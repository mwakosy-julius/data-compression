import streamlit as st
from collections import Counter
import tempfile
import os

def read_fasta(aligned_sequence):
    sequences = []
    sequence = ""

    for line in aligned_sequence.splitlines():
        line = line.strip()
        if line.startswith(">"):
            if sequence:  
                sequences.append(sequence)
                sequence = ""
        else:
            sequence += line
    if sequence:  
        sequences.append(sequence)
    return sequences

def generate_consensus(sequences):
    consensus_sequence = ""
    sequence_length = len(sequences[0])

    for i in range(sequence_length):
        column = [seq[i] for seq in sequences]
        # column = [seq[i] for seq in sequences if seq[i] != '-']
        # if column:
        #     most_common = Counter(column).most_common(1)[0][0]
        #     consensus_sequence += most_common
        # else:
        #     consensus_sequence += "-"
        most_common_nucleotide = Counter(column).most_common(1)[0][0]
        consensus_sequence += most_common_nucleotide

    return consensus_sequence


st.title("Genomic Consensus Generator")

st.write("Upload a fasta aligned file.")

uploaded_file = st.file_uploader("Choose a file", type=["txt", "fasta", "fa", "fastq"], key='sequence_file')
if uploaded_file is not None:
    aligned_sequence = uploaded_file.read().decode('utf-8')
    sequences = read_fasta(aligned_sequence)

    if all(len(seq) == len(sequences[0]) for seq in sequences):
        consensus_sequence = generate_consensus(sequences)

        st.write(consensus_sequence)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".consensus") as tmp_file:
                tmp_file.write(consensus_sequence.encode())
                tmp_file_path = tmp_file.name

        with open(tmp_file_path, "rb") as f:
            st.download_button(
                label="Download consensus sequence",
                data=f,
                file_name="consensus_" + uploaded_file.name,
                mime="application/octet-stream"
            )
        os.remove(tmp_file_path)

