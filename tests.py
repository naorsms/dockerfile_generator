import io
import unittest
import os
import subprocess


class TestCommands(unittest.TestCase):
    def test_backend_prd(self):
        subprocess.run("python main.py --environment_level prd --service_name backend")
        self.assertListEqual(
            list(io.open("Dockerfile")),
            list(io.open("./tests/Dockerfile-backend-prd"))
        )
        self.assertListEqual(
            list(io.open("startup.sh")),
            list(io.open("./tests/startup.sh-backend-prd"))
        )
        os.remove("Dockerfile")
        os.remove("startup.sh")

    def test_backend_stg(self):
        subprocess.run("python main.py --environment_level stg --service_name backend")
        self.assertListEqual(
            list(io.open("Dockerfile")),
            list(io.open("./tests/Dockerfile-backend-stg"))
        )
        self.assertListEqual(
            list(io.open("startup.sh")),
            list(io.open("./tests/startup.sh-backend-stg"))
        )
        os.remove("Dockerfile")
        os.remove("startup.sh")

    def test_backend_dev(self):
        subprocess.run("python main.py --environment_level dev --service_name backend")
        self.assertListEqual(
            list(io.open("Dockerfile")),
            list(io.open("./tests/Dockerfile-backend-dev"))
        )
        self.assertListEqual(
            list(io.open("startup.sh")),
            list(io.open("./tests/startup.sh-backend-dev"))
        )
        os.remove("Dockerfile")
        os.remove("startup.sh")

    def test_frontend_prd(self):
        subprocess.run("python main.py --environment_level prd --service_name frontend")
        self.assertListEqual(
            list(io.open("Dockerfile")),
            list(io.open("./tests/Dockerfile-frontend-prd"))
        )
        self.assertListEqual(
            list(io.open("startup.sh")),
            list(io.open("./tests/startup.sh-frontend-prd"))
        )
        os.remove("Dockerfile")
        os.remove("startup.sh")

    def test_frontend_stg(self):
        subprocess.run("python main.py --environment_level stg --service_name frontend")
        self.assertListEqual(
            list(io.open("Dockerfile")),
            list(io.open("./tests/Dockerfile-frontend-stg"))
        )
        self.assertListEqual(
            list(io.open("startup.sh")),
            list(io.open("./tests/startup.sh-frontend-stg"))
        )
        os.remove("Dockerfile")
        os.remove("startup.sh")

    def test_frontend_dev(self):
        subprocess.run("python main.py --environment_level dev --service_name frontend")
        self.assertListEqual(
            list(io.open("Dockerfile")),
            list(io.open("./tests/Dockerfile-frontend-dev"))
        )
        self.assertListEqual(
            list(io.open("startup.sh")),
            list(io.open("./tests/startup.sh-frontend-dev"))
        )
        os.remove("Dockerfile")
        os.remove("startup.sh")


if __name__ == '__main__':
    unittest.main()
