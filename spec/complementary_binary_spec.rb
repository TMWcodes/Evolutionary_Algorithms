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