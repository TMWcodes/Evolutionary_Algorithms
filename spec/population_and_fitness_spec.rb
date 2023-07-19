require 'population_and_fitness.rb'

describe 'population_and_fitness' do
    it 'calculates the fitness' do
        population = %w|11001111 01110001
        00010011 01101100|
        fitness = lambda do |c|
            ideal = '11110000'
            1.0 * ideal.chars.zip(c.chars).count{|x,y|x==y} / ideal.size
          end
        expect(map_population_fit(population, &fitness).first).to eq({:chromosome=>"11001111", :fitness=>0.25})
        expect(map_population_fit(population, &fitness).first[:fitness]).to eq(0.25)
        expect(map_population_fit(population, &fitness)[1][:fitness]).to eq(0.75)
        expect(map_population_fit(population, &fitness)[2][:fitness]).to eq(0.375)
        expect(map_population_fit(population, &fitness).first[:fitness]).to eq(0.25)
      
    end
    it 'can determine fitness' do
        population = %w|11001111 01110001
        00010011 01101100|
        fitness = lambda do |chromosome|
            ideal = '11110000'
            1.0 * ideal.chars.zip(chromosome.chars).count { |x, y| x == y } / ideal.size 
            end
        expect(map_population_fit(population, &fitness).map { |individual| individual[:fitness] }).to eq  [0.25, 0.75, 0.375, 0.5]
    end
end

