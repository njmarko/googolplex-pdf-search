"""
Author: Marko Njegomir sw-38-2018
"""


# import pdftotext
import fitz


# def get_pdf_content(file_path):
#     with open(file_path, "rb") as f:
#         pdf = pdftotext.PDF(f)
#
#         result = {'pages':[]}
#
#         # Iterate over all the pages
#         for i, content in enumerate(pdf):
#             try:
#                 page_number = int(content[:content.index('\n')].split()[-1])
#             except:
#                 page_number = None
#
#             result['pages'].append({'index': i, 'page_number': page_number, 'content': content})
#
#     return result

def get_pdf_content(file_path):
    doc = fitz.open(file_path)

    result = {}

    index = 0
    previous_page_num = None
    for page in doc:
        text = page.getText()
        try:
            line = text.split("\n")[0]
            page_number = int(line.split()[-1].strip())
            previous_page_num = page_number
        except:
            try:
                page_number = previous_page_num + 1
            except:
                page_number = None
        result[index] = {'index': index,
                         'page_number': page_number,
                         'content': text}
        # result[index].append({'index': index, 'page_number': page_number, 'content': text})
        index += 1
    return result

if __name__ == '__main__':
    path = 'Data Structures and Algorithms in Python.pdf'
    content = get_pdf_content(path)
    i = 51
    print("Page index: %d\nPage number: %s\nPage content: \n\n%s" \
          % (content['pages'][i]["index"], content['pages'][i]["page_number"], content['pages'][i]["content"]))
