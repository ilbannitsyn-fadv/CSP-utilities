import pyperclip

def read_clipboard_to_csp():
    # Read the raw data from the clipboard
    raw_data = pyperclip.paste()
    
    # Split the data into lines
    lines = raw_data.split('\n')
    
    # Find indices of lines with '+---'
    indices = [i for i, line in enumerate(lines) if '+---' in line]
    
    # Verify that there is an even number of indices (pairs of start and end for blocks)
    if len(indices) % 2 != 0:
        raise ValueError("Mismatched number of block delimiters.")

    # Prepare to build the CSP string
    csp_parts = []

    # Iterate through each pair of indices to process blocks
    for start, end in zip(indices[0::2], indices[1::2]):
        # The second line after the start index contains the directive
        directive = lines[start + 1].strip('| ').strip().strip(' |')
        
        # Gather all valid source lines
        sources = []
        for line in lines[start + 3:end]:  # Start from the line after the '----' and go until the block end
            if line.strip() and not line.strip().startswith('+--'):
                converted_line = line.strip(' |').strip('| ').strip()
               
                if "---" not in converted_line:
                    sources.append(converted_line.strip().strip(' |').strip())
        
        # Combine directive with sources to form part of the CSP string
        csp_parts.append(f"{directive} {' '.join(sources)}")

    # Join all parts into a single CSP string with semicolons
    csp_string = '; '.join(csp_parts) + ';'
    
    return csp_string

# Generate CSP string from clipboard data
csp_string = read_clipboard_to_csp()

# Output the CSP string
print(csp_string)

# Optional: Copy the CSP string back to the clipboard
pyperclip.copy(csp_string)
