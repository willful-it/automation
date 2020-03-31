import glob
import locale
import logging
import os
from datetime import date

import fitz
import yaml
from dotenv import load_dotenv

RENAME_FILES_SOURCE_DIR_ENV = "RENAME_FILES_SOURCE_DIR"


def main():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
    load_dotenv()

    source_dir = os.getenv(RENAME_FILES_SOURCE_DIR_ENV)
    if not source_dir:
        raise ValueError(f"source dir not defined: set env {RENAME_FILES_SOURCE_DIR_ENV}")
    logging.info(f"source dir is {source_dir}")

    with open("rename_files.yml", encoding='utf8') as file:
        rules_list = yaml.load(file, Loader=yaml.FullLoader)
        logging.debug(f"rules loaded: {rules_list}")

    date_ts = date.today().strftime("%Y%m%d")
    date_ts_detail = date.today().strftime("%B%Y")

    files = glob.glob(f"{source_dir}/*.pdf")
    logging.info(f"{len(files)} file(s) to handle")
    for f in files:
        logging.info(f"handling file {os.path.basename(f)}")
        match = True
        matched_rule = None
        with fitz.open(f) as pdf_reader:
            for page in pdf_reader:
                text = page.getText("text")
                for r in rules_list:
                    to_match = r.get("MatchAll", [])
                    for m in to_match:
                        match = m in text
                        if not match:
                            break
                        matched_rule = r
                    logging.info(f"file matches rule {r.get('Description')}: {match}")
                if matched_rule:
                    break
        if matched_rule:
            rename_file(f, matched_rule)


def rename_file(f, matched_rule):
    date_ts = date.today().strftime("%Y%m%d")
    date_ts_detail = date.today().strftime("%B%Y")
    suffix = matched_rule.get("FinalNameSuffix", "")
    new_name = f"{date_ts}_{suffix}_{date_ts_detail}.pdf"
    if new_name not in f:
        logging.info(f"renaming file to {new_name}")
        os.rename(f, os.path.dirname(f) + "/" + new_name)
    else:
        logging.info("file already with the final name")


if __name__ == "__main__":
    main()
