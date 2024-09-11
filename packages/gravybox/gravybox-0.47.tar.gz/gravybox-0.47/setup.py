from setuptools import setup

installation_requirements = [
    "logtail-python==0.2.10",
    "fastapi[standard]==0.112.2",
    "pydantic==2.8.2",
    "starlette==0.38.2",
    "httpx==0.27.2",
]

setup(
    name="gravybox",
    description="A big box of gravy for all of your FastAPI-ripping docker-aboded itty-bits. Enjoy at leisure.",
    version="0.47",
    url="https://github.com/clementinegroup/gravybox",
    author="(~)",
    package_dir={"": "packages"},
    packages=["gravybox"],
    install_requires=installation_requirements
)
