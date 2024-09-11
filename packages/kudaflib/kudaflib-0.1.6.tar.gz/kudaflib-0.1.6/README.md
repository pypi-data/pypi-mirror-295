# KUDAF Metadata Library

This package contains the following elements: 

1. Metadata schema definitions for the Kudaf platform, adhering to global standards:
  a. DCAT-AP-NO standard: Catalog and Dataset metadata, compatible with the requirements of the Norwegian Fellesdatakatalog
  b. RAIRD standard: Variable metadata

2. A CLI tool to generate KUDAF Metadata.  

It was developed by [Sikt - Kunnskapssektorens tjenesteleverandør](https://sikt.no/) under the [KUDAF initiative](https://sikt.no/tiltak/kudaf-kunnskapssektorens-datafellesskap) to enable a **Data Producer to make small-file data available on the KUDAF data-sharing platform**.  

The CLI can create Catalog, Dataset and Variable-level metadata for the Kudaf data-sharing platform.

---

## About KUDAF

KUDAF - **Kunnskapssektorens datafelleskap** skal sørge for tryggere, enklere og bedre deling av data. [Les mer om KUDAF](https://kunnskapsdata.no/).  
 

### High-level workflow for Data Source administrators (Beta version)

[Fra dataprodusent til datatilbyder](https://kunnskapsdata.no/fra-dataprodusent-til-datatilbyder-2)

[Feide Kundeportal - Datadeling (Nosrk)](https://www.feide.no/datadeling) 


### Data Sharing and the Feide Customer Portal

[Feide - Data Provider How-to](https://docs.feide.no/data_sharing/data_provider/index.html) 

--- 

## Local installation instructions (Linux/Mac)  


### Make sure Python3 is installed on your computer (versions from 3.8 up to 3.11 should work fine)

\$ `python3 --version` 

### Navigate to the folder chosen to contain this project

\$ `cd path/to/desired/folder` 


### Create a Python virtual environment and activate it  

\$ `python3 -m venv .venv` 

This created the virtualenv under the hidden folder `.venv`  

Activate it with: 

\$ `source .venv/bin/activate`  

### Install Kudaf Metadata Tools and other required Python packages 

\$ `pip install kudaflib`  

---

## Creating a YAML configuration file

Click here for a [basic YAML syntax tutorial](https://realpython.com/python-yaml/#yaml-syntax)  


### Example YAML configuration file

The following file is included in the package and can be found in the `kudaflib/config` folder:  

`config_example.yaml`  

```yaml
---
organizations:
- organization: &myorganization
    name: "my-official-organizations-name"
    orgnr: "my-official-organization-number"

catalogs:
- catalog: &mycatalog
    name: "my-FeideKundeportal-Datasource-name"
    description: "description-of-my-catalog"
    organization: *myorganization

datasets:
- dataset: &mydataset
    fileNameExt: mydatafile.csv
    csvParseDelimiter: ";"  # Valgfritt (som standard ","). Angir tegnet som brukes i CSV-filen for å skille verdier innenfor hver rad
    fileDirectory: /path/to/my/datafiles/directory  # Bare nødvendig hvis forskjellig fra gjeldende katalog

unitTypes: 

- MIN_ENHETSTYPE1: &min_enhetstype1  # Bare nødvendig hvis forskjellig fra de globale enhetstypene: PERSON/VIRKSOMHET/KOMMUNE/FYLKE
    shortName: MIN_ENHETSTYPE1  # This shows as the Key indicator in the Front-end
    name: Kort identifikasjonsetikett  # This will label the Identifier blue box
    description: Detaljert beskrivelse av denne enhetstypen
    dataType: LONG  # En av STRING/DATE/LONG/DOUBLE

- MIN_ENHETSTYPE2: &min_enhetstype2  # Bare nødvendig hvis forskjellig fra de globale enhetstypene: PERSON/VIRKSOMHET/KOMMUNE/FYLKE
    shortName: MIN_ENHETSTYPE2  # This shows as the Key indicator in the Front-end
    name: Kort identifikasjonsetikett  # This will label the Identifier blue box
    description: Detaljert beskrivelse av denne enhetstypen
    dataType: LONG  # En av STRING/DATE/LONG/DOUBLE

variables:

- name: VARIABELENS_NAVN
  temporalityType: FIXED  # En av FIXED/EVENT/STATUS/ACCUMULATED
  dataRetrievalUrl: https://my-datasource-api.no/api/v1/variables/VARIABELENS_NAVN
  sensitivityLevel: NONPUBLIC  # En av PUBLIC/NONPUBLIC
  populationDescription: 
  - Beskrivelse av populasjonen som denne variabelen måler
  spatialCoverageDescription:
  - Norge
  - Annen geografisk beskrivelse som gjelder disse dataene
  subjectFields: 
  - Temaer/konsepter/begreper som disse dataene handler om
  identifierVariables:
  - unitType: *min_enhetstype1  # Kan også være en av de globale enhetstypene: PERSON/VIRKSOMHET/KOMMUNE/FYLKE
  measureVariables: 
  - label: Kort etikett på hva denne variabelen måler/viser
    description: Detaljert beskrivelse av hva denne variabelen måler/viser
    dataType: STRING  # En av STRING/LONG/DATE/DOUBLE

- name: VARIABELENS_NAVN_ACCUM
  temporalityType: ACCUMULATED  # En av FIXED/EVENT/STATUS/ACCUMULATED
  dataRetrievalUrl: https://my-datasource-api.no/api/v1/variables/VARIABELENS_NAVN
  sensitivityLevel: NONPUBLIC  # En av PUBLIC/NONPUBLIC
  populationDescription: 
  - Beskrivelse av populasjonen som denne variabelen måler
  spatialCoverageDescription:
  - Norge
  - Annen geografisk beskrivelse som gjelder disse dataene
  subjectFields: 
  - Temaer/konsepter/begreper som disse dataene handler om
  identifierVariables:
  - unitType: *min_enhetstype2  # Kan også være en av de globale enhetstypene: PERSON/VIRKSOMHET/KOMMUNE/FYLKE
  measureVariables: 
  - label: Kort etikett på hva denne variabelen måler/viser
    description: Detaljert beskrivelse av hva denne variabelen måler/viser
    dataType: LONG  # Hvis akkumulerte data må summeres, bør dette enten være en av LONG/DOUBLE

- name: NØKKELVAR_ID-NØKKEL_MÅLE-NOKKEL
  temporalityType: FIXED  # En av FIXED/EVENT/STATUS/ACCUMULATED
  dataRetrievalUrl: https://my-datasource-api.no/api/v1/variables/NØKKELVAR_ID-NØKKEL_MÅLE-NOKKEL
  sensitivityLevel: PUBLIC  # En av PUBLIC/NONPUBLIC
  populationDescription: 
  - Beskrivelse av populasjonen som denne variabelen måler
  spatialCoverageDescription:
  - Norge
  - Annen geografisk beskrivelse som gjelder disse dataene
  subjectFields: 
  - Temaer/konsepter/begreper som disse dataene handler om
  identifierVariables:
  - unitType: *min_enhetstype1  # ID-NØKKEL - Kan også være en av de globale enhetstypene: PERSON/VIRKSOMHET/KOMMUNE/FYLKE
  measureVariables: 
  - label: Kort etikett på hva denne variabelen måler/viser
    description: Detaljert beskrivelse av hva denne variabelen måler/viser
    unitType: *min_enhetstype2  # MÅLE-NØKKEL - Kan også være en av de globale enhetstypene: PERSON/VIRKSOMHET/KOMMUNE/FYLKE
    dataType: LONG  # En av STRING/LONG/DATE/DOUBLE

... 
```

---

## Kudaflib CLI operation

Navigate to the project directory and activate the virtual environment (**only if not already activated**): 

\$ `source .venv/bin/activate`  

The **`kudaf-generate` command** should be now activated. This is the main entry point to the CLI's functionalities.


### Displaying the help menus 

\$ **`kudaf-generate --help`**  
 

    Usage: kudaf-generate [OPTIONS] COMMAND [ARGS]...
    
    Kudaf Metadata Tools                                                                                             
                                                                                                                        
    ╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────╮
    │ --install-completion          Install completion for the current shell.                                          │
    │ --show-completion             Show completion for the current shell, to copy it or customize the installation.   │
    │ --help                        Show this message and exit.                                                        │
    ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
    ╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────╮
    │ metadata            Generate Variables/UnitTypes Metadata                                                        │
    ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

As we can see, there is **one sub-command** available: **`metadata`**. 

We can obtain **help** on it as well: 


\$ **`kudaf-generate metadata --help`**  


    Usage: kudaf-generate metadata [OPTIONS]                                                                           
                                                                                                                        
    Generate Variables/UnitTypes Metadata                                                                              
    JSON metadata files ('variables.json' and maybe 'unit_types.json') will be written to the                          
    (optionally) given output directory.                                                                               
    If any of the optional directories is not specified, the current directory is used as default.                     
                                                                                                                        
    ╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────╮
    │ --config-yaml-path            PATH  Absolute path to the YAML configuration file                                 │
    │                                     [default: /home/me/current/directory/config.yaml]                            │
    │ --output-metadata-dir         PATH  Absolute path to directory where the Metadata files are to be written to     │
    │                                     [default: /home/me/current/directory]                                        │
    │ --help                              Show this message and exit.                                                  │
    ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯


### Generating metadata only from a YAML configuration file 

\$ **`kudaf-generate metadata --config-yaml-path /home/me/path/to/config.yaml --output-metadata-dir /home/me/path/to/metadata/folder`**  


---

## Developers

### Download the package to your computer

#### Option A: Installation from repository:

Open up a Terminal window and clone the repo locally:

\$ `git clone https://gitlab.sikt.no/kudaf/kudaflib.git`  


#### Option B: Installation from source:

1. Open up your **browser** and navigate to the project's GitLab page: **`https://gitlab.sikt.no/kudaf/kudaflib`**  

2. Once there, **download a ZIP file with the source code**  

![Download ZIP file](static/kdst_download.png)

3. Move the zipped file to whichever directory you want to use for this installation

4. Open a **Terminal window and navigate** to the directory where the zipped file is

5. **Unzip the downloaded file**, it will create a folder called `kudaflib-main` 

6. Switch to the newly created folder 

\$ `cd path/to/kudaflib-main` 


### Make sure Python3 is installed on your computer (versions from 3.8 up to 3.11 should work fine)

\$ `python3 --version` 


### Install Poetry (Python package and dependency manager) on your computer 

Full Poetry documentation can be found here: [`https://python-poetry.org/docs/`](https://python-poetry.org/docs/) 

The **official installer** should work fine on the command line for Linux, macOS and Windows: 

\$ `curl -sSL https://install.python-poetry.org | python3 -` 

If the installation was successful, configure this option:

\$ `poetry config virtualenvs.in-project true`   


#### Mac users: Troubleshooting

**In case of errors installing Poetry on your Mac**, you may have to try installing it with `pipx` . But to install that, we need to have `Homebrew` installed first.   

\$ `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"` 

(Homebrew documentation: https://brew.sh/)

Once `Homebrew` is installed, proceed to install `pipx`: 

\$ `brew install pipx` 

\$ `pipx ensurepath` 

Finally, install `Poetry` :

\$ `pipx install poetry` 


### Create a Python virtual environment and activate it  

\$ `python3 -m venv .venv` 

This created the virtualenv under the hidden folder `.venv`  

Activate it with: 

\$ `source .venv/bin/activate`  

### Install Kudaf Datasource Tools and other required Python packages 

\$ `poetry install`  
