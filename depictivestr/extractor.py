
class AdjectiveVerbExtractor:
    def __init__(self, pairs=[], pairs_text="", count=0):
        self.pairs = pairs
        self.pairs_text = pairs_text
        self.count = count

    def extract(self, conllu_data, adjective_type, output_path=None):
        parsed_data = self._parse_conllu(data=conllu_data)
        
        for entry in parsed_data:
            columns = entry["curr"]
            prev_columns = entry["prev"]
            next_columns = entry["next"]

            try:
                if adjective_type == 'bare':
                    self._handle_bare(columns, prev_columns, next_columns)

                elif adjective_type == 'reduplication':
                    self._handle_reduplication(columns, prev_columns, next_columns)

                elif adjective_type == 'locative':
                    self._handle_locative(columns, prev_columns, next_columns, conllu_data)

                elif adjective_type == 'converb':
                    self._handle_converb(columns, next_columns, conllu_data)

            except (IndexError, ValueError):
                continue

        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(self.pairs_text)
            print(f"Output written to: {output_path}")
        else:
            print(f"Number of pairs: {self.count}\n")
            print("ADJ\tVERB")
            print(self.pairs_text)
        return self.pairs_text, self.count
    
    def _parse_conllu(self, data):
        parsed = []
        current_sentence = ""
        
        for i in range(1, len(data) - 1):
            line = data[i]

            if data[i].startswith("# text = "):
                current_sentence = data[i].strip()

            if data[i].startswith("#") or data[i] == '\n':
                continue

            try:
                prev_line = data[i - 1]
                next_line = data[i + 1]
                if prev_line.startswith("#") or prev_line == '\n':
                    continue
                if next_line.startswith("#") or next_line == '\n':
                    continue

                parsed.append({
                    "index": i,
                    "sentence": current_sentence,
                    "prev": prev_line.strip().split('\t'),
                    "curr": line.strip().split('\t'),
                    "next": next_line.strip().split('\t')
                })
            except IndexError:
                continue

        return parsed


    def _add_pair(self, pair_str):
        if pair_str not in self.pairs:
            self.pairs.append(pair_str)
            self.pairs_text += pair_str
            self.count += 1

    def _handle_bare(self, columns, prev_columns, next_columns, conllu_lines):
        if columns[1].lower() != prev_columns[1].lower() and \
            columns[4] == 'Adj' and \
            next_columns[4] == 'Verb' and next_columns[3] == 'VERB' and \
            next_columns[2] not in ['ol', 'bul', 'et', 'görün', 'say'] and \
            columns[1].lower() not in ['iyi', 'ilk', 'çok'] and \
            len(columns[1]) > 1:
            
            head_id = next_columns[6]
            head = self._find_token_by_id(head_id, conllu_lines)
            if head and head[3] == 'VERB':
                self._add_pair(f"{columns[1].lower()}\t{next_columns[2]}\n")

    def _handle_reduplication(self, columns, prev_columns, next_columns, conllu_lines):
        if columns[7] == 'compound:redup' and \
            columns[1].lower() == prev_columns[1].lower() and \
            columns[4] == 'Adj' and \
            next_columns[4] == 'Verb' and next_columns[3] == 'VERB' and \
            next_columns[2] not in ['ol', 'bul', 'et', 'görün', 'say'] and \
            columns[1].lower() not in ['iyi', 'ilk', 'çok'] and \
            len(columns[1]) > 1:

            head_id = next_columns[6]
            head = self._find_token_by_id(head_id, conllu_lines)
            if head and head[3] == 'VERB':
                self._add_pair(f"{prev_columns[1].lower()} {columns[1].lower()}\t{next_columns[2]}\n")

    def _handle_locative(self, columns, prev_columns, next_columns, conllu_lines):
        loc_words = ['şekilde', 'halde', 'biçimde']
        if next_columns[1].lower() not in loc_words:
            return

        head_id = next_columns[6]  # ID of the verb that 'şekilde' depends on
        if columns[4] == 'Adj':
            verb = self._find_token_by_id(head_id, conllu_lines)
            if verb:
                self._add_pair(f"{columns[1].lower()}\t{next_columns[1].lower()}\t{verb}\n")

        elif prev_columns[4] == 'Adj' and columns[1].lower() == 'bir':
            verb = self._find_token_by_id(head_id, conllu_lines)
            if verb:
                self._add_pair(f"{prev_columns[1].lower()} {columns[1].lower()}\t{next_columns[1].lower()}\t{verb}\n")

    def _handle_converb(self, columns, next_columns, conllu_lines):
        if columns[4] == 'Adj' and next_columns[1].lower() == 'olarak':
            head_id = next_columns[6]
            verb = self._find_token_by_id(head_id, conllu_lines)
            if verb:
                self._add_pair(f"{columns[1].lower()}\t{next_columns[1].lower()}\t{verb}\n")

    def _find_token_by_id(self, token_id, lines):
        for line in lines:
            if line.startswith("#") or line.strip() == '':
                continue
            token = line.strip().split('\t')
            if len(token) > 6 and token[0] == token_id and token[3] == 'VERB':
                return token[2]
        return None