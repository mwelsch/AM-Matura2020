# Overleaf Backup Solution

## Requirements
* Chrome-Browser installed
* Compatible [ChromeDriver](https://chromedriver.chromium.org/downloads) installed and added to system-path
* Python-packages from `requirements.txt`
## Building

First clone or download the repository.  Then run following command in the project directory to create a executable compatible with your OS:

```
pyinstaller --onefile obs.py
```

It should create a `build` and `dist` directory and a `.spec` file. The created executable is located in the `dist` directory. Add this directory to your system-path.

## Usage

Create a directory where you want to backup your LaTeX-project from Overleaf. 

In the directory run the following command:

```
obs init
```

This will initialize a new git-project and create a `config.json` and a `.gitignore` file. 

The `config.json` file stores your Overleaf-credentials and also contains the name of the document you want to backup. As the next step enter your credentials in the following form:

```json
{
  "email": "<your@mail>",
  "password": "<password>",
  "document": "<document_title>"
}
```

**Note** - Don't worry, `config.json` will not be stored in your repository later on. It is included in the `.gitignore` file. 

The next step is to add your remote-repository to git. This is normally done via:

```
git remote add origin <your_remote_url>
```

**Note** - This step can be eliminated if you use `obs init "<your_remote_url>"`.

---

Now you can backup your document  in the same directory with:

```
obs do
```

This will open an automatic chrome-instance that will do everything for you:

* Log in to Overleaf
* Download the document
* Unzip it
* Adding & committing the files to git 
* Push changes to the remote-repository

To add a custom commit-message use `obs do "<your message here>"`.

## Sources
* [Fix your Chromedriver](https://stackoverflow.com/a/52108199)
* [Wait for download to complete](https://stackoverflow.com/a/48267887)
* [How to XPath](https://www.dvdheiden.nl/2013/11/xpath-select-parent-by-child-attribute/)
* [Turn it on and off again - fixes site loading  (sometimes)](https://www.youtube.com/watch?v=p85xwZ_OLX0)