require 'binary.rb'
require 'complementary_binary'
require 'cross_over.rb'
require 'mutation.rb'
require 'population_and_fitness.rb'

describe 'synth_dna' do
    context 'when beginning' do
        it 'can generate single binary strand' do
            expect(generate(10)).to include("1","0")
        end
        it 'can generate and check double binary strand' do
            chromosome = "0111010000"
            expect(binary_double(chromosome)).to eq("1000101111")
            seq2 = binary_double(chromosome).reverse
            expect(check_binary(chromosome, seq2)).to eq(true)
        end
    end
    context 'when selecting the next generation' do
        it 'can determine fitness' do
            chromosome = generate(8,2)
            fitness = lambda do |chromosome|
                ideal = '11110000'
                1.0 * ideal.chars.zip(chromosome.chars).count { |x, y| x == y } / ideal.size 
                end
            expect(map_population_fit(chromosome, &fitness).map { |individual| individual[:fitness] }).to eq(Array)
        end
    end
    context 'when adding variation' do
        it 'can cross over complementary strands' do
            seq1 = "111000111"
            seq2 = binary_double(seq1)
            expect(seq1).to eq("111000111")
            expect(seq2).to eq("000111000")
            expect(crossover(seq1, seq2, 3)).to eq(["111111000", "000000111"])
        end

        it 'can mutate after cross over' do
            cross = crossover("111000", "000110", 3)
            expect(cross.map{ |chromosome| mutate(chromosome, 1) }).to eq ["000001", "111111"]
        end
    end
end

#######
# describe GeneticAlgorithm do
#     binary = GeneticAlgorithm.new
#     context 'when creating a strand of dna' do
#         it 'can generate single binary strand' do
#             expect(binary.generate(10)).to include("1","0")
#         end
#         it 'returns a value of 1 or 0' do
#             expect(binary.generate(1)).to eq("1").or eq("0")
#         end
#         it 'is equal to given length' do
#             expect(binary.generate(20).length).to eq(20)
#         end
#     end
#     context 'when mutating a strand of dna' do
#         it 'inverts character' do
#             expect(binary.mutate("1", 1)).to eq("0")
#             expect(binary.mutate("1", 1)).not_to eq("1")
#             expect(binary.mutate("01010", 1)).to eq("10101")
#             expect(binary.mutate("000000", 1)).to eq("111111")
#             expect(binary.mutate("111111", 1)).to eq("000000")
#         end
#         it 'fails if given a letter' do
#             expect {p binary.mutate("b", 1)}.to raise_error("invalid nucleotide")
#         end
#         context 'if given a probability of 0' do
#             it 'returns the same value' do
#             expect(binary.mutate("0" , 0)).to eq("0")
#             expect(binary.mutate("01010", 0)).to eq("01010")
#             end
#         end
#     end
#     context 'if given a probabiity of 0.5' do
#         it 'has a 1 and a 0' do
#             expect(binary.mutate("11111", 0.5)).to include("1", "0")
#         end
#        end
    
#     context 'when doing cross over' do
#         it 'crosses chromosome at index' do
#             expect(binary.crossover("110", "001", 2)).to eq(["111", "000"])
#             expect(binary.crossover("111000", "000110", 3)).to eq(["111110", "000000"])
#         end
#         it 'remains the same if no index given' do
#         expect(binary.crossover("00000000", "11111111", 0)).to eq(["11111111", "00000000"])
#         end
#     end
# end