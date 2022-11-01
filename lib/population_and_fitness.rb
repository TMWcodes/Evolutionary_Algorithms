
population = %w|11001111 01110001
00010011 01101100 00110101 00110011 01011000 11101001 11101101
10001100 01100101 01000001 01010000 00000000 11110111 01100000
11110011 10101110 10101100 11101010 10011000 01100001 00101001
11101000 11011101 00110111 00111011 10100100 11101100 01111011
00001010 10010010 11101000 00110000 01000010 10100110 10011101
11110000 00100010 11001010 11010001 00010110 10110011 00111000
10111010 10000100 11101011 01001111 01101101 00101110 11010110
11100110 10010011 00110100 11011111 00111100 01011011 11101100
01110101 11010111 00101000 00100110 11001010 10011011 01000011
00101111 01110110 10011110 11011101 10011110 00001101 01101100
01110111 00111101 00000011 00111001 10000011 01000110 01011101
01110011 10011011 10000110 10101111 10111100 00011010 11100101
01110101 00000110 11111000 10000110 01001000 11111100 11010000
10011101 01001100 01101011 11010110 11011100 01000101 01110000|


def map_population_fit(population, &fitness)
  population.map {|w| {chromosome: w, fitness: fitness.call(w)}}
end


fitness = lambda do |c|
  ideal = '11110000'
  1.0 * ideal.chars.zip(c.chars).count{|x,y|x==y} / ideal.size
end

map_population_fit(population, &fitness)






