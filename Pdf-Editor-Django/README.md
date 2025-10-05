

```markdown
# PDF Editor

A web-based PDF editor built with Django, HTML, CSS, and JavaScript. This project allows users to add text, images, draw, highlight, erase content, zoom in/out, and navigate through pages. Additionally, it supports converting PDF files to Word, Excel, image formats, and compressing files.

## Features

- **Add Text**: Insert customizable text into the PDF.
- **Add Images**: Insert images into the PDF.
- **Draw**: Freehand drawing on the PDF.
- **Highlight**: Highlight text or areas on the PDF.
- **Erase**: Erase content with configurable thickness.
- **Zoom In/Out**: Zoom functionality for better viewing.
- **Undo/Redo**: Undo and redo actions.
- **Save**: Save the edited PDF.
- **Export**: Export the edited PDF.
- **Convert**: Convert PDF to Word, Excel, and image formats.
- **Compress**: Compress images and files.

## Technologies Used

- **Backend**: Django
- **Frontend**: HTML, CSS, JavaScript
- **Libraries**: 
  - [pdf.js](https://mozilla.github.io/pdf.js/)
  - [fabric.js](http://fabricjs.com/)
  - [PDFLib](https://pdf-lib.js.org/)
  - [Compressor.js](https://github.com/fengyuanchen/compressorjs)
  - [docx](https://github.com/dolanmiu/docx)
  - [ExcelJS](https://github.com/exceljs/exceljs)

## Setup and Installation

### Prerequisites

- Python 3.x
- Django 3.x or higher
- Node.js and npm (for frontend dependencies if needed)

### Installation Steps

1. **Clone the Repository**
    ```sh
    git clone https://github.com/your-username/pdf-editor.git
    cd pdf-editor
    ```

2. **Create and Activate Virtual Environment**
    ```sh
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```

3. **Install Python Dependencies**
    ```sh
    pip install -r requirements.txt
    ```

4. **Run Migrations**
    ```sh
    python manage.py migrate
    ```

5. **Start the Development Server**
    ```sh
    python manage.py runserver
    ```

6. **Open the Application**
    Open your web browser and navigate to `http://127.0.0.1:8000`.

### Frontend Dependencies

Ensure that the following CDN links are included in your HTML file for frontend libraries:

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.5.207/pdf.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/fabric.js/4.3.1/fabric.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf-lib/1.17.1/pdf-lib.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/compressorjs@1.0.7/dist/compressor.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/docx/6.0.3/docx.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/exceljs/4.2.1/exceljs.min.js"></script>
```

## Usage

1. **Upload PDF**: Upload a PDF file to start editing.
2. **Edit PDF**: Use the toolbar to add text, images, draw, highlight, and erase content.
3. **Save and Export**: Save your progress or export the edited PDF.
4. **Convert PDF**: Convert the PDF to Word, Excel, or image format.
5. **Compress**: Compress images or PDF files as needed.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/branch-name`).
3. Make your changes and commit (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/branch-name`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [pdf.js](https://mozilla.github.io/pdf.js/)
- [fabric.js](http://fabricjs.com/)
- [PDFLib](https://pdf-lib.js.org/)
- [Compressor.js](https://github.com/fengyuanchen/compressorjs)
- [docx](https://github.com/dolanmiu/docx)
- [ExcelJS](https://github.com/exceljs/exceljs)

```

This `README.md` file provides a clear and comprehensive overview of the project, setup instructions, usage, and other relevant details. Adjust the repository URL, dependencies, and other specifics as needed for your project.
