FROM python:3.4.5
## Install app
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
RUN pip install --upgrade pip

##

COPY . /usr/src/app

# Install python-newick
WORKDIR /usr/src/app/python-newick
RUN python setup.py install

# install atlas
WORKDIR /usr/src/app
RUN pip install -r requirements.txt
RUN python setup.py install
 
CMD atlas genotype-and-place 333-08  panel_tb_k31_2016-07-04_no_singeltons.fasta -1 333-08.fastq.gz --mccortex31_path mccortex/bin/mccortex31  --searchable_samples ssamples.txt -k 31 --tree RAxML_der_and_valbestTree.raxml3674