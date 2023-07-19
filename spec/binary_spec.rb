require 'binary'

describe GeneticAlgorithm do
    binary = GeneticAlgorithm.new
    context 'when creating a strand of dna' do
        it 'can generate single binary strand' do
            expect(binary.generate(10)).to include("1","0")
        end
        it 'returns a value of 1 or 0' do
            expect(binary.generate(1)).to eq("1").or eq("0")
        end
        it 'is equal to given length' do
            expect(binary.generate(20).length).to eq(20)
        end
    end
    context 'when mutating a strand of dna' do
        it 'inverts character' do
            expect(binary.mutate("1", 1)).to eq("0")
            expect(binary.mutate("1", 1)).not_to eq("1")
            expect(binary.mutate("01010", 1)).to eq("10101")
            expect(binary.mutate("000000", 1)).to eq("111111")
            expect(binary.mutate("111111", 1)).to eq("000000")
        end
        it 'fails if given a letter' do
            expect {p binary.mutate("b", 1)}.to raise_error("invalid nucleotide")
        end
        context 'if given a probability of 0' do
            it 'returns the same value' do
            expect(binary.mutate("0" , 0)).to eq("0")
            expect(binary.mutate("01010", 0)).to eq("01010")
            end
        end
    end
    context 'if given a probabiity of 0.5' do
        it 'has a 1 and a 0' do
            expect(binary.mutate("11111", 0.5)).to include("1", "0")
        end
       end
    
    context 'when doing cross over' do
        it 'crosses chromosome at index' do
            expect(binary.crossover("110", "001", 2)).to eq(["111", "000"])
            expect(binary.crossover("111000", "000110", 3)).to eq(["111110", "000000"])
        end
        it 'remains the same if no index given' do
        expect(binary.crossover("00000000", "11111111", 0)).to eq(["11111111", "00000000"])
        end
    end
end