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

end