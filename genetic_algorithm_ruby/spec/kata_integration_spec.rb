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

