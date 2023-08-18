require 'bio_genome'

describe Genome do
    genome = Genome.new
    context 'starting with nothing' do
        it 'can generate single strand DNA' do
            expect(genome.generate_ssDNA(10).size).to eq(10)
            expect(genome.generate_ssDNA(10)).not_to include('U')
        end
        it 'can generate single strand RNA' do
            expect(genome.generate_rna(10).size).to eq(10)
            expect(genome.generate_rna(10)).not_to include('T')
        end
    end

    context 'after creating a dna strand' do
        it 'checks if generated strand matches' do
            seq1 = genome.generate_ssDNA(6) 
            seq2 = genome.complementary_DNA_strand(seq1).reverse
            expect(genome.check_DNA(seq1, seq2)).to eq(true)
        end
        it 'checks if known strand matches complementary 3 to 5' do
            seq1 = "TGCGATGAATGGGCTCGCTCC"
            expect(genome.complementary_DNA_strand(seq1)).to eq('ACGCTACTTACCCGAGCGAGG')
        end
        it 'checks if known strand matches 5 to 3' do
            seq1 = "TGCGATGAATGGGCTCGCTCC"
            expect(genome.complementary_DNA_strand(seq1).reverse).to eq("GGAGCGAGCCCATTCATCGCA")
        end
    end

    context 'after creating a double helix' do
        it 'makes dna into mrna' do
            seq1 = "TGCGATGAATGGGCTCGCTCC"
            seq2 = genome.complementary_DNA_strand(seq1).reverse
           expect(genome.dna_to_rna(seq1)).to eq('UGCGAUGAAUGGGCUCGCUCC')
           expect(genome.dna_to_rna(seq2)).to eq('GGAGCGAGCCCAUUCAUCGCA')
        end

        it 'turns RNA strand into aminoacids' do
            seq1 = "TGCGATGAATGGGCTCGCTCC"
            seq2 = genome.complementary_DNA_strand(seq1).reverse
            mRNA1 = genome.dna_to_rna(seq1)
            mRNA2 = genome.dna_to_rna(seq2)
            expect(genome.protein(mRNA1)).to eq('CDEWARS') 
            expect(genome.protein(mRNA2)).to eq('GASPFIA') 
        end
        
        it 'turns DNA into DNA reading frames' do
            seq1 = "TGCGATGAATGGGCTCGCTCC"
            seq2 = genome.complementary_DNA_strand(seq1).reverse
            expect(genome.six_reading_frames(seq1, seq2)).to eq(["TGC GAT GAA TGG GCT CGC TCC\nGCG ATG AAT GGG CTC GCT\nCGA TGA ATG GGC TCG CTC", "GGA GCG AGC CCA TTC ATC GCA\nGAG CGA GCC CAT TCA TCG\nAGC GAG CCC ATT CAT CGC"])
        end
        it 'turns DNA into protien reading frames' do
            expect(genome.translate_with_frame(dna="TGCGATGAATGGGCTCGCTCC", frames=[1,2,3,-1,-2,-3])).to eq(["CDEWARS", "AMNGLA", "R*MGSL", "GASPFIA", "ERAHSS", "SEPIHR"])
        end

    end
end