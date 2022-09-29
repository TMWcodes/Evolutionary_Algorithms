require 'dna_sequence_tester.rb'

describe 'dna_sequence_tester' do
    context 'when given matching sequence of same length' do
        it 'returns true' do
            expect(check_DNA('ATGCTACG','CGTAGCAT')).to eq(true)
        end
    end
    context 'when given non matching sequence of same length' do
        it 'returns false' do
            expect(check_DNA('GTCTTAGTGTAGCTATGCATGC','GCATGCATAGCTACACTACGAC')).to eq(false)
            expect(check_DNA('GTCACCGA','TCGGCTGAC')).to eq(false)
        end
    end
    context 'when given matching sequences of difference length' do
        it 'returns true' do
            expect(check_DNA('GCTAGCACCCATTAGGAGATAC','CTCCTAATGGGTG')).to eq(true)
            end
        it 'return' do
            expect(check_DNA('GCGCTGCTAGCTGATCGA','ACGTACGATCGATCAGCTAGCAGCGCTAC')).to eq(true)
            end
        end
    context 'when given non-matching sequences of difference length' do
        it 'returns false' do
            expect(check_DNA('ACGACTACGTGCGCCGCTAATATT','GCACGGGTCGT')).to eq(false)
        end
    end

end