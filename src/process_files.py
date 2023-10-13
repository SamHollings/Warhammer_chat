""""tools for processing the xml files into a json format for use in the database"""
import glob
import re
import toml
from langchain.text_splitter import RecursiveCharacterTextSplitter
from bs4 import BeautifulSoup
from langchain.schema.document import Document
from tqdm import tqdm
import vectordb as vectordb


config = toml.load('config.toml')

OUTPUT_DIR = config['scrape']["output_dir"]


def extract_page_elements(page_xml,source):
  title = page_xml.title.text
  content = page_xml.find("text").text
  categories = re.findall("(?<=\\n\[\[Category\:)[A-Za-z\s]+(?=\]\])", content)
  links = list(set(re.findall("(?<=\[\[)[A-Za-z\s]+(?=\]\])", content)))
  page_link = "https://{0}/wiki/{1}".format(source,title.replace(" ","-"))
  #sources = list(set(re.findall("(?<=Sources\=\=\n\*[\s\S]*)(\'\'[A-Za-z\s\:\'\(\)\,0-9\.]+)(?=\n+)", content)))
  return dict(page_content=clean_page_content(content),
              metadata=dict(title=title,
                            categories=categories,links=links,
                            page_link=page_link,
              )
              #sources=sources
              )


def clean_page_content(unclean_content):
  cleaned = re.sub("[(\'\'\')(\[\[\)(\]\])(\=\=)(\{\{)(\}\})]",'', unclean_content)
  cleaned = re.sub("\<[A-Za-z\s\"\=0-9\/]+\>",'', cleaned)
  cleaned = re.sub("\n{3,}",'\n', cleaned)
  cleaned = re.sub(' style\"text\-align\: center\;\"\|','', cleaned)
  cleaned = re.sub("Quote\|",'Quote: ', cleaned)
  cleaned = re.sub("\|",'', cleaned)
  cleaned = re.sub("\:\\n",':', cleaned)
  cleaned = re.sub("\-\\n\!",'-', cleaned)
  cleaned = re.sub("\\n\!",'\n-', cleaned)
  return cleaned


def process_into_database(source, vectorstore=None, output_dir=OUTPUT_DIR):
  raw_40k_fandom_json = glob.glob(f"{output_dir}/{source}_raw/*.xml", recursive=True)

  text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)

  json_collection = []
  # for each xml file

  for json_file in tqdm(raw_40k_fandom_json,desc="Processing Files", position=0):
    # get a list of the pages
    with open(json_file, "r") as xmlfile:
      soup = BeautifulSoup(xmlfile,features="lxml-xml")
      pages = soup.find_all("page")

    # for each page:
    doc_collection = []
    for page in tqdm(pages, desc="Processing pages", position=1, leave=False):
      page_elements = extract_page_elements(page,source)

      page_elements['metadata']['categories'] = str(page_elements['metadata']['categories'])
      page_elements['metadata']['links'] = str(page_elements['metadata']['links'])

      if page_elements['page_content'][0:9] == '#REDIRECT':
        continue # we want to ignore the "redirect" pages as they have no useful content

      json_collection.append(page_elements)
      doc_collection.append(Document(**page_elements))

    # during for each loop, we then batch insert all the pages for that file into the database
    if vectorstore:
      if text_splitter:
        texts = text_splitter.split_documents(doc_collection)
      else:
        texts = doc_collection

      vectorstore.add_documents(documents=texts)

  return json_collection

if __name__=="__main__":
  vectordb = vectordb.create_vectorstore()

  process_into_database("warhammer40k.fandom.com", vectorstore=vectordb)