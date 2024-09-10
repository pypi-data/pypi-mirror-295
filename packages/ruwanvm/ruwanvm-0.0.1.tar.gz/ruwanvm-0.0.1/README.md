# Run tests locally

Build Docker image to run test cases

`docker build -t ruwanvm-client-lib-unittest .`

Once image is build, run tests

`docker run -it ruwanvm-client-lib-unittest /bin/bash -c 'sh run_tests.sh'`