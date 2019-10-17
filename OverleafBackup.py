import os
import subprocess
import sys
from zipfile import ZipFile

from OverleafDownloader import OverleafDownloader

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        task = sys.argv[1]
        directory = os.getcwd()

        if task == "init":
            obs_conf = ('{\n'
                        '  "email": "<your@mail>",\n'
                        '  "password": "<password>",\n'
                        '  "project_id": "<project_id>"\n'
                        '}')
            with open("config.json", "w+") as config:
                config.write(obs_conf)
            with open(".gitignore", "w+") as gitignore:
                gitignore.write("config.json\n")
                gitignore.write("debug.log\n")
            subprocess.call(["git", "init"])
            if len(sys.argv) >= 3:
                subprocess.call(["git", "remote", "add", "origin", str(sys.argv[2])])

        elif task == "do":
            overleaf = OverleafDownloader()
            overleaf.login()
            overleaf.download()

            # Unzip download and remove zip
            project_id = overleaf.get_project_id()

            backup = ZipFile(project_id + ".zip")
            backup.extractall()
            backup.close()

            os.remove(project_id + ".zip")

            # Create commit message
            if len(sys.argv) >= 3:
                msg = str(sys.argv[2])
            else:
                msg = "Updated " + project_id
            # Add, commit and push
            subprocess.call(["git", "add", "-A"])
            subprocess.call(["git", "commit", "-m", msg])
            subprocess.call(["git", "push", "-u", "origin", "master"])
        else:
            print("Unknown command - Viable commands are:")
            print("\tobs init [remote-repository-url]")
            print("\tobs do [commit-message]")
    else:
        print("No command given - Viable commands are:")
        print("\tobs init [remote-repository-url]")
        print("\tobs do [commit-message]")
