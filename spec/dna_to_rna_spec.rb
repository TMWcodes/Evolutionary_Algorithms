require 'dna_to_rna' 

describe 'dna_to_rna' do
    it  'replaces thymine and uracil' do
     expect(dna_to_rna("TTTT")).to be("UUUU")
     expect(dna_to_rna("GCAT")).to eq("GCAU")
     expect(dna_to_rna("GACCGCCGCC")).to eq("GACCGCCGCC")
end


end