require 'dna_to_rna' 

describe 'dna_to_rna' do
    it  'replaces thymine and uracil' do
     expect(dna_to_rna("TTTT")).to eq("UUUU")
     expect(dna_to_rna("GCAT")).to eq("GCAU")
     expect(dna_to_rna("GACCGCCGCC")).to eq("GACCGCCGCC")
    end

    it 'can take codons' do
        expect(dna_to_rna("AGG TGA CAC CGC AAG CCT TAT ATT AGC")).to eq("AGG UGA CAC CGC AAG CCU UAU AUU AGC")
    end


end