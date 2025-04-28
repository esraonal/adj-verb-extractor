# Adjective-Verb Extractor

This is a Python tool for extracting adjective-based depictives + verb constructions from Turkish CoNLL-U formatted files. The tool reads `.conllu` files, applies rule-based matching, and outputs tab-separated adjective + verb pairs.


This project is designed to identify patterns such as:
- Bare adjectives preceding verbs (e.g., `yorgun` ("tired"))
- Reduplicated adjectives (e.g., `yavaş yavaş` ("slow slow"))
- Locative modifiers (e.g., `mutlu bir şekilde` ("in a happy way/manner"))
- Converbial forms (e.g., `sert olarak` (as being harsh))

```python
from depictivetr import AdjectiveVerbExtractor

# Load your .conllu file
conllu_path = "path/to/file.conllu"
with open(conllu_path, "r", encoding="utf-8-sig") as f:
    lines = f.readlines()

# Initialize the extractor
extractor = AdjectiveVerbExtractor()
adjective_type = "bare"  # or "reduplication", "locative", "converb"

# Run extraction (optional output_path to write to file)
pairs_text, count = extractor.extract(
    conllu_data=lines,
    adjective_type=adjective_type
    output_path=output_path    # omit to print to stdout
)

# Inspect results
print(pairs_text)
print(f"Number of pairs: {count}")
```

Output example:
```bash
mutlu    ayrıl    
yorgun    yat

Number of pairs: 2
```
