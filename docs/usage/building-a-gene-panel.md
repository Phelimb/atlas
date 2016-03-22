#  Building a gene panel


Building a gene panel for use with [`atlas genotype`](doc:genotyping) 

## Gene panel fastas

In the simplest case a gene panel is just a fasta file with the header being the name of the gene. However, if you want to type multiple versions of the same gene you need to make sure the fasta headers are in the right format. 



e.g if you want to genotype within the oxa family the format would be as follows. 

	 >oxa?name=oxa&version=100
	ATGAACAT...TATAG
	>oxa?name=oxa&version=101
	ATGAAAAC...CTAAG 
You can include any additional parameters in the header with &par=val and it will be reported in the Sequence Call reported by `atlas genotype`
