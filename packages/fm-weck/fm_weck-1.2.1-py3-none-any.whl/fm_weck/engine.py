# This file is part of fm-weck: executing fm-tools in containerized environments.
# https://gitlab.com/sosy-lab/software/fm-weck
#
# SPDX-FileCopyrightText: 2024 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

import logging
import shutil
import subprocess
from abc import ABC, abstractmethod
from functools import cached_property, singledispatchmethod
from pathlib import Path
from tempfile import mkdtemp
from typing import List, Optional, Union

from fm_tools.fmdata import FmData, FmImageConfig

from fm_weck.config import Config, parse_fm_data
from fm_weck.image_mgr import ImageMgr

logger = logging.getLogger(__name__)


class NoImageError(Exception):
    pass


class Engine(ABC):
    interactive: bool = False
    add_benchexec_capabilities: bool = False
    image: Optional[str] = None

    def __init__(self, image: Union[str, FmImageConfig]):
        self.image = self._initialize_image(image)
        self.extra_args = {}
        self._engine = None
        self._tmp_output_dir = Path(mkdtemp("fm_weck_output")).resolve()

        self.output_dir = Path.cwd() / "output"
        self.log_file = None

    def __del__(self):
        if self._tmp_output_dir.exists():
            shutil.rmtree(self._tmp_output_dir)

    def get_workdir(self):
        return Path("/home/cwd")

    def set_output_log(self, output_log: Path):
        self.log_file = output_log

    def set_output_files_dir(self, output_log: Path):
        self.output_dir = output_log

    def mount(self, source: str, target: str):
        self.extra_args["mounts"] = self.extra_args.get("mounts", []) + [
            "-v",
            f"{source}:{target}",
        ]

    @abstractmethod
    def benchexec_capabilities(self):
        raise NotImplementedError

    def base_command(self):
        return [self._engine, "run"]

    def interactive_command(self):
        return ["-it"]

    def setup_command(self):
        return [
            "--entrypoint",
            '[""]',
            "--cap-add",
            "SYS_ADMIN",
            "-v",
            f"{Path.cwd().absolute()}:/home/cwd",
            "-v",
            f"{Config().cache_location}:/home/weck_cache",
            "-v",
            f"{self._tmp_output_dir}:/home/output",
            "--workdir",
            str(self.get_workdir()),
            "--rm",
        ]

    def _move_output(self):
        if not self.output_dir.exists():
            self.output_dir.mkdir()
        for file in self._tmp_output_dir.iterdir():
            if file.is_file():
                shutil.copy(file, self.output_dir / file.name)
            elif file.is_dir():
                shutil.copytree(file, self.output_dir, dirs_exist_ok=True)

    def assemble_command(self, command: tuple[str, ...]) -> list[str]:
        base = self.base_command()
        if self.add_benchexec_capabilities:
            base += self.benchexec_capabilities()

        base += self.setup_command()

        if self.interactive:
            base += self.interactive_command()

        for value in self.extra_args.values():
            if isinstance(value, list) and not isinstance(value, str):
                base += value
            else:
                base.append(value)

        _command = self._prep_command(command)
        return base + [self.image, *_command]

    def _prep_command(self, command: tuple[str, ...]) -> tuple[str, ...]:
        """We want to map absolute paths of the current working directory to the
        working directory of the container."""

        def _map_path(p: Union[str, Path]) -> Union[str, Path]:
            if isinstance(p, Path):
                if not p.is_absolute():
                    return p
                if p.is_relative_to(Path.cwd()):
                    relative = p.relative_to(Path.cwd())
                    return self.get_workdir() / relative
                elif p.is_relative_to(Config().cache_location):
                    relative = p.relative_to(Config().cache_location)
                    return Path("/home/weck_cache") / relative
                else:
                    return p
            mapped = _map_path(Path(p))
            if Path(p) == mapped:
                return p
            else:
                return mapped

        return tuple(map(_map_path, command))

    @singledispatchmethod
    def _initialize_image(self, image: str) -> str:
        logger.debug("Initializing image from string %s", image)
        return image

    @_initialize_image.register
    def _from_fm_config(self, fm_config: FmImageConfig) -> str:
        logger.debug("Initializing image from FmImageConfig: %s", fm_config)
        return ImageMgr().prepare_image(self, fm_config)

    @staticmethod
    def extract_image(fm: Union[str, Path], version: str, config: dict) -> str:
        image = config.get("defaults", {}).get("image", None)

        return parse_fm_data(fm, version).get_images().with_fallback(image)

    @staticmethod
    def _base_engine_class(config: Config):
        engine = config.defaults().get("engine", "").lower()

        if engine == "docker":
            return Docker
        if engine == "podman":
            return Podman

        raise ValueError(f"Unknown engine {engine}")

    @singledispatchmethod
    @staticmethod
    def from_config(config: Config) -> "Engine":
        Base = Engine._base_engine_class(config)
        engine = Base(config.from_defaults_or_none("image"))
        return Engine._prepare_engine(engine, config)

    @from_config.register
    @staticmethod
    def _(fm: Path, version: str, config: Config):
        image = Engine.extract_image(fm, version, config)
        Base = Engine._base_engine_class(config)
        engine = Base(image)
        return Engine._prepare_engine(engine, config)

    @from_config.register
    @staticmethod
    def _(fm: str, version: str, config: Config):
        image = Engine.extract_image(fm, version, config)
        Base = Engine._base_engine_class(config)
        engine = Base(image)
        return Engine._prepare_engine(engine, config)

    @from_config.register
    @staticmethod
    def _(fm: FmData, config: Config):
        image = fm.get_images().with_fallback(config.from_defaults_or_none("image"))
        Base = Engine._base_engine_class(config)
        engine = Base(image)
        return Engine._prepare_engine(engine, config)

    @staticmethod
    def _prepare_engine(engine, config: Config) -> "Engine":
        for src, target in config.mounts():
            if not Path(src).exists():
                logger.warning("Mount source %s does not exist. Ignoring it...", src)
                continue
            engine.mount(src, target)

        return engine

    @abstractmethod
    def image_from(self, containerfile: Path) -> "BuildCommand": ...

    class BuildCommand(ABC):
        build_args: List[str] = []

        @abstractmethod
        def __init__(self, containerfile: Path, **kwargs):
            pass

        def base_image(self, image: str):
            self.build_args += ["--build-arg", f"BASE_IMAGE={image}"]
            return self

        def packages(self, packages: list[str]):
            self.build_args += ["--build-arg", f"REQUIRED_PACKAGES={' '.join(packages)}"]
            return self

        def engine(self):
            return [self._engine]

        def build(self):
            cmd = self.engine() + [
                "build",
                "-f",
                self.containerfile,
                *self.build_args,
                ".",
            ]

            logging.debug("Running command: %s", cmd)

            ret = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            tag = ret.stdout.decode().splitlines()[-1].strip()
            logger.info("Built image %s", tag)
            logger.debug("Output of build image was:\n%s", ret.stdout.decode())

            return tag

    def _run_process(self, command: tuple[str, ...] | list[str]):
        if self.log_file is None:
            process = subprocess.Popen(command)
            process.wait()
            return

        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        with self.log_file.open("wb") as f:
            process = subprocess.Popen(command, stdout=f, stderr=f)
            process.wait()

    def run(self, *command: str) -> None:
        if self.image is None:
            raise NoImageError("No image set for engine.")

        command = self.assemble_command(command)
        logger.info("Running: %s", command)
        self._run_process(command)
        self._move_output()


