def decompose_double_strand(seq1, seq2)
    output = ""
    
    frame1 = seq1.scan(/.../).join" "
    f2 = seq1[1..-3].scan(/.../).join" "
    frame2 = seq1[0] + " " + f2 + " " + seq1[-2..-1]
    f3 = seq1[2..-2].scan(/.../).join" "
    frame3 = seq1[0..1] + " " + f3 + " " + seq1[-1]
    # output << [frame1, frame2, frame3].join("\n")
    output << ["Frame 1: #{frame1}", "Frame 2: #{frame2}", "Frame 3: #{frame3}"].join("\n")

    frame1 = seq2.scan(/.../).join" "
    f2 = seq2[1..-3].scan(/.../).join" "
    frame2 = seq2[0] + " " + f2 + " " + seq2[-2..-1]
    f3 = seq2[2..-2].scan(/.../).join" "
    frame3 = seq2[0..1] + " " + f3 + " " + seq2[-1]
    # output << [frame1, frame2, frame3].join("\n")

    output << ["\nReverse Frame 1: #{frame1}", "Reverse Frame 2: #{frame2}", "Reverse Frame 3: #{frame3}"].join("\n")
    output
end



# decompose_double_strand("AGGTGACACCGCAAGCCTTATATTAGC", "GCTAATATAAGGCTTGCGGTGTCACCT")
