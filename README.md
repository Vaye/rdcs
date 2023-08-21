## Branch Description:
  This is a branch of RDCS. In order to adapt to the special restrictions of the 9sky environment, all services are put into one container, and supervisord is used to support each flask service. At the same time, some parameter passing has been optimized.

## installation instruction

### 1. build image：
    docker build -t rdcs_9sky:0.1 -f Dockerfile .

### 2. start container with the compose yaml
  compose/docker-compose.yml
### 3. test with test.py in the test directory
  The script may need to be modified according to your exact environment.
