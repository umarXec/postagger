import re
import os
import time
from collections import defaultdict
from nltk.tokenize import word_tokenize

# --------------------------------------------
# Step 1: Rule-Based POS Tagging (Marathi)
# --------------------------------------------

def rule_based_marathi_pos(word):
    rules = [
        (r'(णे|तात|तो|ली|विणे)$', 'VERB'),
        (r'(ता|कार|वाडी|पणा|य|ने|नी)$', 'NOUN'),
        (r'(रे|ई|ीत|िक|ी)$', 'ADJ'),
        (r'(पणे|खूप|सरळ|वर|आत)$', 'ADV'),
        (r'(चा|ची|चे|ला|ने|ही)$', 'POST'),
        (r'(आहे|आहोत|असेल)$', 'AUX'),
        (r'[०-९]+', 'NUM'),
        (r'(आणि|पण|म्हणून|की)$', 'CONJ'),
    ]
    for pattern, tag in rules:
        if re.search(pattern, word):
            return tag
    return 'UNK'  # Default for unknown words

# --------------------------------------------
# Step 2: Load Data & Tagging
# --------------------------------------------

def read_dataset(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        sentences = [line.strip() for line in f if line.strip()]
    return [word_tokenize(sent) for sent in sentences]

def tag_sentences(sentences):
    tagged_sentences = []
    pos_stats = defaultdict(set)  # Track word -> possible tags
    for sent in sentences:
        tags = []
        for word in sent:
            tag = rule_based_marathi_pos(word)
            pos_stats[word].add(tag)
            tags.append(tag)
        tagged_sentences.append(tags)
    return tagged_sentences, pos_stats

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
    print(f"Words with Conflicting Tags: {len(conflicts)}")
    if conflicts:
        print("\nExample Conflicts:")
        for word, tags in list(conflicts.items())[:5]:  # Show first 5 conflicts
            print(f"{word}: {', '.join(tags)}")

def save_tagged_file(sentences, tagged_sentences, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for sent, tags in zip(sentences, tagged_sentences):
            for word, tag in zip(sent, tags):
                f.write(f"{word}\t{tag}\n")
            f.write("\n")

# --------------------------------------------
# Main Execution
# --------------------------------------------

if __name__ == "__main__":
    start_time = time.time()
    
    # File paths (update these)
    input_file = r"C:\Users\umarx\OneDrive\Desktop\pos\data\split_parts_part1_2\part1.txt"
    output_file = "pos_tags.txt"

    try:
        # 1. Read sentences
        sentences = read_dataset(input_file)
        if not sentences:
            raise ValueError("Input file is empty or formatted incorrectly.")
        
        # 2. Perform tagging
        tagged_sentences, pos_stats = tag_sentences(sentences)
        
        # 3. Save tagged dataset
        save_tagged_file(sentences, tagged_sentences, output_file)
        print(f"Tagged dataset saved to: {os.path.abspath(output_file)}")
        
        # 4. Print statistics
        print_stats(pos_stats)
        
    except Exception as e:
        print(f"Error: {e}")
    
    # Track execution time
    print(f"\nExecution Time: {time.time() - start_time:.2f} seconds")