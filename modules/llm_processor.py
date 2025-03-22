# modules/llm_processor.py
import os
import json
import re
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
from dotenv import load_dotenv

load_dotenv()

class LLMProcessor:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model_name = "llama3-8b-8192"  # You can change to other models
        self.llm = None
        self._initialize_llm()
        
    def _initialize_llm(self):
        """Initialize the Groq LLM"""
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.llm = ChatGroq(
            groq_api_key=self.api_key,
            model_name=self.model_name
        )
    
    def extract_information(self, search_results, extraction_schema):
        """Extract structured information from search results"""
        if not search_results:
            return {}
        
        # Create prompt with search results and extraction schema
        prompt = f"""
        Based on the following search results, extract information according to the schema.
        
        SEARCH RESULTS:
        {self._format_search_results(search_results)}
        
        EXTRACTION SCHEMA:
        {extraction_schema}
        
        Return ONLY a valid JSON object matching the schema. Do not include any explanations or additional text.
        """
        
        try:
            # Process with LLM
            response = self.llm.invoke([HumanMessage(content=prompt)])
            
            # Extract JSON from response
            response_text = response.content
            
            # Extract JSON using regex
            json_str = self._extract_json_from_text(response_text)
            
            if json_str:
                return json.loads(json_str)
            return {}
            
        except Exception as e:
            print(f"Error extracting information: {e}")
            return {}
    
    def _format_search_results(self, results):
        """Format search results for the prompt"""
        formatted = ""
        for i, result in enumerate(results):
            formatted += f"[{i+1}] {result['title']}\n"
            formatted += f"URL: {result['link']}\n"
            formatted += f"Description: {result['snippet']}\n\n"
        return formatted

def _extract_json_from_text(self, text):
    """Extract JSON from text response"""
    import re
    
    # Try to find JSON in code blocks
    code_block_match = re.search(r'``````', text, re.DOTALL)
    if code_block_match:
        return code_block_match.group(1)
    
    # Try to find JSON objects
    json_match = re.search(r'(\{[\s\S]*\})', text)
    if json_match:
        json_str = json_match.group(1)
        # Clean up the JSON string
        json_str = re.sub(r'[\n\r\t]', '', json_str)
        json_str = re.sub(r',\s*}', '}', json_str)  # Remove trailing commas
        return json_str
    
    return None

