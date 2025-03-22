# app.py
import os
import json
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import plotly.express as px
import plotly.utils
from modules.data_processor import DataProcessor
from modules.search_engine import SearchEngine
from modules.llm_processor import LLMProcessor

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize components
data_processor = DataProcessor()
search_engine = SearchEngine()
llm_processor = LLMProcessor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])  # Make sure both GET and POST are allowed
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('index'))
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('index'))
        
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Load the CSV file
            if data_processor.load_csv(file_path):
                flash('File uploaded successfully')
                return redirect(url_for('configure_enrichment'))
            else:
                flash('Error loading CSV file')
                return redirect(url_for('index'))
    
    # If it's a GET request, redirect to index
    return redirect(url_for('index'))

@app.route('/configure', methods=['GET'])
def configure_enrichment():
    columns = data_processor.get_query_columns()
    return render_template('configure.html', columns=columns)

@app.route('/process', methods=['POST'])
def process_data():
    column_name = request.form.get('column_name')
    query_template = request.form.get('query_template')
    extraction_schema = request.form.get('extraction_schema')
    
    # Build queries based on selected column and template
    queries = data_processor.build_queries(query_template, column_name)
    
    # Process each query
    enriched_data = []
    for query_item in queries:
        value = query_item['value']
        query = query_item['query']
        
        # Search the web
        search_results = search_engine.search(query)
        
        # Extract information using LLM
        extracted_info = llm_processor.extract_information(search_results, extraction_schema)
        
        # Add to enriched data
        enriched_data.append({
            "original_value": value,
            "enriched_data": extracted_info
        })
    
    # Update the dataframe with enriched data
    data_processor.enrich_data(column_name, enriched_data)
    
    # Export the enriched data
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'enriched_data.csv')
    data_processor.export_csv(output_path)
    
    return redirect(url_for('results'))

@app.route('/results')
def results():
    # Create visualizations
    if data_processor.data is not None:
        # Example visualization - adjust based on your data
        df = data_processor.data
        
        # Create a sample bar chart
        if len(df.columns) > 1:
            fig = px.bar(df, x=df.columns[0], y=df.columns[1], title='Enriched Data Visualization')
            bar_chart = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        else:
            bar_chart = None
        
        return render_template('results.html', 
                              data_preview=df.head(10).to_html(classes='table table-striped'),
                              bar_chart=bar_chart)
    else:
        flash('No data available')
        return redirect(url_for('index'))

# Add a route to download the enriched CSV file
@app.route('/download')
def download():
    return send_from_directory(app.config['UPLOAD_FOLDER'], 'enriched_data.csv', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
