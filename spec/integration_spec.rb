require 'complementary_dna'
require 'base_pairs'
require 'dna_sequence_tester'
require 'dna_to_rna'
require 'rna_to_protein_sequence'

describe 'transcription' do
    context 'after creating a dna strand' do
        it 'checks if generated strand matches' do
            seq1 = generate(6)
            seq2 = DNA_strand(seq1).reverse
            expect(check_DNA(seq1, seq2)).to eq(true)
        end
        it 'checks if known strand matches' do
            seq1 = "atgacatgtt"
            expect(DNA_strand(seq1)).to eq('TACTGTACAA')
        end
    end

    context 'after creating a dna strand' do
        it 'makes dna into rna' do
            seq1 = "atgacatgtt".upcase
            seq2 = DNA_strand(seq1)
           expect(dna_to_rna(seq1)).to eq('AUGACAUGUU')
           expect(dna_to_rna(seq2)).to eq('UACUGUACAA')
        end

        it 'turns rna into aminoacids' do
            seq1 = "atgacatgtt".upcase
            seq2 = DNA_strand(seq1)
            mRNA = dna_to_rna(seq1) 
            expect(protein(mRNA)).to eq('MTC')
        end
    end

end
