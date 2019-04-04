FROM geodata/gdal:latest

RUN pip install boto3 

# Scripts downloaded & modified from https://gitlab.officialstatistics.org/joe.peskett/ecw_converter.git
COPY ecw_converter /usr/local/bin/ecw_converter

# Make the scripts executable
RUN chmod -R +x /usr/local/bin/ecw_converter

ENV PATH=$PATH:/usr/local/bin/ecw_converter