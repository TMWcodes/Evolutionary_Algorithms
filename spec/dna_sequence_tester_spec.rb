require 'dna_sequence_tester.rb'

describe 'dna_sequence_tester' do
    context 'when given sequence of same length' do
        it 'returns true of false' do
            expect(check_DNA('ATGCTACG','CGTAGCAT')).to eq(true)
        end
    end

end