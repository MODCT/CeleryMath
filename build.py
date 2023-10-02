"""
Description: build script, using nuitka
Author: Rainyl
LastEditTime: 2022-08-04 17:33:48
"""
import os
import re
from argparse import ArgumentParser
from pathlib import Path

import toml
from py7zr import FILTER_LZMA2, PRESET_DEFAULT, SevenZipFile

project = toml.load(Path(__file__).parent / "pyproject.toml")
__version__ = project["tool"]["poetry"]["version"]


CPUS: int = os.cpu_count()  # type: ignore


def publish_to_7z(build_dir: str, version: str):
    print("Compressing...")
    working_dir = Path(f"{build_dir}/CeleryMathGui.dist/")
    exclude_pattern = re.compile(r"qtwebengine_devtools_resources")
    for file in working_dir.glob("**/*"):
        if exclude_pattern.search(str(file)):
            os.remove(file)
            print(f"Pattern mached, remove {file}")

    save_7z_name = f"{build_dir}/CeleryMath-v{version}-Windows_x64.7z"
    filters = [{"id": FILTER_LZMA2, "preset": PRESET_DEFAULT}]
    with SevenZipFile(save_7z_name, "w", filters=filters, mp=True) as archive:
        archive.writeall(working_dir, arcname="CeleryMath")
    print(f"Publish successfully, saved to {save_7z_name}")


def main(version: str, enable_debug: bool = False, jobs: int = CPUS):
    # std_out = "--force-stdout-spec=celerymath_out.log "
    # std_err = "--force-stderr-spec=celerymath_error.log "
    std_out = ""
    std_err = ""
    console = "--disable-console "
    build_dir = "build"
    debug = ""
    if enable_debug:
        console = "--enable-console "
        build_dir = "build_debug "
        std_out = ""
        std_err = ""
        # debug = "--debug "
    cmd = (
        "nuitka "
        # "--clang "
        "--mingw64 "
        # "--recompile-c-only "
        "--standalone "
        f"{debug} "
        f"--output-dir={build_dir} "
        # "--follow-imports "
        f"{console} "
        f"{std_out} "
        f"{std_err} "
        f"--jobs={jobs} "
        "--file-description=CeleryMath "
        "--company-name=rainyl@MODCT.org "
        f"--product-version={version} "
        f"""--product-name="CeleryMath_v{version}" """
        """--copyright="Copyright © 2022-2023. MODCT All Rights Reserved." """
        # "--show-progress "
        # "--show-memory  "
        "--plugin-enable=pyside6 "
        # "--plugin-enable=matplotlib "
        # "--plugin-enable=multiprocessing "
        # "--plugin-enable=upx "
        "--user-package-configuration-file=cm.nuitka-package.config.yml "
        "--windows-icon-from-ico=resources/icons/logo.ico "
        "./CeleryMathGui.py "
        # "test.py "
    )

    os.system(cmd)

    # make directories and copy necessary files
    mkdirs = [
        Path(f"{build_dir}/CeleryMathGui.dist/conf"),
    ]
    for path in mkdirs:
        if not path.exists():
            print(f"Making directory: {path}")
            path.mkdir(parents=True)

    # # compress using 7z
    publish_to_7z(build_dir, version)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-v", dest="version", type=str)
    parser.add_argument(
        "--debug",
        dest="debug",
        action="store_true",
        help="enable build for debug",
    )
    parser.add_argument("-j", dest="jobs", type=int, default=CPUS)
    args = parser.parse_args()
    # if provide version manully, use the provided version number
    args.version = args.version or __version__

    main(version=args.version, enable_debug=args.debug, jobs=args.jobs)
