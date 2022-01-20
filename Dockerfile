FROM continuumio/miniconda3

WORKDIR /

COPY environment.yml .
RUN conda env create -f environment.yml

RUN echo "source activate venv-axelspace-assignment" > ~/.bashrc
ENV PATH /opt/conda/envs/venv-axelspace-assignment/bin:$PATH 

RUN echo "Testing imports"
RUN ["python", "-c", "import geopandas"]
RUN echo "Import success"

COPY . .

RUN echo "Starting test suite"
RUN ["python", "-m", "pytest", "tests/"]
RUN echo "Test suite completed successfully"

ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "venv-axelspace-assignment", "PYTHONPATH=${PWD}:${PWD}/src", "python", "./solution.py"]