require 'mutation.rb'

describe 'mutation' do
    
    context 'if given 100% probability' do
    it 'inverts character' do
        expect(mutate("1", 1)).to eq("0")
        expect(mutate("1", 1)).not_to eq("1")
        expect(mutate("01010", 1)).to eq("10101")
        expect(mutate("000000", 1)).to eq("111111")
        expect(mutate("111111", 1)).to eq("000000")
        end
    end
    it 'fails if given a letter' do
        expect {p mutate("b", 1)}.to raise_error("invalid nucleotide")
    end

    context 'if given a probability of 0' do
        it 'returns the same value' do
        expect(mutate("0" , 0)).to eq("0")
        expect(mutate("01010", 0)).to eq("01010")
            end
    end

   context 'if given a probabiity of 0.5' do
    it 'has a 1 and a 0' do
        expect(mutate("11111", 0.5)).to include("1", "0")
    end
   end

end