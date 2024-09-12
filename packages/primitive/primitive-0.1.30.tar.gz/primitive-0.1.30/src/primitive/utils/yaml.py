from pathlib import Path


def generate_script_from_yaml(yaml_config: dict, slug: str, destination: Path) -> None:
    commands_blocks = []
    if steps := yaml_config[slug]["steps"]:
        for step in steps:
            commands_blocks.append(step["run"])

    script = f"""
#!/bin/bash

{"".join(commands_blocks)}
    """

    output_path = Path(destination / "run.sh")
    with open(output_path, "w") as f:
        f.write(script)

    # Apply execute file permissions
    output_path.chmod(0o744)

    return output_path
