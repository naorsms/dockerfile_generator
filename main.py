import argparse
import logging
import re

handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s] %(levelname)s:%(filename)s:%(lineno)s: %(message)s")
handler.setFormatter(formatter)
logger = logging.getLogger("main")
logger.setLevel("INFO")
logger.addHandler(handler)


class DockerService:
    with open('Dockerfile') as dockerfile_unp:
        dockerfile = list(dockerfile_unp)
    with open('startup.sh') as startupsh_unp:
        startup_sh = list(startupsh_unp)

    def __init__(self, environment_level):
        self.environment_level = environment_level


class Frontend(DockerService):
    def __init__(self, environment_level):
        super().__init__(environment_level)

    def generate(self):
        f_df = open("Dockerfile1", "w")
        f_st = open("startup1.sh", "w")

        if self.environment_level == "prd":
            for line in self.dockerfile:
                if not re.search("(#)",line):
                    f_df.write(line)
            f_st.write(self.startup_sh[0])
            for line in self.startup_sh[1:]:
                if not re.search("(#)", line):
                    f_st.write(line)

        elif self.environment_level == "stg":
            for line in self.dockerfile:
                if not re.search("(#)", line):
                    f_df.write(line)
            f_st.write(self.startup_sh[0])
            for line in self.startup_sh[1:]:
                if not re.search("(#)", line):
                    f_st.write(line)

        elif self.environment_level == "dev":
            for line in self.dockerfile:
                if re.search("(#)", line):
                    if re.search("(curl|vim|ping|traceroute|wget)", line):
                        line_temp = line.replace("#", " ")
                        f_df.write(line_temp)
                else:
                    f_df.write(line)
            f_st.write(self.startup_sh[0])
            for line in self.startup_sh[1:]:
                if not re.search("(#)", line):
                    f_st.write(line)


class Backend(DockerService):
    def generate(self):
        f_df = open("Dockerfile1", "w")
        f_st = open("startup1.sh", "w")

        if self.environment_level == "prd":
            for line in self.dockerfile:
                if re.search("(#)", line):
                    if re.search("(python|pip|PATH)", line):
                        line_temp = line.replace("#", " ")
                        f_df.write(line_temp)
                else:
                    f_df.write(line)
            f_st.write(self.startup_sh[0])
            for line in self.startup_sh[1:]:
                if re.search("(#)", line):
                    if re.search("(gunicorn)", line):
                        f_st.write("nohup gunicorn -w 4 --threads 4 --bind unix:/run/ipc.sock wsgi:app &\n")
                    else:
                        line_temp = line.replace("#", "")
                        f_st.write(line_temp)
                else:
                    f_st.write(line)

        elif self.environment_level == "stg":
            for line in self.dockerfile:
                if re.search("(#)", line):
                    if re.search("(python|pip|PATH)", line):
                        line_temp = line.replace("#", " ")
                        f_df.write(line_temp)
                else:
                    f_df.write(line)
            f_st.write(self.startup_sh[0])
            for line in self.startup_sh[1:]:
                if re.search("(#)", line):
                    if re.search("(gunicorn)", line):
                        f_st.write("nohup gunicorn -w 3 --threads 3 --bind unix:/run/ipc.sock wsgi:app &\n")
                    else:
                        line_temp = line.replace("#", "")
                        f_st.write(line_temp)
                else:
                    f_st.write(line)
        elif self.environment_level == "dev":
            for line in self.dockerfile:
                if re.search("(#)", line):
                    if re.search("(python|curl|vim|ping|traceroute|wget|pip|PATH)", line):
                        line_temp = line.replace("#", " ")
                        f_df.write(line_temp)
                else:
                    f_df.write(line)
            f_st.write(self.startup_sh[0])
            for line in self.startup_sh[1:]:
                if re.search("(#)", line):
                    if re.search("(gunicorn)", line):
                        f_st.write("nohup gunicorn -w 2 --threads 2 --bind unix:/run/ipc.sock wsgi:app &\n")
                    else:
                        line_temp = line.replace("#", "")
                        f_st.write(line_temp)

                else:
                    f_st.write(line)


class ServiceDeployer:
    def __init__(self, environment_level, service_name):
        self.environment_level = environment_level
        self.service_name = service_name

    def run(self):
        logger.info(f"Deploying service '{self.service_name}' with level: '{self.environment_level}'")
        if self.service_name == "frontend":
            template = Frontend(self.environment_level)
            template.generate()
        elif self.service_name == "backend":
            template = Backend(self.environment_level)
            template.generate()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--environment_level", type=str, required=True, choices={"prd", "stg", "dev"})
    parser.add_argument("--service_name", type=str, required=True, choices={"frontend", "backend"})
    args = parser.parse_args()

    service_deployer = ServiceDeployer(args.environment_level, args.service_name)
    service_deployer.run()
