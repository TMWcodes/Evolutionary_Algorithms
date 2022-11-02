require 'complementary_binary'

describe 'binary_strand' do
    context 'when given a single strand' do
        it 'matches strand' do
            expect(binary_double("1111")).to eq("0000")
            expect(binary_double("0000")).to eq("1111")
            expect(binary_double("1010")).to eq("0101")
        end
    end
end

describe 'dna_sequence_tester' do
    context 'when given matching sequence of same length' do
        it 'returns true' do
            expect(check_binary('101010','101010')).to eq(true)
        end
    end

    context 'when given non matching sequence of same length' do
        it 'returns false' do
            expect(check_binary('101010','010101')).to eq(false)
        end
    end
end