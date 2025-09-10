require 'chromosome.rb'

describe 'chromosome' do
    context 'when given a length of one' do
        it 'returns 1' do
            expect(generate(1).length).to eq(1)
        end
        it 'returns a value of 1 or 0' do
            expect(generate(1)).to eq("1").or eq("0")
        end
    end
    
        context 'when given a length longer than one' do
        it 'is equal to given length' do
            expect(generate(20).length).to eq(20)
        end
        it 'likely includes both 1 and 0' do
        expect(generate(20)).to include("1", "0") 
        end
    end
end