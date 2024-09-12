from subprocess import run
from lynq.backendutils.safety.handler import handle

@handle
def pwsh(cmd: str) -> None:
    run(["powershell", "-Command", cmd])