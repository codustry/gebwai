#!/usr/bin/env scriptisto

# scriptisto-begin
# script_src: script.py
# build_once_cmd: virtualenv -p python3 . && . ./bin/activate && pip install mypy click sh
# build_cmd: . ./bin/activate && mypy script.py && python3 -m compileall . && chmod +x ./run.sh
# target_bin: ./run.sh
# files:
#   - path: run.sh
#     content: |
#       #!/bin/sh
#       export DIR=$(dirname $0)
#       . $DIR/bin/activate
#       python3 $DIR/script.py $@
# scriptisto-end

"""
This script is used to run docker-compose commands.

ref: 
- https://martinheinz.dev/blog/98
"""

import click
import sh # type: ignore
import os

git = sh.Command("git")

class ComposeCmd:
    def __init__(self, verb: str = "up", dryrun: bool = False, dev: bool = False, detach: bool = False):
        self.compose_files = [
            "Deployment/compose.yml",
            "Deployment/compose.tunnel.yml"
        ]
        if dev:
            self.compose_files.append("Deployment/compose.dev.yml")
        self.verb = verb
        self.verb_additional_flags = {
            "up": "--build --remove-orphans "
        }
        if dev:
            self.verb_additional_flags["up"] += "--watch "
        if detach:
            self.verb_additional_flags["up"] += "--detach "
        self.dryrun = dryrun

    def run(self):
        click.echo(click.style(f"Running docker-compose {self.verb}...", fg="green"))


        # cd to root project directory(git root dir)
        git_root = git("rev-parse", "--show-toplevel").strip()
        os.chdir(git_root)

        compose_files_cmdpart = " ".join([f"-f {file}" for file in self.compose_files])

        final_cmd = f"docker-compose -p gebwai {compose_files_cmdpart} --project-directory . {self.verb} {self.verb_additional_flags.get(self.verb, '')}"
        click.echo(click.style(f"Running command: {final_cmd}\ncwd: {os.getcwd()}", fg="yellow"))
        if not self.dryrun:
            os.system(final_cmd)

@click.command()
@click.argument("verb", default="up")
@click.option("--dryrun", is_flag=True, help="Perform a dry run without executing actions", default=False)
@click.option("--dev", is_flag=True, help="Run in development mode", default=False)
@click.option("--detach", is_flag=True, help="Run containers in the background", default=False)
def main(verb: str, dryrun: bool, dev: bool, detach: bool):
    compose_cmd = ComposeCmd(verb, dryrun, dev, detach)
    compose_cmd.run()

if __name__ == "__main__":
    main()
