require 'counting_dna_nucleotides.rb'

describe 'get_counted_nucleotides' do
    context 'when given no input' do
        it 'returns 0 for each nucleobase' do
            expect(get_counted_nucleotides('')).to eq({"A" => 0, "C" => 0, "G" => 0, "T" => 0})
        end
    end
end