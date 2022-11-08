require 'complementary_dna'
require 'base_pairs'
require 'dna_sequence_tester'
require 'dna_to_rna'
require 'rna_to_protein_sequence'
require '3_reading_frame'
require '6_reading_frames'

describe 'gene integration' do
    context 'after creating a dna strand' do
        it 'checks if generated strand matches' do
            seq1 = generate_strand(6) 
            seq2 = DNA_strand(seq1).reverse
            expect(check_DNA(seq1, seq2)).to eq(true)
        end
        it 'checks if known strand matches complementary 3 to 5' do
            seq1 = "TGCGATGAATGGGCTCGCTCC"
            expect(DNA_strand(seq1)).to eq('ACGCTACTTACCCGAGCGAGG')
        end
        it 'checks if known strand matches 5 to 3' do
            seq1 = "TGCGATGAATGGGCTCGCTCC"
            expect(DNA_strand(seq1).reverse).to eq("GGAGCGAGCCCATTCATCGCA")
        end
    end

    context 'after creating a double helix' do
        it 'makes dna into mrna' do
            seq1 = "TGCGATGAATGGGCTCGCTCC"
            seq2 = DNA_strand(seq1).reverse
           expect(dna_to_rna(seq1)).to eq('UGCGAUGAAUGGGCUCGCUCC')
           expect(dna_to_rna(seq2)).to eq('GGAGCGAGCCCAUUCAUCGCA')
        end

        it 'turns  RNA strand into aminoacids' do
            seq1 = "TGCGATGAATGGGCTCGCTCC"
            seq2 = DNA_strand(seq1).reverse
            mRNA1 = dna_to_rna(seq1)
            mRNA2 = dna_to_rna(seq2)
            expect(protein(mRNA1)).to eq('CDEWARS') 
            expect(protein(mRNA2)).to eq('GASPFIA') 
        end

        # it 'creates 3 reading frames' do
        #     seq1 = "AGGTGACACCGCAAGCCTTATATTAGC"
        #     seq2 = DNA_strand(seq1).reverse #complementary_dna, reverse for check dna
        #     check_DNA(seq1, seq2)
        #     expect(decompose_single_strand(seq2)).to eq("Frame 1: GCT AAT ATA AGG CTT GCG GTG TCA CCT, Frame 2: G CTA ATA TAA GGC TTG CGG TGT CAC CT, Frame 3: GC TAA TAT AAG GCT TGC GGT GTC ACC T")
            
        # end
        it 'creates 3 reading frames' do
            seq1 = "TGCGATGAATGGGCTCGCTCC"
            seq2 = DNA_strand(seq1).reverse #complementary_dna, reverse for check dna
            check_DNA(seq1, seq2)
            expect(decompose_single_strand(seq1)).to eq("Frame 1: TGC GAT GAA TGG GCT CGC TCC\nFrame 2: T GCG ATG AAT GGG CTC GCT CC\nFrame 3: TG CGA TGA ATG GGC TCG CTC C")
            
        end
        it 'creates 6 reading frames' do
            seq1 = "AGGTGACACCGCAAGCCTTATATTAGC"
            seq2 = DNA_strand(seq1).reverse #complementary_dna.
            check_DNA(seq1, seq2)
            expect(decompose_double_strand(seq1, seq2)).to eq("Frame 1: AGG TGA CAC CGC AAG CCT TAT ATT AGC\nFrame 2: A GGT GAC ACC GCA AGC CTT ATA TTA GC\nFrame 3: AG GTG ACA CCG CAA GCC TTA TAT TAG C\nReverse Frame 1: GCT AAT ATA AGG CTT GCG GTG TCA CCT\nReverse Frame 2: G CTA ATA TAA GGC TTG CGG TGT CAC CT\nReverse Frame 3: GC TAA TAT AAG GCT TGC GGT GTC ACC T")
        end


        it 'turns DNA reading frames into mrna' do
            seq1 = "AGGTGACACCGCAAGCCTTATATTAGC"
            seq2 = DNA_strand(seq1).reverse
            check_DNA(seq1, seq2)
            reading_frame = decompose_double_strand(seq1, seq2)
            expect(dna_to_rna(reading_frame)).to eq("Frame 1: AGG UGA CAC CGC AAG CCU UAU AUU AGC\nFrame 2: A GGU GAC ACC GCA AGC CUU AUA UUA GC\nFrame 3: AG GUG ACA CCG CAA GCC UUA UAU UAG C\nReverse Frame 1: GCU AAU AUA AGG CUU GCG GUG UCA CCU\nReverse Frame 2: G CUA AUA UAA GGC UUG CGG UGU CAC CU\nReverse Frame 3: GC UAA UAU AAG GCU UGC GGU GUC ACC U")
        end

        it 'turns mRNA into reading frames' do
            seq1 = "AGGTGACACCGCAAGCCTTATATTAGC"
            seq2 = DNA_strand(seq1).reverse
            check_DNA(seq1, seq2)
            mRNA_seq1 = dna_to_rna(seq1) 
            mRNA_seq2 = dna_to_rna(seq2) 
            expect(decompose_double_strand(mRNA_seq1, mRNA_seq2)).to eq("Frame 1: AGG UGA CAC CGC AAG CCU UAU AUU AGC\nFrame 2: A GGU GAC ACC GCA AGC CUU AUA UUA GC\nFrame 3: AG GUG ACA CCG CAA GCC UUA UAU UAG C\nReverse Frame 1: GCU AAU AUA AGG CUU GCG GUG UCA CCU\nReverse Frame 2: G CUA AUA UAA GGC UUG CGG UGU CAC CU\nReverse Frame 3: GC UAA UAU AAG GCU UGC GGU GUC ACC U")
        end

        it 'turns mRNA into reading frames' do
            seq1 = "TGCGATGAATGGGCTCGCTCC"
            seq2 = DNA_strand(seq1).reverse
            check_DNA(seq1, seq2)
            p mRNA_seq1 = dna_to_rna(seq1) 
            p mRNA_seq2 = dna_to_rna(seq2) 
            expect(decompose_double_strand(mRNA_seq1, mRNA_seq2)).to eq("Frame 1: UGC GAU GAA UGG GCU CGC UCC\nFrame 2: U GCG AUG AAU GGG CUC GCU CC\nFrame 3: UG CGA UGA AUG GGC UCG CUC C\nReverse Frame 1: GGA GCG AGC CCA UUC AUC GCA\nReverse Frame 2: G GAG CGA GCC CAU UCA UCG CA\nReverse Frame 3: GG AGC GAG CCC AUU CAU CGC A")
        end
        it 'turns mrna into protien' do
            seq1 = "TGCGATGAATGGGCTCGCTCC"
            seq2 = DNA_strand(seq1).reverse
            check_DNA(seq1, seq2)
            mRNA_seq1 = dna_to_rna(seq1) 
            mRNA_seq2 = dna_to_rna(seq2) 
            f2 = seq1[1..-3].scan(/.../).join" "
            # expect(protein()).to eq("CDEWARSTLLTRAR")
        end
        it 'turns mrna reading frames into protien' do
            seq1 = "TGCGATGAATGGGCTCGCTCC"
            seq2 = DNA_strand(seq1).reverse
            check_DNA(seq1, seq2)
            mRNA_seq1 = dna_to_rna(seq1) 
            mRNA_seq2 = dna_to_rna(seq2) 
            f2 = seq1[1..-3].scan(/.../).join" "
           frames = decompose_double_strand(mRNA_seq1, mRNA_seq2).join("")
            expect(protein(frames)).to eq("CDEWARSTLLTRAR")
        end
    end

end
