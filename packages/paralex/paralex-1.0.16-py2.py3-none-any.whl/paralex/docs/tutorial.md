This workflow tutorial takes you through the steps in order to create a paralex lexicon.

## Creating the dataset

Creating the data is of course the hardest task. You have full freedom to do this in whatever way feels most practical or convenient for you and your team.
This might mean editing csv files directly in LibreOffice Calc or Microsoft Excel,
manipulating raw data using a programming language like R or Python, relying on some sort of database manager with a graphical interface, or anything else you can think of.
Before publication, you need to be able to export each table in `csv` format with a
utf-8 character encoding.

The set of expected tables are described in the [description of the standard](standard.md).
Minimally, you should
have a forms table which documents forms, and has at least the three columns
`form_id`, `lexeme`, `cell` and `phon_form` (or `orth_form`). The standard also specified
the
following tables:

- a `lexemes` table to document lexeme-level information such as inflection class.
- a `cells` table to document the meaning of each cell identifier,
- a `features` table to document the meaning of each feature in the each cell,
- a `sounds` table to document the conventions used to write the `phon_form`,
- a `grapheme` table to document the conventions used to write the `orth_form`,
- a `tags` table to document the labels for sets of forms related by properties such
  as overabundant series, defectivity type, dialectal variants, or data quality.

