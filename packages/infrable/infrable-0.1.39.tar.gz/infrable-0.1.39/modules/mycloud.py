from dataclasses import dataclass
from typer import Typer
from infrable import Host, infra

@dataclass
class MyCloud:
    """MyCloud Python library."""

    secret_api_key: str
    typer: Typer | None = None

    def provision_ubuntu_host(self, fqdn: str):
        ip = self.api.create_ubuntu_host(fqdn)
        return MyCloudUbuntuHost(fqdn=fqdn, ip=ip)

@dataclass
class MyCloudUbuntuHost(Host):
    """MyCloud's customized Ubuntu server."""

    def setup(self):
        self.install_mycloud_agent()

    def install_mycloud_agent(self):
        raise NotImplementedError

workflows = Typer()

@workflows.command()
def provision_ubuntu_host(fqdn: str, setup: bool = True):
    """[WORKFLOW] Provision Ubuntu host."""

    # Get the MyCloud instance from infra.py
    cloud = next(iter(infra.item_types[MyCloud].values()))

    # Provision the host
    host = cloud.provision_ubuntu_host(fqdn)
    if setup:
        host.setup()

    name = fqdn.split(".")[0].replace("-", "_")
    print("Add the host to the infra.py file.")
    print(f"{name} = {repr(host)}")