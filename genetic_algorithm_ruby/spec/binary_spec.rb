
require 'binary.rb'
describe '' do
    context 'when creating a strand of dna' do
        it 'can generate single binary strand' do
            expect(generate(10).join()).to include("1","0")
        end
        it 'returns a value of 1 or 0' do
            expect(generate(1)).to eq(["1"]).or eq(["0"])
        end
        it 'is equal to given length' do
            expect(generate(20).join().length).to eq(20)
        end
    end
end