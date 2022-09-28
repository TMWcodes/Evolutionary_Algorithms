require 'counting_dna_nucleotides.rb'

describe 'get_counted_nucleotides' do

    context 'when given no input' do
        it 'returns 0 for each nucleobase' do
            expect(get_counted_nucleotides('')).to eq({"A" => 0, "C" => 0, "G" => 0, "T" => 0})
        end
    end

    context 'when given less than 4 nucleobases' do
        it 'counts nucleotides' do
        expect(get_counted_nucleotides('TTT')).to eq({"A" => 0, "C" => 0, "G" => 0, "T" => 3});
        end
    end

end