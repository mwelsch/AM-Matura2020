# Overleaf Backup Solution

## Requirements
* Install python packages from `requirements.txt` via `pip install -r requirements.txt`
## Building

First clone or download the repository.  Then run following command in the project directory to create a executable compatible with your OS:

```
pyinstaller --onefile OverleafBackup.py
```

It should create a `build` and `dist` directory and a `.spec` file. The created executable is located in the `dist` directory. Add this directory to your system-path.

## Usage

Create a directory where you want to backup your LaTeX-project from Overleaf. 

In the directory run the following command:

```
OverleafBackup init [<your_remote_git_url>]
```

This will initialize a new git-project and create a `config.json` and a `.gitignore` file. 

The `config.json` file stores your Overleaf-credentials and also contains the name of the document you want to backup. As the next step enter your credentials in the following form:

```json
{
  "email": "<your@mail>",
  "password": "<password>",
  "project_id": "<project_id>"
}
```

**Note** - Don't worry, `config.json` will not be stored in your repository later on. It is included in the `.gitignore` file. 

To find your project id, simply open the project you want to backup in your browser and copy it from the URL, it should be located here:
`https://www.overleaf.com/project/<project_id>`

The next step is to add your remote-repository to git if you haven't done it with the parameter. This is normally accomplished via:

```
git remote add origin <your_remote_git_url>
```

---

Now you can backup your document  in the same directory with:

```
OverleafBackup do
```

This will open an automatic chrome-instance that will do everything for you:

* Log in to Overleaf
* Download the document
* Unzip it
* Adding & committing the files to git 
* Push changes to the remote-repository

To add a custom commit-message use `OverleafBackup do "<your message here>"`.

## Sources
* [Fix your Chromedriver](https://stackoverflow.com/a/52108199)
* [Wait for download to complete](https://stackoverflow.com/a/48267887)
* [How to XPath](https://www.dvdheiden.nl/2013/11/xpath-select-parent-by-child-attribute/)
* [Turn it on and off again - fixes site loading  (sometimes)](https://www.youtube.com/watch?v=p85xwZ_OLX0)
* [Python Requests](https://requests.kennethreitz.org/en/master/)
* [Overleaf Sources](https://github.com/overleaf/overleaf)