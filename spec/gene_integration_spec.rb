require 'complementary_dna'
require 'base_pairs'
require 'dna_sequence_tester'
require 'dna_to_rna'
require 'rna_to_protein_sequence'
require '3_reading_frame'
require '6_reading_frames'

describe 'transcription' do
    context 'after creating a dna strand' do
        it 'checks if generated strand matches' do
            seq1 = generate_strand(6)
            seq2 = DNA_strand(seq1).reverse
            expect(check_DNA(seq1, seq2)).to eq(true)
        end
        it 'checks if known strand matches' do
            seq1 = "atgacatgtt"
            expect(DNA_strand(seq1)).to eq('TACTGTACAA')
        end
    end

    context 'after creating a double helix' do
        it 'makes dna into mrna' do
            seq1 = "atgacatgtt".upcase
            seq2 = DNA_strand(seq1)
           expect(dna_to_rna(seq1)).to eq('AUGACAUGUU')
           expect(dna_to_rna(seq2)).to eq('UACUGUACAA')
        end

        it 'turns mrna into aminoacids' do
            seq1 = "atgacatgtt".upcase
            seq2 = DNA_strand(seq1)
            mRNA = dna_to_rna(seq1) 
            expect(protein(mRNA)).to eq('MTC')
        end
        it 'creates 6 reading frames' do
            seq1 = "AGGTGACACCGCAAGCCTTATATTAGC"
            seq2 = DNA_strand(seq1).reverse #complementary_dna.
            check_DNA(seq1, seq2)
            expect(decompose_single_strand(seq2)).to eq("Frame 1: GCT AAT ATA AGG CTT GCG GTG TCA CCT, Frame 2: G CTA ATA TAA GGC TTG CGG TGT CAC CT, Frame 3: GC TAA TAT AAG GCT TGC GGT GTC ACC T")
            expect(decompose_double_strand(seq1, seq2)).to eq("Frame 1: AGG TGA CAC CGC AAG CCT TAT ATT AGC\nFrame 2: A GGT GAC ACC GCA AGC CTT ATA TTA GC\nFrame 3: AG GTG ACA CCG CAA GCC TTA TAT TAG C\nReverse Frame 1: GCT AAT ATA AGG CTT GCG GTG TCA CCT\nReverse Frame 2: G CTA ATA TAA GGC TTG CGG TGT CAC CT\nReverse Frame 3: GC TAA TAT AAG GCT TGC GGT GTC ACC T")
        end
    end

end
