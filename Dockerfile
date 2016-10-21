FROM python:3.4.5
## Install app
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
RUN pip install --upgrade pip

##

COPY . /usr/src/app

# Install mccortex
RUN rm -rf mccortex
RUN git clone -b genotype --recursive https://github.com/Phelimb/mccortex.git
WORKDIR /usr/src/app/mccortex
RUN make clean && make
ENV PATH /usr/src/app/mccortex/bin:$PATH

# Install python-newick
WORKDIR /usr/src/app/python-newick
RUN python setup.py install

# install atlas
WORKDIR /usr/src/app
RUN pip install -r requirements.txt
RUN python setup.py install
RUN pip install mykrobe  --no-dependencies
RUN pip install uwsgi hug

CMD uwsgi --processes 4 --threads 2 --pythonpath python-newick/ --pythonpath /usr/local/lib/python3.4/site-packages/ --http 0.0.0.0:8000 --wsgi-file mykatlas/server.py --callable __hug_wsgi__