class Podman(Engine):
    def __init__(self, image: Union[str, FmImageConfig]):
        super().__init__(image)
        self._engine = "podman"

    class PodmanBuildCommand(Engine.BuildCommand):
        def __init__(self, containerfile: Path):
            self.containerfile = containerfile
            self._engine = "podman"

    def image_from(self, containerfile: Path):
        return self.PodmanBuildCommand(containerfile)

    def benchexec_capabilities(self):
        return [
            "--annotation",
            "run.oci.keep_original_groups=1",
            "--security-opt",
            "unmask=/proc/*",
            "--security-opt",
            "seccomp=unconfined",
            "-v",
            "/sys/fs/cgroup:/sys/fs/cgroup",
        ]


class Docker(Engine):
    def __init__(self, image: Union[str, FmImageConfig]):
        super().__init__(image)
        logger.debug("Image: %s", self.image)
        self._engine = "docker"

    class DockerBuildCommand(Engine.BuildCommand):
        def __init__(self, containerfile: Path, needs_sudo: bool = False):
            self.containerfile = containerfile
            if needs_sudo:
                self._engine = "sudo docker"
            else:
                self._engine = "docker"

        def engine(self):
            return self._engine.split(" ")

    def image_from(self, containerfile: Path):
        return self.DockerBuildCommand(containerfile, needs_sudo=self._requires_sudo)

    @cached_property
    def _requires_sudo(self):
        """Test if docker works without sudo."""
        try:
            subprocess.run(["docker", "info"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            logger.debug("Docker does not require sudo.")
            return False
        except subprocess.CalledProcessError:
            logger.debug("Docker requires sudo.")
            return True

    def base_command(self):
        if self._requires_sudo:
            return ["sudo", "docker", "run"]
        return ["docker", "run"]

    def setup_command(self):
        return [
            "--entrypoint",
            "/bin/sh",
            "--cap-add",
            "SYS_ADMIN",
            "-v",
            f"{Path.cwd().absolute()}:/home/cwd",
            "-v",
            f"{Config().cache_location}:/home/weck_cache",
            "-v",
            f"{self._tmp_output_dir}:/home/output",
            "--workdir",
            str(self.get_workdir()),
            "--rm",
        ]

    def benchexec_capabilities(self):
        return [
            "--security-opt",
            "seccomp=unconfined",
            "--security-opt",
            "apparmor=unconfined",
            "--security-opt",
            "label=disable",
            "-v /sys/fs/cgroup:/sys/fs/cgroup",
        ]
