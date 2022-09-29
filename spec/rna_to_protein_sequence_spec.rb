require 'rna_to_protein_sequence.rb'

describe 'rna to protien' do
    context 'when given one codon' do
        it 'returns an amino acid' do
            expect(protein('AUG')).to eq('M')
        end
        it 'can return stop' do
            expect(protein('UGA')).to eq('Stop')
        end
    end
    context 'when given multiple codons' do
        it 'returns multiple aminoacids' do
            expect(protein('UUCGAC')).to eq('FD')
        end
        it 'ignores stop' do
            expect(protein('AUGGUUAGUUGA')).to eq('MVS')
        end
        it '' do
            expect(protein('AUGUCCUUCCAUCAAGGAAACCAUGCGCGUUCAGCUUUCUGA')).to eq('MSFHQGNHARSAF')
        end

    end 
end
