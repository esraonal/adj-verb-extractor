# Adjective-Verb Extractor

This is a Python tool for extracting adjective-based depictives + verb constructions from Turkish CoNLL-U formatted files.

This project is designed to identify patterns such as:
- Bare adjectives preceding verbs (e.g., `yorgun uyudu`)
- Reduplicated adjectives (e.g., `yavaş yavaş yürüdü`)
- Locative modifiers (e.g., `mutlu bir şekilde konuştu`)
- Converbial forms (e.g., `sert olarak eleştirdi`)

```bash
from depictivetr import AdjectiveVerbExtractor

# Load your .conllu file
conllu_path = "path/to/file.conllu"
with open(conllu_path, "r", encoding="utf-8-sig") as f:
    lines = f.readlines()

# Initialize and run the extractor
extractor = AdjectiveVerbExtractor()
adjective_type = "bare"  # or "reduplication", "locative", "converb"
output_path = "output.txt"

pairs_text, count = extractor.extract(
    conllu_data=lines,
    adjective_type=adjective_type
)
```
The tool reads `.conllu` files, applies rule-based matching, and outputs tab-separated adjective + verb pairs.
