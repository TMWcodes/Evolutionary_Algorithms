def decompose_double_strand(seq1, rseq2)
    output = ""
    
    frame1 = seq1.scan(/.../).join" "
    f2 = seq1[1..-3].scan(/.../).join" "
    frame2 = seq1[0] + " " + f2 + " " + seq1[-2..-1]
    f3 = seq1[2..-2].scan(/.../).join" "
    frame3 = seq1[0..1] + " " + f3 + " " + seq1[-1]
    # output << [frame1, f2, f3].join("\n")
    output << ["Frame 1: #{frame1}", "Frame 2: #{frame2}", "Frame 3: #{frame3}"].join("\n")
    # output << "\n"

    
    rframe1 = rseq2.scan(/.../).join" "
    f2 = rseq2[1..-3].scan(/.../).join" "
   rframe2 = rseq2[0] + " " + f2 + " " + rseq2[-2..-1]
    f3 = rseq2[2..-2].scan(/.../).join" "
    rframe3 = rseq2[0..1] + " " + f3 + " " + rseq2[-1]
    # output << [rframe1, f2, f3].join("\n")
    output << ["\nReverse Frame 1: #{rframe1}", "Reverse Frame 2: #{rframe2}", "Reverse Frame 3: #{rframe3}"].join("\n")
    output
end

# def format

# end

# puts decompose_double_strand("UGCGAUGAAUGGGCUCGCUCC", "ACGCUACUUACCCGAGCGAGG")
