import argparse
import logging

handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s] %(levelname)s:%(filename)s:%(lineno)s: %(message)s")
handler.setFormatter(formatter)
logger = logging.getLogger("main")
logger.setLevel("INFO")
logger.addHandler(handler)


class DockerService:
    DOCKERFILE_TEMPLATE_NAME = "TemplateDockerfile"
    STARTUP_SH_TEMPLATE_NAME = "TemplateStartup.sh"
    ENV_PACKAGES = {
        'prd': ['nginx'],
        'stg': ['nginx'],
        'dev': [
            'curl',
            'vim',
            'traceroute',
            'wget',
            'nginx'
        ]
    }
    PYTHON_ENV_INSTRUCTIONS = '''
RUN python3 -m venv /dockerfileGen    
ENV PATH="/dockerfileGen/bin:$PATH"
RUN pip3 install --no-cache-dir -r requirements.txt
'''
    GUNICORN_CONF = {
        'prd': ['4'],
        'stg': ['3'],
        'dev': ['2']
    }
    GUNICORN_ACTIVATION = '''
. /dockerfileGen/bin/activate
nohup gunicorn -w {env_level_num} --threads {env_level_num} --bind unix:/run/ipc.sock wsgi:app &
'''

    def __init__(self, environment_level):
        self.environment_level = environment_level

    def generate_dockerfile(self, packages=None, setup_python_env=False):
        if packages is None:
            packages = ['nginx']

        env_instructions = ''
        if setup_python_env:
            env_instructions = self.PYTHON_ENV_INSTRUCTIONS
            packages.extend([
                'python3.8',
                'python3-pip',
                'python3-venv',
            ])
        with open(self.DOCKERFILE_TEMPLATE_NAME) as template_file:
            dockerfile_content = template_file.read().format(
                packages=' '.join(packages),
                python_env_instructions=env_instructions,
            )

        with open('Dockerfile', 'wb') as output_dockerfile:
            output_dockerfile.write(bytes(dockerfile_content, "UTF-8"))

    def generate_startupfile(self, gunicorn_activation=None):

        if gunicorn_activation is None:
            gunicorn_activation = ''
        if gunicorn_activation:
            gunicorn_activation = self.GUNICORN_ACTIVATION
            gunicorn_activation = gunicorn_activation.format(
                env_level_num=self.GUNICORN_CONF[self.environment_level][0])
        with open(self.STARTUP_SH_TEMPLATE_NAME) as template_file:
            startup_sh_content = template_file.read().format(
                gunicorn_activation=gunicorn_activation
            )
        with open('startup.sh', 'wb') as output_startup_sh:
            output_startup_sh.write(bytes(startup_sh_content, "UTF-8"))


class Frontend(DockerService):
    def __init__(self, environment_level):
        super().__init__(environment_level)

    def generate(self):
        self.generate_dockerfile(packages=self.ENV_PACKAGES[self.environment_level])
        self.generate_startupfile()


class Backend(DockerService):
    def __init__(self, environment_level):
        super().__init__(environment_level)

    def generate(self):
        self.generate_dockerfile(packages=self.ENV_PACKAGES[self.environment_level],
                                 setup_python_env=True)
        self.generate_startupfile(gunicorn_activation=self.GUNICORN_ACTIVATION)


class ServiceDeployer:
    def __init__(self, environment_level, service_name):
        self.environment_level = environment_level
        self.service_name = service_name

    def run(self):
        logger.info(f"Deploying service '{self.service_name}' "
                    f"with level: '{self.environment_level}'")
        if self.service_name == "frontend":
            template = Frontend(self.environment_level)
            template.generate()
        elif self.service_name == "backend":
            template = Backend(self.environment_level)
            template.generate()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--environment_level", type=str, required=True,
                        choices={"prd", "stg", "dev"})
    parser.add_argument("--service_name", type=str, required=True,
                        choices={"frontend", "backend"})
    args = parser.parse_args()

    service_deployer = ServiceDeployer(args.environment_level, args.service_name)
    service_deployer.run()
