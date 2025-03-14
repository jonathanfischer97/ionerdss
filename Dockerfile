# Use Miniconda as the base image
FROM continuumio/miniconda3:latest

# Set the working directory inside the container
WORKDIR /app

# Copy the Conda environment file
COPY environment.yml .

# Create the Conda environment
RUN conda env create -f environment.yml

# Set Conda environment as default by modifying PATH
ENV PATH=/opt/conda/envs/ionerdss_env/bin:$PATH

# Copy the rest of the application files
COPY . .

# Expose Jupyter Notebook port
EXPOSE 8888

# Default command to run Jupyter Notebook
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]