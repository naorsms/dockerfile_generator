# Dockerfile generator
Nginx-Gunicorn-Flask Dockerfile generator.
It will be able to generate following Dockerfiles:
* Frontend production
* Frontend staging
* Frontend development
* Backend production
* Backend staging
* Backend development

Production: Big service which can handle heavy traffic.
Staging: Moderate service - can handle less traffic.
Development - can handle small traffic but yet has to be multithreaded to simulate the prod env.
              Moreover all development env docker images should have debug tools installed.

1) the software uses Argparse command example:
   "python3.8 serivce_deployer.py --environment_level prd --service_name frontend"

2) Input: environment level: one of [prd, stg, dev]
          service name: one of [frontend, backend]

3) Output: Dockerfile generated per environment ans service name.
           No need for the Frontend-backend containers to communicate.
   Frontend:
            Production:  Only Nginx server with some sample index.html file.
                         Without Gunicorn and Flask.

            Staging:     Only Nginx server with some sample index.html file.
                         Without Gunicorn and Flask.

            Development: Only Nginx server with some sample index.html file.
                         Without Gunicorn and Flask.
                         Has following tools installed into Docker image: vim, ping, traceroute, curl, wget, pip.
   Backend:
            Production:  Only Nginx server with some sample index.html
                         Number of workers 4, number of threads 4.

            Staging:     Has only the service from first and second steps.
                         Number of workers 3, number of threads 3.

            Development: Has the service from first and second steps.
                         Number of workers 2, number of threads 2.
                         Has following tools installed into Docker image: vim, ping, traceroute, curl, wget, pip.