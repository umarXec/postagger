import os
import time
import stanza
from collections import defaultdict

# Download the Marathi model if not already installed
# stanza.download('mr')  # Uncomment this line if running for the first time

# --------------------------------------------
# Step 1: Initialize Stanza Pipeline for Marathi
# --------------------------------------------

def initialize_stanza():
    try:
        nlp = stanza.Pipeline(
            lang='mr',  # Marathi language
            processors='tokenize,pos',  # Tokenization and POS tagging
            tokenize_pretokenized=False  # Let Stanza handle tokenization
        )
        return nlp
    except:
        raise Exception("Marathi model not found. Run `stanza.download('mr')` first.")

# --------------------------------------------
# Step 2: Load Data & Perform POS Tagging
# --------------------------------------------

def read_dataset(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        sentences = [line.strip() for line in f if line.strip()]
    return sentences

def tag_sentences(nlp, sentences):
    pos_stats = defaultdict(set)  # Track word -> possible tags across sentences
    tagged_data = []

    for sent in sentences:
        doc = nlp(sent)
        words = []
        tags = []
        for sentence in doc.sentences:
            for word in sentence.words:
                words.append(word.text)
                tags.append(word.pos)
                pos_stats[word.text].add(word.pos)
        tagged_data.append((words, tags))
    
    return tagged_data, pos_stats

# --------------------------------------------
# Step 3: Generate Statistics & Save Output
# --------------------------------------------

def print_stats(pos_stats):
    total_words = sum(len(tags) for word, tags in pos_stats.items())
    unique_pos = set(tag for tags in pos_stats.values() for tag in tags)
    conflicts = {word: tags for word, tags in pos_stats.items() if len(tags) > 1}
    
    print("\n=== POS Tagging Statistics ===")
    print(f"Total Words Processed: {total_words}")
    print(f"Unique POS Tags Found: {len(unique_pos)} ({', '.join(unique_pos)})")
    print(f"Words with Contextual Conflicts: {len(conflicts)}")
    if conflicts:
        print("\nExample Conflicts (same word, different tags):")
        for word, tags in list(conflicts.items())[:5]:
            print(f"{word}: {', '.join(tags)}")

def save_tagged_file(tagged_data, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for words, tags in tagged_data:
            for word, tag in zip(words, tags):
                f.write(f"{word}\t{tag}\n")
            f.write("\n")

# --------------------------------------------
# Main Execution
# --------------------------------------------

if __name__ == "__main__":
    start_time = time.time()

    # File paths (update these)
    input_file = r'C:\Users\umarx\OneDrive\Desktop\pos\data\split_parts_part1_2\part1.txt'
    output_file = "pos_tags_stanza.txt"

    try:
        # 1. Initialize Stanza
        nlp = initialize_stanza()
        
        # 2. Read sentences
        sentences = read_dataset(input_file)
        if not sentences:
            raise ValueError("Input file is empty or formatted incorrectly.")
        
        # 3. Perform POS tagging
        tagged_data, pos_stats = tag_sentences(nlp, sentences)
        
        # 4. Save tagged dataset
        save_tagged_file(tagged_data, output_file)
        print(f"Tagged dataset saved to: {os.path.abspath(output_file)}")
        
        # 5. Print statistics
        print_stats(pos_stats)

    except Exception as e:
        print(f"Error: {e}")

    # Track execution time
    print(f"\nExecution Time: {time.time() - start_time:.2f} seconds")