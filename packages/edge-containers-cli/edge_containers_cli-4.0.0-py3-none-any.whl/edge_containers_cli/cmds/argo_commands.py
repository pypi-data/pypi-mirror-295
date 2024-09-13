"""
implements commands for deploying and managing service instances suing argocd

Relies on the Helm class for deployment aspects.
"""

import webbrowser
from datetime import datetime

import polars
from ruamel.yaml import YAML

from edge_containers_cli.cmds.commands import CommandError, Commands, ServicesDataFrame
from edge_containers_cli.definitions import ECContext
from edge_containers_cli.globals import TIME_FORMAT
from edge_containers_cli.shell import ShellError, shell


def extract_ns_app(target: str) -> tuple[str, str]:
    namespace, app = target.split("/")
    return namespace, app


class ArgoCommands(Commands):
    """
    A class for implementing the Kubernetes based commands
    """

    def __init__(
        self,
        ctx: ECContext,
    ):
        super().__init__(ctx)

    def logs(self, service_name, prev):
        self._logs(service_name, prev)

    def log_history(self, service_name):
        self._check_service(service_name)
        url = self.log_url.format(service_name=service_name)
        webbrowser.open(url)

    def ps(self, running_only):
        self._ps(running_only)

    def restart(self, service_name):
        self._check_service(service_name)
        namespace, app = extract_ns_app(self.target)
        cmd = (
            f"argocd app delete-resource {namespace}/{service_name} "
            f"--kind StatefulSet"
        )
        shell.run_command(cmd, skip_on_dryrun=True)

    def start(self, service_name):
        self._check_service(service_name)
        namespace, app = extract_ns_app(self.target)
        cmd = f"argocd app set {namespace}/{service_name} -p global.enabled=true"
        shell.run_command(cmd, skip_on_dryrun=True)

    def stop(self, service_name):
        self._check_service(service_name)
        namespace, app = extract_ns_app(self.target)
        cmd = f"argocd app set {namespace}/{service_name} -p global.enabled=false"
        shell.run_command(cmd, skip_on_dryrun=True)

    def _get_logs(self, service_name, prev) -> str:
        namespace, app = extract_ns_app(self.target)
        self._check_service(service_name)
        previous = "-p" if prev else ""

        logs = shell.run_command(
            f"argocd app logs {namespace}/{service_name} {previous}",
            error_OK=True,
        )
        return logs

    def _get_services(self, running_only) -> ServicesDataFrame:
        namespace, app = extract_ns_app(self.target)
        service_data = {
            "name": [],  # type: ignore
            "version": [],
            "ready": [],
            "deployed": [],
        }
        app_resp = shell.run_command(
            f'argocd app list -l "ec_service=true" --app-namespace {namespace} -o yaml',
        )
        app_dicts = YAML(typ="safe").load(app_resp)

        if not app_dicts:
            raise CommandError(f"No ec-services found in {self.target}")
        for app in app_dicts:
            resources_dict = app["status"]["resources"]

            for resource in resources_dict:
                is_ready = False
                if resource["kind"] == "StatefulSet":
                    name = app["metadata"]["name"]

                    # check if replicas ready
                    mani_resp = shell.run_command(
                        f"argocd app manifests {namespace}/{name} --source live",
                    )
                    for resource_manifest in mani_resp.split("---")[1:]:
                        manifest = YAML(typ="safe").load(resource_manifest)
                        if not manifest:
                            continue
                        kind = manifest["kind"]
                        resource_name = manifest["metadata"]["name"]
                        if kind == "StatefulSet" and resource_name == name:
                            try:
                                is_ready = bool(manifest["status"]["readyReplicas"])
                            except (KeyError, TypeError):  # Not ready if doesnt exist
                                is_ready = False
                            time_stamp = datetime.strptime(
                                manifest["metadata"]["creationTimestamp"],
                                "%Y-%m-%dT%H:%M:%SZ",
                            )
                            service_data["name"].append(name)
                            service_data["version"].append(
                                app["spec"]["source"]["targetRevision"]
                            )
                            service_data["ready"].append(is_ready)
                            service_data["deployed"].append(
                                datetime.strftime(time_stamp, TIME_FORMAT)
                            )

        services_df = polars.from_dict(service_data)

        if running_only:
            services_df = services_df.filter(polars.col("ready").eq(True))
        return ServicesDataFrame(services_df)

    def _check_service(self, service_name: str):
        """
        validate that there is a app with the given service_name
        """
        services_list = self._get_services(running_only=False)["name"]
        if service_name in services_list:
            pass
        else:
            raise CommandError(f"Service '{service_name}' not found in {self.target}")

    def _validate_target(self):
        """
        Verify we have a good namespace that exists in the cluster
        """
        cmd = f"argocd app get {self._target}"
        try:
            shell.run_command(cmd, error_OK=False)
        except ShellError as e:
            if "code = Unauthenticated" in str(e):
                raise CommandError("Not authenticated to argocd server") from e
            elif "code = PermissionDenied" in str(e):
                raise CommandError(f"Target '{self._target}' not found") from e
            else:
                raise
