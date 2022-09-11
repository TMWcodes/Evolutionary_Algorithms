def generate(length)
  nucleotide = [0,1]
  chromosome = []
  until chromosome.length >= length
  chromosome << nucleotide.sample
  end
  chromosome.join
  # Good Luck!
end
  # generated_numbers = 4.times.map{Random.rand(8) } #=> [4, 2, 6, 8]

  p generate(10)