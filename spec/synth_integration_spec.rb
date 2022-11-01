require 'chromosome.rb'
require 'cross_over.rb'
require 'mutation.rb'
require 'population_and_fitness.rb'

describe 'synth_dna' do
    context 'when beginning' do
        it 'can generate chromosome' do
            expect(generate(10)).to include("1","0")
        end

        it 'can cross over ' do
        cross = crossover("111000", "000110", 3)
        expect(cross.map{ |chromosome| mutate(chromosome, 1) }).to eq ["000001", "111111"]
        end
    end
end
