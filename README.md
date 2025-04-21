# Adjective-Verb Extractor

A lightweight Python tool for extracting adjective + verb constructions from Turkish CoNLL-U formatted files.

This project is designed to identify patterns such as:
- Bare adjectives preceding verbs (e.g., `yorgun uyudu`)
- Reduplicated adjectives (e.g., `yavaş yavaş yürüdü`)
- Locative modifiers (e.g., `mutlu bir şekilde konuştu`)
- Converbial forms (e.g., `sert olarak eleştirdi`)

The tool reads `.conllu` files, applies rule-based matching, and outputs tab-separated adjective + verb pairs.
