"""This script is used to scrape the Warhammer 40k fandom wiki. It is based on the ScrapeFandom script by @mattiasostmar."""
import scrapefandom
import toml

config = toml.load('config.toml')

WIKI_LIST = config['scrape']["source_wikis"]
OUTPUT_DIR = config['scrape']["output_dir"]

def scrapefandoms_and_save(source_wikis, output_dir):
    """Scrapes the fandoms and saves the output"""
    for wiki in source_wikis:
        try:
            scrapefandom.scrape(wiki, output_dir=output_dir)
        except Exception as error:
            print(error)


if __name__ == '__main__':
    if config['scrape']["run_scraper"]:
        scrapefandoms_and_save(WIKI_LIST, OUTPUT_DIR)