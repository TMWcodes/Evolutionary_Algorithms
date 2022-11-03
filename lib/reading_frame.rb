
def decompose_single_strand(dna)
    frame1 = dna.scan(/.../).join" "
    f2 = dna[1..-3].scan(/.../).join" "
    frame2 = dna[0] + " " + f2 + " " + dna[-2..-1]
    f3 = dna[2..-2].scan(/.../).join" "
    frame3 = dna[0..1] + " " + f3 + " " + dna[-1]
    ["Frame 1: #{frame1}", "Frame 2: #{frame2}", "Frame 3: #{frame3}"].join(", ")
end

decompose_single_strand("AGGTGACACCGCAAGCCTTATATTAGC")