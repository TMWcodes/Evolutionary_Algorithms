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
        expect(get_counted_nucleotides('ACG')).to eq({"A" => 1, "C" => 1, "G" => 1, "T" => 0})
        end
    end
    context 'when given for or more nucleobases' do
        it 'counts all nucleotides' do
            expect(get_counted_nucleotides('AAACGT')).to eq({"A" => 3, "C" => 1, "G" => 1, "T" => 1})
        end
    end

end