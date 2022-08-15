# Required Image for AWS Lambda
FROM amazon/aws-lambda-python:3.8

# RUN apt-get update && apt-get install -y ffmpeg

# Copy function code
COPY app/ ${LAMBDA_TASK_ROOT}

# Install function's dependencies
COPY requirement.txt .
RUN pip install -r requirement.txt --target "${LAMBDA_TASK_ROOT}"

# Set the CMD to handler (could also be done as a
# parameter override outside of the Dockerfile)
CMD [ "multithread_lambda_func.lambda_handler" ]