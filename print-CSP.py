import pandas as pd
from tabulate import tabulate
import pyperclip

# Function to split dictionary into chunks with a maximum of 3 items per chunk
def chunk_dict(data, size):
    it = iter(data)
    for _ in range(0, len(data), size):
        yield {k: data[k] for k in [next(it) for _ in range(size) if _ < len(data)]}

# Read CSP string from clipboard
csp_string = pyperclip.paste()

if not csp_string:
    print("Clipboard is empty or does not contain a valid CSP string.")
else:
    directives = [directive.strip() for directive in csp_string.split(';') if directive.strip()]
    csp_dict = {}
    # sort directives alphabetically
    directives = sorted(directives)
    for directive in directives:
        parts = directive.split(None, 1)
        if len(parts) > 1:
            property_name = parts[0]
            values = parts[1].split()
            csp_dict[property_name] = values

    # Break the dictionary into chunks of 3
    chunked_dicts = list(chunk_dict(csp_dict, 1))

    # Process each chunk and print formatted tables
    tables = []
    for chunk in chunked_dicts:
        df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in chunk.items()])).fillna('')
        formatted_table = tabulate(df, headers='keys', tablefmt='psql', showindex=False)
        tables.append(formatted_table)
        print(formatted_table)

    # Copy the first formatted table to clipboard as an example
    giant_string = '\n\n'.join(tables)
    pyperclip.copy(giant_string)
    print("The first formatted CSP table chunk has been copied to the clipboard.")
