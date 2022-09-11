require 'cross_over.rb'

describe 'crossover' do
    it 'crosses chromosome at index' do
    expect(crossover("110", "001", 2)).to eq(["111", "000"])
    expect(crossover("111000", "000110", 3)).to eq(["111110", "000000"])
    end
    it 'remains the same if no index given' do
    expect(crossover("00000000", "11111111", 0)).to eq(["11111111", "00000000"])
    end
end

