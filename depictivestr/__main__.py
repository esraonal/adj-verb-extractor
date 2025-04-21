#!/usr/bin/env python3

import argparse
from depictivestr import AdjectiveVerbExtractor

def main():
    parser = argparse.ArgumentParser(
        description="Extract adjective + verb constructions from a .conllu file for Turkish."
    )
    parser.add_argument("infile", help="Path to input .conllu file")
    parser.add_argument("type", choices=["bare", "reduplication", "locative", "converb"],
                        help="Type of adjective construction to extract")
    parser.add_argument("-o", "--output", help="Optional path to save output as .txt")
    
    args = parser.parse_args()

    try:
        with open(args.infile, "r", encoding="utf-8-sig") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"❌ File not found: {args.infile}")
        return

    extractor = AdjectiveVerbExtractor()
    output, count = extractor.extract(conllu_data=lines, adjective_type=args.type, full_lines=lines)

    print(f"✅ Done processing {args.infile}")
    print(f"🔢 Number of pairs: {count}")
    print("📋 Extracted pairs:\n")
    print(output)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as out:
            out.write(output)
        print(f"💾 Output written to {args.output}")

if __name__ == "__main__":
    main()
