import os

# Input file path
input_file = r"C:\Users\umarx\OneDrive\Desktop\pos\split_parts_part1\part1.txt"

# Output directory (will create if it doesn't exist)
output_dir = r'C:\Users\umarx\OneDrive\Desktop\pos\split_parts_part1_2'
os.makedirs(output_dir, exist_ok=True)

# Split Marathi dataset into 10 files
with open(input_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

total_lines = len(lines)
num_parts = 10
lines_per_part = total_lines // num_parts
remainder = total_lines % num_parts

start = 0
for part_num in range(1, num_parts + 1):
    # Calculate end index for this part
    end = start + lines_per_part + (1 if part_num <= remainder else 0)
    part_lines = lines[start:end]
    
    # Create output path
    output_path = os.path.join(output_dir, f'part{part_num}.txt')
    
    # Write to new file
    with open(output_path, 'w', encoding='utf-8') as f_out:
        f_out.writelines(part_lines)
    
    start = end

print(f"Split into {num_parts} files in directory: {output_dir}")