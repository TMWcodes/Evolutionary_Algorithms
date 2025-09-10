require 'synth_genome.rb'

describe 'GeneticAlgorithm' do

    let(:gene) {GeneticAlgorithm.new()}

    context 'when beginning' do

        it 'can generate single binary strand' do
            expect(gene.generate(10,1).to_s).to include("1","0")
        end

        it 'can generate a population of genes' do
            expect(gene.generate(8,2).length).to eq 2
            expect(gene.generate(10,2)).to be_an_instance_of(Array)
        end
        # it 'can generate and check double binary strand' do
        #     chromosome = "0111010000"
        #     expect(gene.binary_double(chromosome)).to eq("1000101111")
        #     seq2 = binary_double(chromosome).reverse
        #     expect(gene.check_binary(chromosome, seq2)).to eq(true)
        # end
    end

    context 'when selecting the next generation' do

        it 'can determine fitness' do
            population = ["01100100", "10000111", "01100010", "10001111"]
            fitness = lambda do |chromosome|
                ideal = '11110000'
                1.0 * ideal.chars.zip(chromosome.chars).count { |x, y| x == y } / ideal.size 
                end
            expect(gene.map_population_fit(population, &fitness).map { |individual| individual[:fitness] }).to eq [0.625, 0.25, 0.625, 0.125]
        end

        it 'can select the fitess genes' do
            population = ["01100100", "10000111", "01100010", "10001111"]
            fitness_values = [0.625, 0.25, 0.625, 0.125]
            expect(gene.roulette_wheel_selection(population, fitness_values, fitness_values.length/2)).to include("01100100").or include("01100010")
        end
        # can produce duplicates
    end

    
    context 'when adding variation' do
        it 'can cross over complementary strands' do
            chromosome1 = "111000111"
            chromosome2 = "000111000"
            # expect(seq1).to eq("111000111")
            # expect(seq2).to eq("000111000")
            expect(gene.crossover(chromosome1, chromosome2, 3)).to eq(["111111000", "000000111"])
        end
   
        it 'can mutate after cross over' do
            cross = gene.crossover("111000", "000110", 3)
            expect(cross.map{ |chromosome| gene.mutate(chromosome, 1) }).to eq ["000001", "111111"]
        end
    end
    
end