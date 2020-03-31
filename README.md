# automation
Scripts to automate manual tasks

## rename_file.py

Analysis the content of a pdf file and renames accordingly. 

For example from a file named `document.pdf` and transforms into `20200401_PaymentRenato_April2020.pdf`.

How to use:
* configure rules in `rename_file.yml`
* define source folder setting OS env var `RENAME_FILES_SOURCE_DIR`
* run `python rename_file.py`
