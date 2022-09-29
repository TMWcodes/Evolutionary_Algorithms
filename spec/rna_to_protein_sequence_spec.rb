require 'rna_to_protein_sequence.rb'

describe 'rna to protien' do
    context 'when given one codon' do
        it 'returns an amino acid' do
            expect(protein('AUG')).to eq('M')
        end
        # it 'can return stop' do
        #     expect(protein('UGA')).to eq('Stop')
        # end
    end
    context 'when given multiple codons' do
        it 'returns multiple aminoacids' do
            expect(protein('UUCGAC')).to eq('FD')
        end
        it 'can return long aminoacid chains' do
            expect(protein('AUGUCCUUCCAUCAAGGAAACCAUGCGCGUUCAGCUUUCUGA')).to eq('MSFHQGNHARSAF')
            expect(protein('AUGCUAUGGAGGGUAGUGUUAACUACCACGCCCAGUACUUGA')).to eq('MLWRVVLTTTPST')
        end
        it 'can read unique aminoacid chains' do
            expect(protein('UGCGAUGAAUGGGCUCGCUCC')).to eq('CDEWARS')
        end
        it 'does not display Stop' do
            expect(protein('AUGGUUAGUUGA')).to eq('MVS')
            expect(protein('AUGUGA')).to eq('M')
        end
        it 'Stops on Stop' do
            expect(protein('GCUUACAGGGGCUGUGACGAAUUCUGCGGCUAAAUUUCGGACCUUUUAGCA')).to eq("AYRGCDEFCG")
            
        end
        

    end 
end