If you provide many lexemes and cells, the forms table can grow very big. In such a case, the [frictionless specification](https://specs.frictionlessdata.io/data-resource/#data-in-multiple-files) allows the tables to be separated in several chunks, provided that they have the exact same data structure.

See [specs](specs.md) for the detail of expected tables and columns. Any additional
ad-hoc tables and columns can be added as necessary.

## Metadata quick start


The python package `paralex` allows you to then generate
additional [metadata](metadata.md) in accordance with the standard automatically. It will
create a single metadata file with a name ending in *.package.json*. You should then
A paralex package is the set of all your tables, documentation, joined with this `json` file.


First, you need to install `paralex`. This can be done from the command line, for example as follows:

```bash title="Installing paralex"
pip3 install paralex
```

Let's assume you have a single table of data, documenting Vulcan verbal paradigms. First, create a configuration file looking like this: 


```yaml title="paralex-infos.yml"
title: Vulcan Verbal Paradigms
tables:
  forms:
    path: "vulcan_v_forms.csv"
name: vulcan
```
This configuration file provides a title for your paralex dataset, a short name (in lowercase), and a single table for forms, with the path to the file holding that csv table. You can now generate the metadata, to be placed in a file `vulcan.package.json` automatically, by executing:


```bash title="Generating metadata"
paralex meta paralex-infos.yml
```

This is enough to obtain a well formed paralex dataset.

The example above is minimal: a title for the package and at least a paradigm table
with a specific path is necessary. However, we recommend you add more information. In particular, provide a full text citation specifying how you wish your
dataset to be cited, a list of collaborators following the [frictionless specification](https://specs.frictionlessdata.io/), a license, a DOI identifier. Moreover, you can add further tables. Here is an example with more metadata, and a full list of five tables, including `vulcan_v_cells.csv`, `vulcan_v_features.csv`, `vulcan_v_lexemes.csv`, `vulcan_v_sounds.csv`. The forms table has also been devided into subtables:

```yaml title="paralex-infos.yml"
title: Vulcan Verbal Paradigms
tables:
  cells:
    path: vulcan_v_cells.csv
  features-values:
    path: vulcan_v_features.csv
  forms:
    path:
    - vulcan_v_forms.csv
    - vulcan_v_forms2.csv
  lexemes:
    path: vulcan_v_lexemes.csv
  sounds:
    path: vulcan_v_sounds.csv
name: vulcan
citation: Spock (2258). Vulcan Verbal Paradigms dataset. Online.
contributors:
- role: author
  title: Spock
id: http://dx.doi.org/S.179-276.SP
keywords:
- vulcan
- paradigms
licenses:
- name: CC-BY-SA-4.0
  path: https://creativecommons.org/licenses/by-sa/4.0/
  title: Creative Commons Attribution Share-Alike 4.0
version: 1.0.2
```


## Advanced metadata

### Custom columns 

For any columns already defined in the [specification](specs.md), rich metadata is automatically generated, including a column name, title and description, its expected type, and potential constraints. This is nested in the `<dataset>.package.json` file. For example, the metadata for the lexeme column from the forms table looks as follows:

```json
{
  "name": "lexeme",
  "type": "string",
  "title": "Reference to a lexeme identifier",
  "description": "Lexeme identifiers must be unique to paradigms.",
  "constraints": {
    "required": true
  },
  "rdfProperty": "https://www.paralex-standard.org/paralex_ontology.xml#lexeme"
}
```

The Paralex standard accomodates user-defined columns on top of pre-defined ones. For these columns, very little metadata can be inferred automatically. For example, imagine we have a `consonantal` column in the `sounds` table, coding whether each sound is a consonant or not. Since it is not pre-defined in the standard, the only inferred metadata would be:

```json

{
  "name": "consonantal",
  "type": "any"
}
```

It is possible to inject more detailed metadata by adding a "schema" key under a specific table in the config file. 
The syntax of the schema section follows the `frictionless` standard, eg: 

```yaml title="paralex-infos.yml"
title: Vulcan Verbal Paradigms
tables:
tables:
  cells:
    path: vulcan_v_cells.csv
  features-values:
    path: vulcan_v_features.csv
  forms:
    path:
    - vulcan_v_forms.csv
    - vulcan_v_forms2.csv
  lexemes:
    path: vulcan_v_lexemes.csv
  sounds:
    path: vulcan_v_sounds.csv
    schema:
      fields:
      - constraints:
          required: true
        description: Binary feature (1/0) indicating whether the segment is a consonant
        falseValues:
        - '0'
        name: consonantal
        title: Whether the segment is a consonant
        trueValues:
        - '1'
        type: boolean
name: vulcan
citation: Spock (2258). Vulcan Verbal Paradigms dataset. Online.
contributors:
- role: author
  title: Spock
id: http://dx.doi.org/S.179-276.SP
keywords:
- vulcan
- paradigms
licenses:
- name: CC-BY-SA-4.0
  path: https://creativecommons.org/licenses/by-sa/4.0/
  title: Creative Commons Attribution Share-Alike 4.0
version: 1.0.2
```

To find the definitions and format of the column metadata, see the [fields descriptors](https://specs.frictionlessdata.io/table-schema/#field-descriptors) in the Frictionless specifications.

### Custom tables

Similarly, some metadata will be missing if using custom tables. In particular, one often needs to specify which column is an **identifier** (or **primary key**), and which columns refer to other ones. This is also done by specifying the schema of these tables in the config file. For example, imagine that in addition to lexemes, we have added a flexeme table, which provides a different partition of forms into paradigms. This is done through a `flexeme` column in the forms table, which refers to identifiers in the `flexeme` table. Thus, we need to add three things in the schemas.

In the forms schema, we need to define the column, as shown above, as well as the foreign key relation to the flexeme table:

```yaml title="excerpt of paralex-infos.yml" 
...
tables:
 ...
  forms:
    path:
    - vulcan_v_forms.csv
    - vulcan_v_forms2.csv
    schema:
      foreignKeys:
      - field: flexeme
        reference:
          resource: flexemes
          field: flexeme_id
      fields:
      - name: flexeme
        title: reference to a flexeme identifier
        description: A flexeme to which a form belongs.
        type: string
        constraints:
          required: true
...
```

In the flexeme schema, we define the `flexeme_id` column (we would probably need to define more columns), and declare it as the identifier (primary key):

```yaml title="excerpt of paralex-infos.yml"
...
tables:
  ...
  flexemes:
      path: vulcan_v_flexemes.csv
      schema:
        primaryKey: flexeme_id
        fields:
        - name: flexeme_id
          title: identifier for a flexeme
          description: the flexeme id identifies a single flexeme
          type: string
          constraints:
            required: true
...
```

The entire configuration is starting to get long:

```yaml title="paralex-infos.yml"
title: Vulcan Verbal Paradigms
tables:
  cells:
    path: vulcan_v_cells.csv
  forms:
    path:
    - vulcan_v_forms.csv
    - vulcan_v_forms2.csv
    schema:
      foreignKeys:
      - field: flexeme
        reference:
          resource: flexemes
          field: flexeme_id
      fields:
      - name: flexeme
        title: reference to a flexeme identifier
        description: A flexeme to which a form belongs.
        type: string
        constraints:
          required: true
  features-values:
    path: vulcan_v_features.csv
  lexemes:
    path: vulcan_v_lexemes.csv
  sounds:
    path: vulcan_v_sounds.csv
    schema:
      fields:
      - name: consonantal
        type: boolean
        title: Whether the segment is a consonant
        description: Binary feature (1/0) indicating whether the segment is a consonant
        trueValues:
        - '1'
        falseValues:
        - '0'
        constraints:
          required: true
  flexemes:
    path: vulcan_v_flexemes.csv
    schema:
      primaryKey: flexeme_id
      fields:
      - name: flexeme_id
        title: identifier for a flexeme
        description: the flexeme id identifies a single flexeme
        type: string
        constraints:
          required: true
citation: Spock (2258). Vulcan Verbal Paradigms dataset. Online.
version: 1.0.2
keywords:
- vulcan
- paradigms
id: http://dx.doi.org/S.179-276.SP
contributors:
- title: Spock
  role: author
licenses:
- name: CC-BY-SA-4.0
  title: Creative Commons Attribution Share-Alike 4.0
  path: https://creativecommons.org/licenses/by-sa/4.0/
```

### More custom manipulations

You can also write your own python script, calling `paralex.paralex_factory`, the argument of which reflect the structure of the config file: first a title, then a list of tables, then optional arguments name, citation, contributors, id, keywords, licenses and version. The factory returns a `frictionless` `Package` object, which can then be written to disk. This is more flexible, as you can then modify the Package object as you like:
    
```python title="gen-metadata.py"
from paralex import paralex_factory
package = paralex_factory("Vulcan Verbal Paradigms", {"forms": {"path": "vulcan_v_forms.csv"}})
package.to_json("vulcan.package.json")
```

## Ensuring high quality data

### Frictionless validation

The metadata generated above, and saved in the json file `vulcan.package.json` can now be used to [validate the dataset using frictionless](https://frictionlessdata.io/software/#software-toolkit). Frictionless should have been installed as a dependency when you installed `paralex`. You can now run:

```bash title="Checking against the metadata"
frictionless validate vulcan.package.json
```

This will check that all the tables exist and are well formed, and that columns
contain the types and contents declared by the metadata file, and that any constraints
on columns (such as being a value from a specific set of predefined values, being
unique, being obligatory, having maximum or minimum values, etc) are respected. Note that
the following requirements will also be checked for:

- All identifiers MUST be unique, that is to say, no two rows in their table has the
  same value in `form_id`, `cell_id`, `lexeme_id`, `feature_id`, or `sound_id`.
- All values in the `cell` column of the forms MUST correspond to an identifier in
  `cell_id` of the `cells` table if it exists;
- All values in the `lexeme` column of the forms MUST correspond to an identifier
  in `lexeme_id` of the `lexemes` table if it exists
- If there is a `sounds` table, then the `phon_form` in `forms` MUST be
  composed
  only of sound identifiers and spaces.
- If there is a `cells` table and a `features` table, then the `cell_id` in `cells`
  MUST be composed only of feature identifiers found in `feature_id`, separated by dots, following the Leipzig glossing rules convention.

### Paralex validation

Any frictionless dataset can be checked against its metadata. In addition, to check that the dataset is in fact a paralex lexicon, you can use the `paralex validate` command as follows:

```bash title="Checking against the standard itself"
paralex validate vulcan.package.json
```

This attempts to check all of the MUST and SHOULD statements from the [standard](standard.md). 

### Testing

In addition, you might want to check or to constrain additional properties of the data. Some constraints can be expressed in the package metadata, see the [frictionless doc on constraints](https://specs.frictionlessdata.io/table-schema/#constraints).

For more checks, we recommend writing
*tests* in the programming language of your choice, which read the data and automatically verify sets of expected properties. For example, you might want to check:

- That the number of rows in each table conforms to your expectations (thereby checking that you did not add rows anywhere by mistake)
- Complex verifications on the phonological form (this serves to avoid obvious mistakes in the phonemic transcriptions), for example ensuring that every word has a stress marker.
- Logical properties: for example, that defective forms do not have positive frequencies (if that is relevant !)
- etc.

### Continuous pipelines

Validation and testing can be setup to run each time the data changes, if you track your data using git and push it either to gitlab or github.


=== "Pipelines with gitlab"
    
    With gitlab, create a plain text file called `.gitlab-ci.yml`, with the following content:

    ``` yaml title=".gitlab-ci.yml"
    image: python:3.8
    
    validate:
      stage: test
      script:
        - pip install frictionless paralex
        - frictionless validate *.package.json
        - paralex validate *.package.json
    ```

## Publishing

### The raw data files

We recommend publishing the completed dataset as an online repository, such as on github or gitlab.

The repository should contain:

- the data, in the form of csv tables
- the metadata, in the form of a json file (this is a frictionless _package_ file)
- the documentation files, at the minimum a README.md file
- a license file
- the code:
    - the config file `paralex-infos.yml` or the metadata python script `gen-metadata.py`
    - the tests if they exist
    - when possible, legal, and practical: a link to any automated process used to generate the data, or any related repository used to generate it.

When using git, a simple way to do this is the `git archive` command. For example, the following command will create a zip archive for a repository at the current revision (HEAD):

```shell
git archive -o vulcan_verbs.zip HEAD
```

It is possible to include just a sub-folder in the archive, for example if the sub-folder is called `distrib`:

```shell
git archive -o vulcan_verbs.zip HEAD distrib
```

Only files versionned with git will be included, but they will all be included. To exclude some files, use a [`.gitattributes` file](https://git-scm.com/docs/gitattributes). Here is an example:

```gitexclude title=".gitattributes"
.zenodo.json       export-ignore
.gitlab-ci.yml     export-ignore
.gitattributes     export-ignore
.gitignore     export-ignore
mkdocs.yml     export-ignore
```

### Revisable, automatically generated sites

You can use [mkdocs-paralex](https://pypi.org/project/mkdocs-paralex-plugin/) to generate a website automatically using [mkdocs](https://www.mkdocs.org/). This software is currently in beta mode: it is not stable and might have critical bugs. If you find any, please make issues or write us an email.

Your repository needs to have pipelines and pages enabled. 

First, create a configuration file for [mkdocs](https://www.mkdocs.org/user-guide/), compatible with [mkdocs-material](https://squidfunk.github.io/mkdocs-material/). 

It needs a special `paralex` section, with minimally a `paralex_package_path` (to the json file), lists of feature labels to use to separate tables, rows and columns. It can contain 

``` yaml title="mkdocs.yml"
site_name: "My site name"
docs_dir: docs
plugins:
  - paralex:
      paralex_package_path: "<name>.package.json"
      layout_tables:
        - mood
      layout_rows:
        -  person/number
      layout_columns:
        - tense
repo_url: https://gitlab.com/<user>/<repo>
```

If your lexicon is massive, the generated site might exceed the free hosting capacity on gitlab or github. You can then add two more keys under the paralex section. If `sample_size` is set, the corresponding number of lexemes will be selected, and the site will only show that sample. If `frequency_sample` is set to `true`, then the chosen lexemes will be the most frequent.

``` yaml title="mkdocs.yml"
site_name: "My site name"
docs_dir: docs
plugins:
  - paralex:
      paralex_package_path: "<name>.package.json"
      sample_size: 5000
      frequency_sample: true
      layout_tables:
        - mood
      layout_rows:
        -  person/number
      layout_columns:
        - tense
repo_url: https://gitlab.com/<user>/<repo>
```

To generate the site, add a pipeline file:

=== "gitlab pages"
    
    With gitlab, create a plain text file called `.gitlab-ci.yml`, with the following content. The site will then be served at `https://<username>.gitlab.io/<repository-name>`. For more on gitlab pages, see [the gitlab pages docs](https://docs.gitlab.com/ee/user/project/pages/). 

    ``` yaml title=".gitlab-ci.yml"
    image: python:3.8

    pages:
      stage: deploy
      script:
        - mkdir -p docs/
        - pip install pandas mkdocs>=1.1.2 mkdocs-material mkdocs_paralex_plugin
        - mkdocs build -d public/ --strict --verbose
      artifacts:
        paths:
          - public/
      only:
        - master
    ```

Here are some examples of such generated sites:

- [Eesthetic: Estonian N and V](https://sbeniamine.gitlab.io/estonianparadigms/)
- [Aravelex: Arabic V](https://sbeniamine.gitlab.io/aravelex)
- [VeLePo: European Portuguese V](https://sbeniamine.gitlab.io/europeanportugueseverbs/)
- [Vlexique: French V](https://sbeniamine.gitlab.io/vlexique)


## Archiving

We recommend archiving the data by creating a record on some archival service, for
example [zenodo](https://zenodo.org/). A good practice would be to set up automatic
archives for new versions. This can be done natively from github, or can be done using
[gitlab2zenodo](https://pypi.org/project/gitlab2zenodo/).

To have a DOI generated by zenodo in the metadata, first make a draft deposit, filling in the metadata, and checking the box for pre-registering a DOI. Then copy this DOI, add it to your README.md file and your metadata, generate an archive, and upload this to zenodo before publishing the record.

To have your dataset officially listed as a paralex lexicon, add it to the [Paralex zenodo community](https://zenodo.org/communities/paralex/)

