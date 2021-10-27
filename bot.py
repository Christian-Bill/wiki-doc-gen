import os
import shutil
import requests
import platform
import wikipediaapi
from time import sleep
from Scripts.pdf import CreatePDF
from Scripts.wiki import Open_File
from Scripts.wiki import WikiFetch
from Scripts.methods import Methods

# Create folders
if not os.path.exists('body'):
    os.mkdir('body')
else:
    shutil.rmtree('body')
    os.mkdir('body')

if not os.path.exists('generated'):
    os.mkdir('generated')

# GNU/Linux or Mac OS
unix = platform.system() == 'Linux' or platform.system() == 'Darwin'

# Init methods
mets = Methods()

# Welcome Page
print('''
********** Random PDF Generator from Wikipedia ************
**********           Version: 1.2              ************

Source Code: https://github.com/Christian-Bill/wiki-doc-gen
''')

# Enter your topic of choice
keyword = input('Enter Topic: ')
print('How many files?')

while True:
    try:
        query_count = int(input('Enter here: '))
        print('')
        break
    except ValueError:
        print('ValueError: Type a number not a letter')     

try:
    # Wikipedia Object
    crawler = WikiFetch(keyword, query_count)
    # Getting all the titles from the topic
    page_titles = crawler.getTitles()
    # Generating all the contents each title
    page_content = crawler.getContent()
    # Summary iteration
    count_titles = len(page_content)
    mets.loadbar(0, count_titles, prefix=f'Generating {query_count} files:', suffix='Complete', length=count_titles)
    for i in page_content:
        
        wiki_wiki = wikipediaapi.Wikipedia('en')
        page_py = wiki_wiki.page(i)
        sample_body_name = page_content.index(i)

        try:
            if unix:
                with Open_File(f'body/sample_{sample_body_name}.txt', 'w') as f:
                    f.write(page_py.summary)
            else:
                with Open_File(f'./body/sample_{sample_body_name}.txt', 'w') as f:
                    f.write(page_py.summary)

        except requests.exceptions.ConnectionError:
            mets.error_message('Something else went wrong', "Press Enter to Exit")
        
        except UnicodeEncodeError:
            mets.error_message('Something else went wrong', 'Press Enter to Refresh')
        
        sleep(0.1)
        mets.loadbar(page_content.index(i) + 1, count_titles, prefix=f'Generating {query_count} files:', suffix='Complete', length=count_titles)

    # Pdf Generation
    for i in page_titles:
        # Creating createpdf object
        locals()[i] = CreatePDF()
        # Add page before writing
        locals()[i].add_page()
        # Printing the titles
        locals()[i].chapter_title(i)

        txt_filename = page_titles.index(i)
        pdf_filename = i
        
        if unix:
            # Printing the body
            locals()[i].print_chapter(f'body/sample_{txt_filename}.txt')
            # Generate PDF file
            locals()[i].output(f'generated/Eng-Essay_{pdf_filename}.pdf')
            
        else:
            # Printing the body
            locals()[i].print_chapter(f'./body/sample_{txt_filename}.txt')
            # Generate PDF file
            locals()[i].output(f'./generated/Eng-Essay_{pdf_filename}.pdf')

    # Delete body files
    shutil.rmtree('body')

    # Closing Message
    current_dir = os.getcwd()
    if unix:
        print(f'Generated PDF files : {current_dir}/generated')
        mets.close()
    else:
        print(f'Generated PDF files : {current_dir}\generated')
        mets.close()  

except requests.exceptions.ConnectionError:
    mets.error_message('ConnectionError: Please check your network connection', 'Press Enter to exit')





    



