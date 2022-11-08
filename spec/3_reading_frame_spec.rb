require '3_reading_frame' 

describe 'reading frame' do

    context 'when given strand' do

        it 'creates 3 reading frames' do 
            expect(decompose_single_strand("AGGTGACACCGCAAGCCTTATATTAGC")).to eq("Frame 1: AGG TGA CAC CGC AAG CCT TAT ATT AGC\nFrame 2: A GGT GAC ACC GCA AGC CTT ATA TTA GC\nFrame 3: AG GTG ACA CCG CAA GCC TTA TAT TAG C")
        end

    end

end
