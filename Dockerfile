FROM python:3.7

# Setup paths:
ENV DIRPATH /sbml2sbol
WORKDIR $DIRPATH
COPY . .
ENV PYTHONPATH="$DIRPATH:$PYTHONPATH"

# Install Python dependencies:
RUN pip install --upgrade pip \
  && pip install -r requirements.txt
  
# Set ENTRYPOINT:
ENTRYPOINT ["python", "-u", "sbml2sbol/converter.py"]