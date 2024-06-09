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
    def __init__(self, verb: str = "up"):
        self.compose_files = [
            "Deployment/compose.yml"
        ]
        self.verb = verb
        self.verb_additional_flags = {
            "up": "--build"
        }

    def run(self):
        click.echo(click.style(f"Running docker-compose {self.verb}...", fg="green"))


        # cd to root project directory(git root dir)
        git_root = git("rev-parse", "--show-toplevel").strip()
        os.chdir(git_root)

        # click.echo(click.style(f"cwd: {os.getcwd()}", fg="yellow"))

        compose_files_cmdpart = " ".join([f"-f {file}" for file in self.compose_files])

        os.system(f"docker-compose -p gebwai {compose_files_cmdpart} --project-directory . {self.verb} {self.verb_additional_flags.get(self.verb, '')}")

@click.command()
@click.argument("verb", default="up")
def main(verb: str):
    compose_cmd = ComposeCmd(verb)
    compose_cmd.run()

if __name__ == "__main__":
    main()
