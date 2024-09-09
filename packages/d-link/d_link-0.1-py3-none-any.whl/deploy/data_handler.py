import json
import os

class DataHandler:
    def __init__(self):
        # Load constants or values from a config file, or define them manually here
        self.constants = {
            'name': 'Pg Network',
            'project': 'Data Display on GitHub Pages',
            'version': '1.0',
            'description': 'This project showcases how to display Python data on a static GitHub Pages website.'
        }

    def get_data(self):
        # Returns the constant values or collected data
        return self.constants

    def generate_json(self, filename='data.json'):
        # Convert data to JSON and save it to a file
        data = self.get_data()
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"JSON data written to {filename}")

    def generate_html(self, filename='index.html'):
        # Generate an HTML file that will be served by GitHub Pages
        data = self.get_data()
        html_content = f"""
        <html>
        <head>
            <title>{data['project']}</title>
        </head>
        <body>
            <h1>{data['project']}</h1>
            <p><strong>Author:</strong> {data['name']}</p>
            <p><strong>Version:</strong> {data['version']}</p>
            <p><strong>Description:</strong> {data['description']}</p>
        </body>
        </html>
        """
        with open(filename, 'w') as f:
            f.write(html_content)
        print(f"HTML data written to {filename}")
