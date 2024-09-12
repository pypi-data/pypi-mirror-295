import platform
import sys
from pathlib import Path
from time import sleep
from primitive.utils.actions import BaseAction
from loguru import logger
from primitive.__about__ import __version__
import yaml
from ..utils.yaml import generate_script_from_yaml

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


class Agent(BaseAction):
    def set_cache_dir(self):
        os_family = platform.system()

        if os_family == "Darwin":
            self.cache_dir = Path(
                Path.home() / "Library" / "Caches" / "tech.primitive.agent"
            )
        elif os_family == "Linux":
            self.cache_dir = Path(Path.home() / ".cache" / "primitive")
        elif os_family == "Windows":
            raise NotImplementedError("Windows is not currently supported.")
            self.cache_dir = None

        if not self.cache_dir.exists():
            self.cache_dir.mkdir(parents=True, exist_ok=True)

    def execute(
        self,
    ):
        logger.enable("primitive")
        logger.info(" [*] primitive")
        logger.info(f" [*] Version: {__version__}")

        # Create cache dir if it doesnt exist
        self.set_cache_dir()

        # self.primitive.hardware.update_hardware_system_info()
        try:
            self.primitive.hardware.check_in_http(is_available=True, is_online=True)
        except Exception as ex:
            logger.error(f"Error checking in hardware: {ex}")
            sys.exit(1)

        try:
            active_reservation_id = None
            active_reservation_pk = None

            while True:
                hardware = self.primitive.hardware.get_own_hardware_details()
                if hardware["activeReservation"]:
                    if (
                        hardware["activeReservation"]["id"] != active_reservation_id
                        or hardware["activeReservation"]["pk"] != active_reservation_pk
                    ):
                        logger.warning("New reservation for this hardware.")
                        active_reservation_id = hardware["activeReservation"]["id"]
                        active_reservation_pk = hardware["activeReservation"]["pk"]
                        logger.debug("Active Reservation:")
                        logger.debug(f"Node ID: {active_reservation_id}")
                        logger.debug(f"PK: {active_reservation_pk}")
                else:
                    if (
                        hardware["activeReservation"] is None
                        and active_reservation_id is not None
                        and hardware["isAvailable"]
                    ):
                        logger.debug("Previous Reservation is Complete:")
                        logger.debug(f"Node ID: {active_reservation_id}")
                        logger.debug(f"PK: {active_reservation_pk}")
                        active_reservation_id = None
                        active_reservation_pk = None

                if not active_reservation_id:
                    sleep_amount = 5
                    logger.debug(
                        f"No active reservation found... [sleeping {sleep_amount} seconds]"
                    )
                    sleep(sleep_amount)
                    continue

                job_runs_data = self.primitive.jobs.get_job_runs(
                    status="pending", first=1, reservation_id=active_reservation_id
                )

                pending_job_runs = [
                    edge["node"] for edge in job_runs_data["jobRuns"]["edges"]
                ]

                if not pending_job_runs:
                    sleep_amount = 5
                    logger.debug(
                        f"Waiting for Job Runs... [sleeping {sleep_amount} seconds]"
                    )
                    sleep(sleep_amount)
                    continue

                for job_run in pending_job_runs:
                    logger.debug("Found pending Job Run")
                    logger.debug(f"Job Run ID: {job_run['id']}")
                    logger.debug(f"Job Name: {job_run['job']['name']}")

                    git_repo_full_name = job_run["gitCommit"]["repoFullName"]
                    git_ref = job_run["gitCommit"]["sha"]
                    logger.debug(
                        f"Downloading repository {git_repo_full_name} at ref {git_ref}"
                    )

                    github_access_token = (
                        self.primitive.jobs.github_access_token_for_job_run(
                            job_run["id"]
                        )
                    )

                    downloaded_git_repository_dir = (
                        self.primitive.git.download_git_repository_at_ref(
                            git_repo_full_name=git_repo_full_name,
                            git_ref=git_ref,
                            github_access_token=github_access_token,
                            destination=self.cache_dir,
                        )
                    )

                    source_dir = downloaded_git_repository_dir.joinpath(
                        job_run["jobSettings"]["rootDirectory"]
                    )

                    cmd = ("make",)
                    if containerArgs := job_run["jobSettings"]["containerArgs"]:
                        cmd = tuple(containerArgs.split(" "))

                    # Load config and generate bash script
                    yaml_config_path = Path(source_dir / "primitive.yaml")
                    run_script_path = None
                    if yaml_config_path.exists() and yaml_config_path.is_file():
                        yaml_config = yaml.load(
                            open(yaml_config_path, "r"), Loader=Loader
                        )

                        job_slug = job_run["job"]["slug"]
                        if job_slug in yaml_config:
                            run_script_path = generate_script_from_yaml(
                                yaml_config,
                                slug=job_slug,
                                destination=source_dir,
                            )
                            cmd = (
                                "/bin/bash",
                                str(run_script_path.resolve()),
                            )

                    match job_run["job"]["slug"]:
                        case "lint":
                            logger.debug("Executing Lint Job")

                            self.primitive.jobs.job_run_update(
                                job_run["id"], status="request_in_progress"
                            )

                            result, message = self.primitive.lint.execute(
                                source=source_dir
                            )
                            if result:
                                conclusion = "success"
                            else:
                                conclusion = "failure"
                            self.primitive.jobs.job_run_update(
                                job_run["id"],
                                status="request_completed",
                                conclusion=conclusion,
                                stdout=message,
                            )

                            logger.debug("Lint Job Completed")
                        case "sim":
                            logger.debug("Executing Sim Job")

                            self.primitive.jobs.job_run_update(
                                job_run["id"], status="request_in_progress"
                            )

                            result, message = self.primitive.sim.execute(
                                source=source_dir, cmd=cmd
                            )

                            # Attempt artifact collection
                            self.primitive.sim.collect_artifacts(
                                source=source_dir, job_run_id=job_run["id"]
                            )

                            if result:
                                conclusion = "success"
                            else:
                                conclusion = "failure"
                            self.primitive.jobs.job_run_update(
                                job_run["id"],
                                status="request_completed",
                                conclusion=conclusion,
                                stdout=message,
                            )

                            logger.debug("Sim Job Completed")

                sleep(5)
        except KeyboardInterrupt:
            logger.info(" [*] Stopping primitive...")
            self.primitive.hardware.check_in_http(is_available=False, is_online=False)
            sys.exit()
