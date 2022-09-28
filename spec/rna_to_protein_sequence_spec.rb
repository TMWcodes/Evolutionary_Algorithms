require 'rna_to_protein_sequence.rb'

describe 'rna to protien' do
    context 'when given one codon' do
        it 'returns and amino acid' do
            expect(protein('AUG')).to eq('M')
        end
    end
end
