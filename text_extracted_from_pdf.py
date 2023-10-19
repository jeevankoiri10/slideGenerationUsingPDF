import PyPDF2
import spacy

# Function to extract text from a PDF file and convert it to structured Markdown
def extract_text_and_convert_to_markdown(pdf_file_path):
    text = ""
    with open(pdf_file_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        markdown_text = ""  # Initialize Markdown text
        current_heading = None

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()
            if page_text.strip():  # Check if the page has content
                # Detect and mark headings in Markdown format
                if page_text.startswith('#'):
                    if current_heading:
                        markdown_text += f"\n\n{current_heading}\n"  # Add a new line for a new heading
                    current_heading = page_text.strip()
                else:
                    markdown_text += page_text

        # Append the last heading and page content
        if current_heading:
            markdown_text += f"\n\n{current_heading}\n"

    return markdown_text

# Function to perform topic modeling based on headings in Markdown
def perform_topic_modeling(markdown_text):
    # Initialize spaCy NLP model (you may need to download the model first)
    nlp = spacy.load("en_core_web_sm")

    headings = []
    paragraphs = []

    lines = markdown_text.split('\n')
    for line in lines:
        if line.strip():
            if line.startswith('#'):
                headings.append(line.strip('#').strip())
            else:
                paragraphs.append(line)

    return headings, paragraphs

if __name__ == "__main__":
    pdf_file_path = "pdf/pdf2.pdf"
    
    markdown_text = extract_text_and_convert_to_markdown(pdf_file_path)
    print('Extracted text in Markdown format:')
    print(markdown_text)

    if markdown_text:
        headings, paragraphs = perform_topic_modeling(markdown_text)

        # Print the detected headings
        print("Detected Headings:")
        for heading in headings:
            print(heading)

        # Create a mapping between headings and their corresponding paragraphs
        heading_paragraph_mapping = {}
        current_heading = None
        for heading, paragraph in zip(headings, paragraphs):
            if heading not in heading_paragraph_mapping:
                heading_paragraph_mapping[heading] = []
            heading_paragraph_mapping[heading].append(paragraph)

        # Print paragraphs for a specific heading
        target_heading = "Your Target Heading"  # Replace with the desired heading
        if target_heading in heading_paragraph_mapping:
            print(f"Paragraphs under '{target_heading}':")
            for paragraph in heading_paragraph_mapping[target_heading]:
                print(paragraph)
