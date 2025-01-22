import stanza
import csv
import os
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

# Download Stanza model for Marathi if not already downloaded
stanza.download('mr')
nlp = stanza.Pipeline('mr', processors='tokenize,pos', use_gpu=True)

# File paths
input_file_path = r'D:\spell checking\POS\fulldataset_dedup_final.txt'
output_file_path = r"D:\spell checking\POS\pos_tagged_dataset.csv"

# Validate file paths
def validate_file_path(file_path, is_input=True):
    if is_input and not os.path.isfile(file_path):
        raise FileNotFoundError(f"Input file not found at {file_path}")
    if not is_input:
        output_dir = os.path.dirname(file_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

try:
    # Validate input and output paths
    validate_file_path(input_file_path, is_input=True)
    validate_file_path(output_file_path, is_input=False)

    logging.info(f"Reading input file: {input_file_path}")

    # Process the input file
    with open(input_file_path, "r", encoding="utf-8") as file, open(output_file_path, "w", encoding="utf-8", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Word", "POS"])  # Write header

        logging.info("Processing file in chunks...")
        chunk_size = 1024 * 1024  # 1 MB chunk size
        buffer = ""

        for chunk in iter(lambda: file.read(chunk_size), ""):
            buffer += chunk
            lines = buffer.splitlines(keepends=True)
            buffer = lines.pop()  # Save incomplete line for the next chunk

            for line in lines:
                line = line.strip()
                if not line:  # Skip empty lines
                    continue
                try:
                    # Process the line with Stanza
                    doc = nlp(line)
                    for sentence in doc.sentences:
                        for word in sentence.words:
                            csvwriter.writerow([word.text, word.upos])
                except Exception as e:
                    logging.error(f"Error processing line: {line}. Skipping. Error: {e}")

        # Process remaining buffer if there's any leftover text
        if buffer.strip():
            try:
                doc = nlp(buffer.strip())
                for sentence in doc.sentences:
                    for word in sentence.words:
                        csvwriter.writerow([word.text, word.upos])
            except Exception as e:
                logging.error(f"Error processing remaining buffer: {buffer}. Skipping. Error: {e}")

        logging.info(f"POS tagging completed and saved to: {output_file_path}")

except FileNotFoundError as fnf_error:
    logging.error(fnf_error)
except UnicodeDecodeError:
    logging.error("Unable to decode the file. Try using a different encoding (e.g., utf-16).")
except Exception as e:
    logging.error(f"An unexpected error occurred: {e}")
