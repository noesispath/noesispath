import docker
from fastapi import APIRouter, HTTPException, status
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel
from requests.exceptions import ReadTimeout

router = APIRouter(tags=["Execution"])
client = docker.from_env()


class CodeSubmission(BaseModel):
    code: str
    stdin: str = ""


class ExecutionResult(BaseModel):
    output: str | None
    error: str | None
    status: str
    time: str | None
    memory: int | None


import time as pytime

def _run_in_docker(submission: CodeSubmission) -> ExecutionResult:
    container = None
    runner = (
        "import io, os, sys, time\n"
        "sys.stdin = io.StringIO(os.environ.get('NOESIS_STDIN', ''))\n"
        "code = os.environ.get('NOESIS_CODE', '')\n"
        "exec(compile(code, '<submission>', 'exec'), {'__name__': '__main__'})\n"
        "time.sleep(0.1)\n"
    )

    start_time = pytime.time()
    try:
        container = client.containers.run(
            "python:3.11-slim",
            command=["python", "-c", runner],
            environment={
                "NOESIS_CODE": submission.code,
                "NOESIS_STDIN": submission.stdin,
            },
            mem_limit="128m",
            network_disabled=True,
            detach=True,
            remove=False,
        )

        result = container.wait(timeout=10)
        elapsed = pytime.time() - start_time
        stdout = container.logs(stdout=True, stderr=False).decode("utf-8", errors="replace")
        stderr = container.logs(stdout=False, stderr=True).decode("utf-8", errors="replace")

        # Get memory usage (max RSS in bytes)
        memory = 0
        try:
            stats = container.stats(stream=False)
            mem_stats = stats.get("memory_stats", {})
            memory = int(mem_stats.get("max_usage") or mem_stats.get("usage") or 0)
        except Exception:
            memory = 0

        if result.get("StatusCode", 1) == 0:
            return ExecutionResult(output=stdout or None, error=None, status="Accepted", time=f"{elapsed:.3f}", memory=memory)

        return ExecutionResult(
            output=stdout or None,
            error=stderr or "Execution failed",
            status="Error",
            time=f"{elapsed:.3f}",
            memory=memory,
        )
    except ReadTimeout:
        elapsed = pytime.time() - start_time
        if container is not None:
            try:
                container.kill()
            except docker.errors.APIError:
                pass
        memory = 0
        try:
            stats = container.stats(stream=False)
            mem_stats = stats.get("memory_stats", {})
            memory = int(mem_stats.get("max_usage") or mem_stats.get("usage") or 0)
        except Exception:
            memory = 0
        return ExecutionResult(output=None, error="Execution timed out", status="Time Limit Exceeded", time=f"{elapsed:.3f}", memory=memory)
    except docker.errors.DockerException as exc:
        raise HTTPException(status_code=500, detail=f"Docker execution failed: {exc}") from exc
    finally:
        if container is not None:
            try:
                container.remove(force=True)
            except docker.errors.APIError:
                pass


@router.post("/execute", response_model=ExecutionResult, status_code=status.HTTP_200_OK)
async def execute_code(submission: CodeSubmission):
    return await run_in_threadpool(_run_in_docker, submission)
