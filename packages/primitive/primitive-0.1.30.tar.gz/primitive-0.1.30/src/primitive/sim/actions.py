from pathlib import Path, PurePath
from primitive.utils.actions import BaseAction
from loguru import logger
import subprocess
from typing import Tuple
from ..utils.files import find_files_for_extension
import os
from .vcd import TokenKind, tokenize
import io
from collections import defaultdict
import json
import xml.etree.ElementTree as ET


class Sim(BaseAction):
    def execute(
        self, source: Path = Path.cwd(), cmd: Tuple[str] = ["make"]
    ) -> Tuple[bool, str]:
        logger.debug(f"Starting simulation run for source: {source}")

        os.chdir(source)
        logger.debug(f"Changed to {source}, starting sim run")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, env=os.environ)
        except FileNotFoundError:
            message = f"Did not find {cmd}"
            logger.error(message)
            return False, message

        logger.debug("Sim run complete.")

        message = ""
        if result.stderr:
            logger.error("\n" + result.stderr)
        if result.stdout:
            logger.info("\n" + result.stdout)
        message = "See above logs for sim output."

        if result.returncode != 0:
            if not self.primitive.DEBUG:
                message = result.stderr
            return False, message
        else:
            message = "Sim run successful."

        return True, message

    def upload_file(self, path: Path, prefix: str) -> str:
        file_upload_response = self.primitive.files.file_upload(path, key_prefix=prefix)
        return file_upload_response.json()["data"]["fileUpload"]["id"]

    def collect_artifacts(self, source: Path, job_run_id: str) -> None:
        # Parse VCD artifacts
        # files = find_files_for_extension(source, ".vcd")
        # for file in files:
        #     self.parse_vcd(path=file)

        # Parse XML artifacts
        files = find_files_for_extension(source, "results.xml")
        for file in files:
            self.parse_xml(path=file)

        logger.debug("Uploading additional artifacts...")
        # TODO: Figure out how to track ".log", ".history" files w/ analog stuff involved
        file_ids = []
        files = find_files_for_extension(
            source,  # ("results.xml", ".vcd", ".vcd.json", ".xml.json")
            ("results.xml", ".xml.json"),
        )
        for file_path in files:
            try:
                file_ids.append(
                    self.upload_file(
                        file_path,
                        prefix=f"{job_run_id}/{str(PurePath(file_path).relative_to(Path(source)).parent)}",
                    )
                )
            except FileNotFoundError:
                logger.warning(f"{file_path} not found...")

        logger.debug("Updating job run...")
        if len(file_ids) > 0:
            job_run_update_response = self.primitive.jobs.job_run_update(
                id=job_run_id, file_ids=file_ids
            )
            logger.success(job_run_update_response)

    def parse_xml(self, path: Path) -> None:
        results = ET.parse(path)
        testsuites = results.getroot()

        parsed_results = {}
        testsuites_name = testsuites.attrib["name"]
        parsed_results[testsuites_name] = {}

        for testsuite in testsuites.findall("testsuite"):
            testsuite_name = testsuite.attrib["name"]
            parsed_results[testsuites_name][testsuite_name] = {
                "properties": {},
                "testcases": {},
            }
            props = parsed_results[testsuites_name][testsuite_name]["properties"]
            testcases = parsed_results[testsuites_name][testsuite_name]["testcases"]

            for prop in testsuite.findall("property"):
                props[prop.attrib["name"]] = prop.attrib["value"]

            for testcase in testsuite.findall("testcase"):
                testcases[testcase.attrib["name"]] = {
                    attr_key: attr_val for attr_key, attr_val in testcase.attrib.items()
                }

                failures = testcase.findall("failure")

                if len(failures) > 0:
                    for failure in failures:
                        testcases[testcase.attrib["name"]]["status"] = {
                            "conclusion": "failure",
                            "message": failure.attrib["message"],
                        }
                else:
                    testcases[testcase.attrib["name"]]["status"] = {
                        "conclusion": "success",
                        "message": "",
                    }

        # Write parsed file
        data_path = path.parent / f"{path.name}.json"
        with open(data_path, "w") as f:
            f.write(json.dumps(parsed_results))

    def parse_vcd(self, path: Path) -> None:
        logger.debug("Parsing VCD file...")
        with open(path, "rb") as f:
            tokens = tokenize(io.BytesIO(f.read()))

        metadata = defaultdict(dict)
        header = defaultdict(dict)
        data = defaultdict(list)

        active_scope = header
        previous_scope = None

        current_time = 0

        for token in tokens:
            match token.kind:
                case TokenKind.TIMESCALE:
                    metadata["timescaleUnit"] = token.data.unit.value
                    metadata["timescaleMagnitude"] = token.data.magnitude.value
                case TokenKind.SCOPE:
                    scope_type = str(token.data.type_)
                    scope_ident = token.data.ident
                    key = f"{scope_type}:{scope_ident}"
                    active_scope[key] = {}

                    previous_scope = active_scope
                    active_scope = active_scope[key]
                case TokenKind.UPSCOPE:
                    active_scope = previous_scope
                case TokenKind.VAR:
                    active_scope[token.data.id_code] = {
                        "id_code": token.data.id_code,
                        "var_type": str(token.data.type_),
                        "var_size": token.data.size,
                        "reference": token.data.reference,
                        "bit_index": str(token.data.bit_index),
                    }
                case TokenKind.CHANGE_TIME:
                    current_time = int(token.data)
                case TokenKind.CHANGE_SCALAR:
                    data[token.data.id_code].append(
                        (str(current_time), str(token.data.value))
                    )
                case TokenKind.CHANGE_VECTOR:
                    data[token.data.id_code].append(
                        (str(current_time), str(token.data.value))
                    )

        # Add traces and write files
        logger.debug("Writing traces...")

        # Find name of file for json dumps
        file_name = path.name.split(".")[0]

        # Write metadata file
        metadata_path = path.parent / f"{file_name}.metadata.vcd.json"
        with open(metadata_path, "w") as f:
            f.write(json.dumps(metadata))

        # Write header file
        header_path = path.parent / f"{file_name}.header.vcd.json"
        with open(header_path, "w") as f:
            f.write(json.dumps(header))

        # Write data file
        data_path = path.parent / f"{file_name}.data.vcd.json"
        with open(data_path, "w") as f:
            f.write(json.dumps(data))
