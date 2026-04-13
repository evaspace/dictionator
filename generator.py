import itertools

class DictionaryGenerator:
    def __init__(self, data):
        # Base data sets
        self.words = list(set(w.strip() for w in data.get('words', []) if w.strip()))
        self.animals = list(set(w.strip() for w in data.get('animals', []) if w.strip()))
        self.dates = list(set(d.strip() for d in data.get('dates', []) if d.strip()))
        self.places = list(set(p.strip() for p in data.get('places', []) if p.strip()))
        self.numbers = list(set(n.strip() for n in data.get('numbers', []) if n.strip()))
        
        self.symbols = list(set(data.get('symbols', ["!", "@", "#", "$", "*", "&"])))
        self.conjunctions = list(set(data.get('conjunctions', ["&", "+", "-", "_", "@"])))
        
        # Consolidate bases and ensure uniqueness
        self.all_bases = list(set(self.words + self.animals + self.places))
        self.all_nums = list(set(self.dates + self.numbers))
        
        # Pre-computed transformed bases to save CPU cycles inside inner loops
        self.bases_lower = [w.lower() for w in self.all_bases]
        self.bases_cap = [w.capitalize() for w in self.all_bases]
        self.bases_upper = [w.upper() for w in self.all_bases]
        self.bases_initials = list(set(w[0].upper() for w in self.bases_cap if w))
        
        # Vowel-less bases for linguistic degradation (Locus of control strategy)
        self.bases_no_vowels = list(set(
            "".join([c for c in w.lower() if c not in "aeiouy"]) for w in self.all_bases
        ))
        self.bases_no_vowels = [w for w in self.bases_no_vowels if len(w) > 1]
        
        # High priority keyboard walks and sequences updated from 2024-2025 research
        self.walks = [
            "123", "1234", "12345", "123456", "12345678", "123456789", 
            "qwerty", "azerty", "1234qwer", "qwertz", "qsd",
            "password", "admin", "secret"
        ]
        
        # Specialized leetspeak map
        self.leetspeak_map = {
            'a': ['a', '@', '4'],
            'e': ['e', '3'],
            'i': ['i', '1', '!'],
            'o': ['o', '0'],
            's': ['s', '$', '5'],
            't': ['t', '7']
        }

    def get_leetspeak(self, word):
        """Yields limited leetspeak permutations for a given word."""
        chars = [self.leetspeak_map.get(char, [char]) for char in word.lower()]
        for idx, combo in enumerate(itertools.product(*chars)):
            yield "".join(combo)
            if idx >= 15: # Prevent massive combinatorial explosion per word
                break

    def generate(self, level=10):
        """
        Yields password candidates.
        Designed to rely on itertools to stay efficient and avoid RAM overload.
        Overlaps between levels are acceptable to avoid keeping a multi-gigabyte `seen` set.
        """
        
        # -------------------------------------------------------------
        # LEVEL 1: Top 1% & Fundamentals
        # -------------------------------------------------------------
        for w in self.bases_lower:
            yield w
        for w in self.bases_cap:
            yield w
        for n in self.all_nums:
            yield n
        
        # Very high probability patterns (Word + common digits)
        common_digits = ["1", "123", "123456", "1234"]
        for w, n in itertools.product(self.bases_lower + self.bases_cap, common_digits):
            yield f"{w}{n}"

        if level < 2: return

        # -------------------------------------------------------------
        # LEVEL 2: Corporate Compliance "60% Rule" (Very High Probability 70%+)
        # Word(Cap) + Digits + Symbol
        # -------------------------------------------------------------
        for w, n, s in itertools.product(self.bases_cap, self.all_nums, self.symbols):
            yield f"{w}{n}{s}"

        if level < 3: return

        # -------------------------------------------------------------
        # LEVEL 3: Inversions and Medium Probability Patterns (20%)
        # Word(Cap) + Symbol + Digits & Numbers + Word + Symbol
        # -------------------------------------------------------------
        for walk in self.walks:
            yield walk
            
        for w, s, n in itertools.product(self.bases_cap, self.symbols, self.all_nums):
            yield f"{w}{s}{n}"
            
        for n, w, s in itertools.product(self.all_nums, self.bases_cap, self.symbols):
            yield f"{n}{w}{s}"

        # Shift error: faustinE2026
        for w in self.bases_lower:
            if len(w) > 1:
                shift_w = w[:-1] + w[-1].upper()
                for n in self.all_nums:
                    yield f"{shift_w}{n}"

        if level < 4: return

        # -------------------------------------------------------------
        # LEVEL 4: Composites Simples (Words combined)
        # -------------------------------------------------------------
        # Keyboard walks appended
        for w, walk in itertools.product(self.bases_cap, self.walks):
            yield f"{w}{walk}"
            yield f"{walk}{w}"

        for w1, w2 in itertools.permutations(self.bases_cap, 2):
            yield f"{w1}{w2.lower()}"
            yield f"{w1}{w2}"
            for c in self.conjunctions:
                yield f"{w1}{c}{w2}"

        if level < 5: return

        # -------------------------------------------------------------
        # LEVEL 5: Composites Intimes (Initiales Croisées & Symétrie)
        # -------------------------------------------------------------
        if len(self.bases_initials) >= 2:
            for i1, i2 in itertools.permutations(self.bases_initials, 2):
                for n in self.all_nums:
                    yield f"{i1}{i2}{n}"
                    for c in self.conjunctions:
                        yield f"{i1}{c}{i2}{n}"
        
        # Enveloppement
        for s, w in itertools.product(self.symbols, self.bases_cap):
            yield f"{s}{w}{s}"
        for s, w, n in itertools.product(self.symbols, self.bases_cap, self.all_nums):
            yield f"{s}{w}{n}{s}"

        if level < 6: return

        # -------------------------------------------------------------
        # LEVEL 6: Substitutions Leetspeak Primaires
        # -------------------------------------------------------------
        for w in self.bases_lower:
            for l in self.get_leetspeak(w):
                l_cap = l.capitalize()
                yield l_cap
                for n in self.all_nums:
                    yield f"{l_cap}{n}"
                    for s in self.symbols:
                        yield f"{l_cap}{n}{s}"

        if level < 7: return

        # -------------------------------------------------------------
        # LEVEL 7: Dégradation Linguistique (Élision et Répétition)
        # -------------------------------------------------------------
        for cons in self.bases_no_vowels:
            yield cons.capitalize()
            for n in self.all_nums:
                yield f"{cons.capitalize()}{n}"
                for s in self.symbols:
                    yield f"{cons.capitalize()}{n}{s}"
                    
        # Répétitions complètes
        for w in self.bases_lower:
            for n in self.all_nums:
                yield f"{w}{w}{n}"
                
        # Répétition partielle (doublon de syllabe approx)
        for w in self.bases_lower:
            if len(w) >= 4:
                prefix = w[:3].capitalize()
                yield f"{prefix}{w.capitalize()}"
                for n in self.all_nums:
                    yield f"{prefix}{w.capitalize()}{n}"

        if level < 8: return

        # -------------------------------------------------------------
        # LEVEL 8: Advanced Composites (Numbers embedded)
        # -------------------------------------------------------------
        for w1, w2 in itertools.permutations(self.bases_cap, 2):
            for n in self.all_nums:
                yield f"{w1}{w2}{n}"
                for c in self.conjunctions:
                    yield f"{w1}{c}{w2}{n}"

        if level < 9: return

        # -------------------------------------------------------------
        # LEVEL 9: Hybridation Profonde (Initials + Leetspeak)
        # -------------------------------------------------------------
        if len(self.bases_initials) >= 2:
            for i1, i2 in itertools.permutations(self.bases_initials, 2):
                for n, c, s in itertools.product(self.all_nums, self.conjunctions, self.symbols):
                    yield f"{i1}{c}{i2}{n}{s}"

        for w in self.bases_lower:
            init = w[0].upper()
            for other_w in self.bases_lower:
                if other_w == w: continue
                for l in self.get_leetspeak(other_w):
                    for n in self.all_nums:
                        yield f"{init}{l}{n}"

        if level < 10: return

        # -------------------------------------------------------------
        # LEVEL 10: Hybridation Totale
        # -------------------------------------------------------------
        for w1, w2 in itertools.permutations(self.bases_lower, 2):
            for l1 in self.get_leetspeak(w1):
                l1_cap = l1.capitalize()
                for l2 in self.get_leetspeak(w2):
                    l2_cap = l2.capitalize()
                    for c, n, s in itertools.product(self.conjunctions, self.all_nums, self.symbols):
                        yield f"{l1_cap}{c}{l2_cap}{n}{s}"
