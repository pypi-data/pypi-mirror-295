import asyncio
import nbformat
from nbconvert import WebPDFExporter
from nbconvert.preprocessors import TagRemovePreprocessor


def notebook_to_pdf(notebook_path):
    # Set the appropriate event loop policy for Windows
    if asyncio.get_event_loop().is_running():
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # Read the notebook
    with open(notebook_path) as f:
        notebook = nbformat.read(f, as_version=4)

    # Configure the tag removal preprocessor
    tag_remove_preprocessor = TagRemovePreprocessor()
    tag_remove_preprocessor.remove_cell_tags = ("remove_cell",)
    tag_remove_preprocessor.remove_single_output_tags = ("remove_output",)
    tag_remove_preprocessor.remove_input_tags = ("remove_input",)

    # Create the WebPDF exporter and register the preprocessor
    pdf_exporter = WebPDFExporter()
    pdf_exporter.register_preprocessor(tag_remove_preprocessor, enabled=True)

    # Convert the notebook to PDF
    pdf_data, resources = pdf_exporter.from_notebook_node(notebook)

    # Save the PDF to a file
    pdf_filename = notebook_path.replace(".ipynb", ".pdf")
    with open(pdf_filename, "wb") as f:
        f.write(pdf_data)
    print(f"PDF created: {pdf_filename}")
