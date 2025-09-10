import random

class Genome:
    def __init__(self):
        # universal amino acid dictionary
        self.aminoacid_dict = {
            'UUC':'F','UUU':'F','UUA':'L','UUG':'L','CUU':'L','CUC':'L','CUA':'L','CUG':'L',
            'AUU':'I','AUC':'I','AUA':'I','AUG':'M','GUU':'V','GUC':'V','GUA':'V','GUG':'V',
            'UCU':'S','UCC':'S','UCA':'S','UCG':'S','AGU':'S','AGC':'S','CCU':'P','CCC':'P','CCA':'P','CCG':'P',
            'ACU':'T','ACC':'T','ACA':'T','ACG':'T','GCU':'A','GCC':'A','GCA':'A','GCG':'A',
            'UAU':'Y','UAC':'Y','CAU':'H','CAC':'H','CAA':'Q','CAG':'Q',
            'AAU':'N','AAC':'N','AAA':'K','AAG':'K','GAU':'D','GAC':'D','GAA':'E','GAG':'E',
            'UGU':'C','UGC':'C','UGG':'W','CGU':'R','CGC':'R','CGA':'R','CGG':'R','AGA':'R','AGG':'R',
            'GGU':'G','GGC':'G','GGA':'G','GGG':'G',
            'UAA':'Stop','UGA':'Stop','UAG':'Stop'
        }

    def generate_ssDNA(self, length):
        """Generate a random single-stranded DNA sequence"""
        return ''.join(random.choice("ATGC") for _ in range(length))

    def generate_rna(self, length):
        """Generate a random RNA sequence"""
        return ''.join(random.choice("AUGC") for _ in range(length))

    def complementary_DNA_strand(self, dna):
        """Generate complementary strand"""
        mapping = str.maketrans("ATGC", "TACG")
        return dna.upper().translate(mapping)

    def check_DNA(self, seq1, seq2):
        """Check complementarity"""
        if len(seq1) >= len(seq2):
            strand2 = seq2[::-1]  # reverse
            strand2_check = seq1.translate(str.maketrans("ACTG", "TGAC"))
            return strand2 in strand2_check
        else:
            strand1 = seq1[::-1]
            strand1_check = seq2.translate(str.maketrans("ACTG", "TGAC"))
            return strand1 in strand1_check

    def six_reading_frames(self, seq1, rseq2):
        """Return six reading frames for DNA and its reverse complement"""
        output = []

        # forward frames
        f1 = ' '.join([seq1[i:i+3] for i in range(0, len(seq1), 3)])
        f2 = ' '.join([seq1[i:i+3] for i in range(1, len(seq1)-2, 3)])
        f3 = ' '.join([seq1[i:i+3] for i in range(2, len(seq1)-2, 3)])
        output.append("\n".join([f1, f2, f3]))

        # reverse complement frames
        r1 = ' '.join([rseq2[i:i+3] for i in range(0, len(rseq2), 3)])
        r2 = ' '.join([rseq2[i:i+3] for i in range(1, len(rseq2)-2, 3)])
        r3 = ' '.join([rseq2[i:i+3] for i in range(2, len(rseq2)-2, 3)])
        output.append("\n".join([r1, r2, r3]))

        return output

    def translate_with_frame(self, dna, frames=[1,2,3,-1,-2,-3]):
        """Translate DNA sequence into protein sequences for given frames"""
        if not dna:
            return ["" for _ in frames]

        def to_rna(seq): return seq.replace('T', 'U')

        forward = [to_rna(dna[i:]) for i in range(3)]
        reverse = [to_rna(self.complementary_DNA_strand(dna[::-1])[i:]) for i in range(3)]

        translations = []
        for seq in forward + reverse:
            codons = [seq[i:i+3] for i in range(0, len(seq)-2, 3)]
            aa_seq = ''.join(self.aminoacid_dict.get(c, '') for c in codons)
            translations.append(aa_seq)

        frame_map = {1:0, 2:1, 3:2, -1:3, -2:4, -3:5}
        return [translations[frame_map[f]] for f in frames]

    def dna_to_rna(self, dna):
        """Convert DNA to RNA"""
        return dna.replace("T", "U")

    def protein(self, rna):
        """Convert RNA to protein sequence"""
        codons = [rna[i:i+3] for i in range(0, len(rna)-2, 3)]
        return ''.join(self.aminoacid_dict.get(c, '') for c in codons)


# Example usage
if __name__ == "__main__":
    g = Genome()
    dna = g.generate_ssDNA(21)
    comp = g.complementary_DNA_strand(dna)
    print("DNA:", dna)
    print("Complement:", comp)
    print("Frames:", g.six_reading_frames(dna, comp))
    print("Translation:", g.translate_with_frame(dna))
    print("RNA:", g.dna_to_rna(dna))
    print("Protein:", g.protein(g.dna_to_rna(dna)))
