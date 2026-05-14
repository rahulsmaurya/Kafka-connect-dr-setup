
import subprocess

steps = [
    "python export_connectors.py",
    "python deploy_connectors.py",
    "python validate_connectors.py"
]

for step in steps:

    print(f"Running step: {step}")

    result = subprocess.run(
        step,
        shell=True
    )

    if result.returncode != 0:
        raise Exception(f"Step failed: {step}")

print("DR connector synchronization complete.")
