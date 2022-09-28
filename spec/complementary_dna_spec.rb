
require 'complementary_dna.rb'

describe 'DNA_strand' do
    it 'matches A with T' do
        expect(DNA_strand("AAAA")).to eq("TTTT")
    end
    it 'matches G with C' do
    expect(DNA_strand("ATTGC")).to eq("TAACG")
    end
    it 'matches G with C' do
        expect(DNA_strand("GTAT")).to eq("CATA")
        end
end