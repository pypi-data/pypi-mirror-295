import importlib
import inspect
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Union

from mlflow.pyfunc import PythonModelContext

from mlflow_extensions.serving.engines.base import (
    Command,
    EngineConfig,
    EngineProcess,
    debug_msg,
)
from mlflow_extensions.serving.engines.huggingface_utils import snapshot_download_local


@dataclass(frozen=True, kw_only=True)
class RayServeEngineConfig(EngineConfig):
    ray_script: str
    model_artifact_key: str = field(default="model")
    ray_script_key: str = field(default="ray_script")
    model_requirements: Optional[List[str]] = None

    def _to_run_command(
        self, context: PythonModelContext = None
    ) -> Union[List[str], Command]:
        this_python_executable = sys.executable
        script_path = self._get_script_path()
        return [this_python_executable, script_path]

    def engine_pip_reqs(self, ray_serve_version: str = "2.35.0", **kwargs) -> List[str]:
        return [
            f"ray[serve]=={ray_serve_version}",
            *(self.model_requirements if self.model_requirements else []),
        ]

    def _setup_snapshot(self, local_dir: str = "/root/models") -> Optional[str]:
        try:
            return snapshot_download_local(repo_id=self.model, local_dir=local_dir)
        except Exception as e:
            return None

    def _get_script_path(self):
        # check if script is a python module or a string to a python module or file path
        if self.ray_script.endswith(".py"):
            return self.ray_script
        try:
            if isinstance(self.ray_script, str):
                # If the input is a string, try to import it
                module = importlib.import_module(self.ray_script.split(".")[0])
                if "." in self.ray_script:
                    for part in self.ray_script.split(".")[1:]:
                        module = getattr(module, part)
                else:
                    module = self.ray_script

                    # Get the file path
                if inspect.ismodule(module):
                    return inspect.getfile(module)
                elif inspect.isclass(module):
                    return inspect.getfile(sys.modules[module.__module__])
                else:
                    # If it's a function or method, get its module
                    return inspect.getfile(sys.modules[module.__module__])
        except Exception as e:
            raise ValueError(
                f"Could not find the script file: {self.ray_script}. "
                f"Try providing the full path to the script file."
            )

    def setup_artifacts(self, local_dir: str = "/root/models") -> Dict[str, str]:
        artifacts = {self.ray_script_key: self._get_script_path()}
        local_path = self._setup_snapshot(local_dir)
        if local_path is None:
            return artifacts
        artifacts[self.model_artifact_key] = local_path
        return artifacts

    @staticmethod
    def supported_model_architectures(self) -> List[str]:
        return []


class RayServeEngineProcess(EngineProcess):
    @property
    def engine_name(self) -> str:
        return "ray-serve-engine"

    def health_check(self) -> bool:
        try:
            import ray
            from ray import serve

            ray.init(address="auto", ignore_reinit_error=True)
            for k, v in serve.status().applications.items():
                from ray.serve._private.common import ApplicationStatus

                if v.status != ApplicationStatus.RUNNING:
                    return False
            return True
        except Exception as e:
            debug_msg(f"Error during health check: {e}")
            return False


if __name__ == "__main__":

    proc = RayServeEngineProcess(
        config=RayServeEngineConfig(
            model="custom-model-nothing-to-download",
            ray_script="/Users/sri.tikkireddy/PycharmProjects/mlflow-vllm-flavor/scripts/rayserve_test.py",
        ),
    )

    proc.start_proc(None)
    print(proc.health_check())
    import concurrent.futures

    async def submit_request(session, url):
        async with session.post(
            "http://0.0.0.0:9989/v1/", json={"image_or_text": url}
        ) as response:
            return await response.json()
        # response = proc.oai_http_client.post("/", json={"image_or_text": url})
        # return response.json()

    while True:
        # urls = [
        #     "https://unsplash.com/photos/QtxgNsmJQSs/download?ixid=MnwxMjA3fDB8MXxhbGx8fHx8fHx8fHwxNjM1ODQ0MjY3&w=640",
        #     "https://unsplash.com/photos/QtxgNsmJQSs/download?ixid=MnwxMjA3fDB8MXxhbGx8fHx8fHx8fHwxNjM1ODQ0MjY3&w=640",
        #     "https://unsplash.com/photos/QtxgNsmJQSs/download?ixid=MnwxMjA3fDB8MXxhbGx8fHx8fHx8fHwxNjM1ODQ0MjY3&w=640",
        #     "https://unsplash.com/photos/QtxgNsmJQSs/download?ixid=MnwxMjA3fDB8MXxhbGx8fHx8fHx8fHwxNjM1ODQ0MjY3&w=640",
        #     "https://unsplash.com/photos/QtxgNsmJQSs/download?ixid=MnwxMjA3fDB8MXxhbGx8fHx8fHx8fHwxNjM1ODQ0MjY3&w=640",
        # ]*100
        urls = [
            "what is your name",
            "i want a red purse",
            "i want a black purse",
            "i want lipstick",
        ] * 500
        import asyncio

        import aiohttp

        async def main():
            async with aiohttp.ClientSession() as session:
                tasks = [submit_request(session, url) for url in urls]
                responses = await asyncio.gather(*tasks)
                for response in responses:
                    print(len(response))

        asyncio.run(main())
    proc.stop_proc()
