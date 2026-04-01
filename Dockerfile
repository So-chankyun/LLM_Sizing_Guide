FROM python:3.12-slim

WORKDIR /workspace

# Install uv
RUN pip install uv

# Copy uv dependency files
COPY pyproject.toml uv.lock ./

# Copy the rest of the application code
COPY app/ app/
COPY configs/ configs/
COPY llm_calculator/ llm_calculator/
COPY LLM_size_pef_calculator.py README.md ./

# Sync dependencies using uv, excluding dev dependencies
RUN uv sync --frozen --no-dev

# Expose the API port
EXPOSE 8000

# Start the application using uvicorn correctly within uv run
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
