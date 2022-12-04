require '6_reading_frames'


describe '6 frames ' do
    context 'after recieiving a string of dna' do
        it 'creates reverse complement' do
            five_three = "AGGTGACACCGCAAGCCTTATATTAGC"
            three_five = "TCCACTGTGGCGTTCGGAATATAATCG"  
            reversed_reverse_complement = three_five.reverse
            expect(reversed_reverse_complement == "TCCACTGTGGCGTTCGGAATATAATCG".reverse).to be true
        end
        it 'displays 6 reading frames' do
            seq1 = "AGGTGACACCGCAAGCCTTATATTAGC"
            seq2 = "TCCACTGTGGCGTTCGGAATATAATCG".reverse
            expect(decompose_double_strand(seq1,seq2)).to eq(
"Frame 1: AGG TGA CAC CGC AAG CCT TAT ATT AGC
Frame 2: A GGT GAC ACC GCA AGC CTT ATA TTA GC
Frame 3: AG GTG ACA CCG CAA GCC TTA TAT TAG C
Reverse Frame 1: GCT AAT ATA AGG CTT GCG GTG TCA CCT
Reverse Frame 2: G CTA ATA TAA GGC TTG CGG TGT CAC CT
Reverse Frame 3: GC TAA TAT AAG GCT TGC GGT GTC ACC T")
        end

    end
end