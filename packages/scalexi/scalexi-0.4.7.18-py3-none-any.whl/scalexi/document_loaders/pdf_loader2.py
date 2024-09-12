import os
import json
import pkgutil
from langchain_community.document_loaders import PyPDFLoader
#from scalexi.llm.openai_gpt import GPT
from scalexi.llm.google_gemini import Gemini
from scalexi.openai.pricing import OpenAIPricing
#from scalexi_api.prompt_builder.prompts_loader import PromptsLoader
from scalexi.utilities.text_processing import classify_text_binary, remove_code_blocks, remove_code_block_markers, get_text_statistics
from scalexi.generators.generator import Generator
from scalexi.utilities.data_formatter import DataFormatter
import re
from scalexi.utilities.logger import Logger
import PyPDF2
import pdfplumber
from scalexi.openai.pricing import OpenAIPricing
from scalexi.utilities.logger import Logger
import re
from collections import Counter
import pkgutil
from scalexi.openai.utilities import estimate_inference_cost


# Create a logger file
logger = Logger().get_logger()

data = pkgutil.get_data('scalexi', 'data/openai_pricing.json')
pricing_info = json.loads(data)
#print(dfm.json_to_yaml(pricing_info))
pricing = OpenAIPricing(pricing_info)

class PDFLoader:
    """
    A class for loading, splitting, and extracting information from PDF files.
    
    Attributes:
        pdf_path (str): Path to the PDF file.
        model_name (str): Name of the model used for information extraction.
        loader (PyPDFLoader): Instance of PyPDFLoader for loading PDF.
        llm (Generator): Instance of Generator for making LLM requests.
        system_prompt: system prompts.
        logger (Logger): Logger for logging information.
    """

    def __init__(self, pdf_path, model_name="gpt-4o", loader_type = "pdfplumber"):
        """
        Initializes the PDFLoader with a path to the PDF and an optional model name.
        
        Parameters:
            pdf_path (str): Path to the PDF file to be loaded.
            model_name (str): Optional; name of the model for extraction. Default is 'gpt-4o'.
        """
        t0= time.time()
        logger.info('[PDFLoader] Initializing PDFLoader.')
        #EnvironmentConfigLoader().load_environment_config()#must be delcared before logger
        self.logger = Logger().get_logger()
        self.pdf_path = pdf_path
        self.llm = Generator(openai_key=os.getenv("OPENAI_API_KEY"))
        self.model_name = model_name
        #EnvironmentConfigLoader().display_all_env_variables()
        t1= time.time()
        self.loader_type = loader_type
        self.text = self.load_pdf(loader_type=loader_type)
        self.num_tokens = None
        if self.text is not None:
            self.pdf_loding_execution_time = time.time()-t1
            logger.info(f"[PDFLoader] PDF text extracted in {self.pdf_loding_execution_time} seconds")
            #self.logger.info('[PDFLoader] Initialized with model: %s', model_name)
            t1= time.time()
            self.num_tokens = pricing.calculate_token_usage_for_text(self.text, model_name)
            self.calculate_pricing_execution_time = time.time()-t1
            logger.info(f"[PDFLoader] Token usage calculated in {self.calculate_pricing_execution_time} seconds")
            self.total_execution_time = time.time()-t0
            logger.info(f"[PDFLoader] Completed initialization with {model_name} in {self.total_execution_time} seconds")
            #self.stats = self.get_stats(model_name = model_name)
        
        #exit()


    def load_pdf(self, loader_type = "pdfplumber"):
        
        """
        Loads the PDF file and extracts text from it.
        
        Returns:
            str: The extracted text from the PDF.
        """
        self.logger.info('[PDFLoader] Loading PDF.')
        try:
            if loader_type.lower() == "pdfplumber":
                text = self.extract_text_pdfplumber()
            elif loader_type.lower() == "pypdf2":
                text = self.extract_text_with_PyPDFLoader()
            else:
                text = self.extract_text_from_pdf()
            
            if text and len(text) > 50: # Check if there is substantial text
                return text
            else:
                self.logger.error('[PDFLoader-load_pdf] Text is not readable. Returning None')
                return None
        except Exception as e:
            self.logger.error('[PDFLoader-load_pdf] Failed to extract text: %s', str(e))
            return None
            #raise  ValueError("[PDFLoader] Failed to extract text from PDF. Upload a Valid PDF")
            
        
        


    def extract_text_with_PyPDFLoader(self):
        """
        Loads and splits the PDF into pages.
        
        Returns:
            str: The complete text extracted from all pages of the PDF.
        """
        # Check file extension
        if not self.pdf_path.lower().endswith('.pdf'):
            return None
        loader = PyPDFLoader(self.pdf_path)
        pages = loader.load_and_split()
        all_pages_text = [document.page_content for document in pages]
        self.logger.info('[PDFLoader] PDF Loaded and split into pages.')
        return "\n".join(all_pages_text)
    
    def clean_text(self, text):
        """
        Cleans the text by replacing special characters with their correct counterparts.
        
        Parameters:
            text (str): The text to clean.
            
        Returns:
            str: The cleaned text.
        """
        self.logger.debug('[PDFLoader] Cleaning text.')
        replacements = {
            'â€™': "'", 'â€œ': '"', 'â€': '"', 'â€”': '-', 'â€“': '-'
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text
    
    def extract_text_from_pdf_with_PyPDF2(self):
        self.logger.info('[PDFLoader] Extracting text using PyPDF2.')
        all_text = ""
        if not self.pdf_path.lower().endswith('.pdf'):
            return None
        try:
            with open(self.pdf_path , 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    page_text = page.extract_text() or ""  # Handle None
                    all_text += self.clean_text(page_text) + "\n"
        except Exception as e:
            print(f"Failed to read PDF with PyPDF2: {e}")
            all_text = None
        return all_text

    def is_spacing_anomalous(self, text, max_expected_ratio=0.2):
        """
        Check if the spacing in the text is anomalous.
        
        Parameters:
            text (str): The text to check.
            max_expected_ratio (float): Maximum expected ratio of spaces to total characters.
            
        Returns:
            bool: True if the spacing is anomalous, False otherwise.
        """
        self.logger.info('[PDFLoader] Checking spacing in text.')
        if not text:
            return True
        total_chars = len(text)
        space_count = text.count(' ')
        space_ratio = space_count / total_chars
        return space_ratio > max_expected_ratio

    def extract_text_pdfplumber(self):
        """
        Extracts text from the PDF using pdfplumber.
        
        Returns:
            str: The extracted text.
        """
        self.logger.info('[PDFLoader] Extracting text using pdfplumber.')
        text = ''
        if not self.pdf_path.lower().endswith('.pdf'):
            return None
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text() or ""
                    text += self.clean_text(page_text)
        except Exception as e:
            print(f"Failed to read PDF with pdfplumber: {e}")
            text = None
        return text

            
    def extract_text_from_pdf(self):
        """
        Extracts text from the PDF using PyPDF2 and pdfplumber.
        
        Returns:
            str: The extracted text.
        """
        self.logger.info('[PDFLoader] Extracting text from PDF.')
        
        text = self.extract_text_from_pdf_with_PyPDF2()
        if text and len(text) > 50 and not any(ord(char) > 128 for char in text) and not self.is_spacing_anomalous(text):
            return text
        else:
            text = self.extract_text_pdfplumber()
            if text and len(text) >= 50: # Check if there is substantial text
                return text
            else:
                self.logger.error("Text is not readable after trying with pdfplumber. Returning None")
                raise ValueError("Text is not readable after trying with pdfplumber and PyPDF2. Upload a Valid PDF")

    
    def extract_information(self, text:str, request_id, stream=False, max_tokens=4096, system_prompt = None):
        """
        Extracts information from the given text using a specific prompt ID.
        
        Parameters:
            complete_text (str): The text to extract information from.
            request_id (str): The ID of the prompt to use for extraction.
        
        Returns:
            tuple: Extracted information, price, token usage, and execution time.
        
        Raises:
            ValueError: If the prompt ID does not exist in the templates.
            Exception: For other errors that may occur during processing.
        """
        self.logger.info('[extract_information] Extracting information.')
        self.logger.info('[extract_information] Using request_id: %s', request_id)

        if request_id not in self.PROMPT_TEMPLATES:
            self.logger.error('[extract_information] Invalid request_id: %s', request_id)
            #raise ValueError(f"[extract_information] Invalid request_id: {request_id}")
        logger.info(f"request_id: {request_id}")
        
        try:
            logger.debug(f"System Prompt:\n{system_prompt}")
            response, price, token_usage, execution_time = self.llm.ask_llm(
                model_name=self.model_name,
                max_tokens=max_tokens,
                temperature=0.1,
                system_prompt=system_prompt,
                user_prompt=text,
                stream=stream
            )
            clean_response = remove_code_block_markers(response)

            self.logger.debug('[extract_information] Response: %s', clean_response)
            self.logger.debug('[extract_information] Token usage: %s', token_usage)
            
            return clean_response, price, token_usage, execution_time

        except Exception as e:
            self.logger.error('[extract_information] Failed to extract information: %s', str(e))
            #raise e
        
    def get_stats(self, model_name="gpt-4"):
        """
        Provides descriptive statistics about the extracted text from a PDF.

        :param pdf_path: The path to the PDF file to analyze.
        :param model_name: The name of the model to use for token calculation.

        :return: A dictionary containing descriptive statistics about the text.
        """
        # Initialize variables for collecting text and word counts per page
        all_text = ""
        words_per_page = []
        num_pages = 0

        with pdfplumber.open(self.pdf_path) as pdf:
            num_pages = len(pdf.pages)
            for page in pdf.pages:
                page_text = page.extract_text()
                all_text += page_text
                
                # Count words per page
                words = re.findall(r'\w+', page_text)
                words_per_page.append(len(words))

        # Number of characters
        num_chars = len(all_text)
        
        # Number of words
        words = re.findall(r'\w+', all_text)
        num_words = len(words)
        
        # Number of sentences
        sentences = re.split(r'[.!?]+', all_text)
        num_sentences = len(sentences) - 1  # Adjust for possible trailing empty string
        
        # Most common words
        word_freq = Counter(words)
        most_common_words = word_freq.most_common(10)
        print('most_common_words:', most_common_words)
        # Token count
        num_tokens = pricing.calculate_token_usage_for_text(all_text, model_name)
        
        # Get file size in bytes
        try:
            file_size = os.path.getsize(self.pdf_path)
        except Exception as e:
            logger.error(f"An error occurred while getting file size: {e}")
            file_size = None
        
        # Generate statistics dictionary
        stats = {
            "num_chars": num_chars,
            "num_words": num_words,
            "num_sentences": num_sentences,
            "most_common_words": str(most_common_words),
            "num_tokens": num_tokens,
            "num_pages": num_pages,
            "words_per_page": str(words_per_page),
            "file_size": file_size,
            "file_path": self.pdf_path,
            "model_name": model_name
        }   
        
        
        return stats
    
    def get_first_page(self):
        try:
            # Open the PDF file using pdfplumber
            with pdfplumber.open(self.pdf_path) as pdf:
                
                # Check if the PDF has pages
                if len(pdf.pages) < 1:
                    return {"success": False, "message": "The PDF file is empty."}
                
                # Get the first page
                first_page = pdf.pages[0]
                
                # Extract text from the first page
                first_page_text = first_page.extract_text()
                
                # Return the text of the first page
                return {"success": True, "page_text": first_page_text}
        
        except Exception as e:
            logger.error(f"An error occurred while extracting the first page: {e}")
            raise ValueError("Failed to extract the first page. Upload a Valid PDF")
            
    
    def calculate_pricing(self, token_usage):
        """
        Calculates the pricing based on token usage.
        
        Parameters:
            token_usage (dict): A dictionary containing 'prompt_tokens' and 'completion_tokens'.
        
        Returns:
            float: Estimated cost based on token usage.
        """
        self.logger.info('[PDFLoader] calculate_pricing')
        try:
            
            return estimate_inference_cost(
                token_usage,
                self.model_name
            )
        except Exception as e:
            self.logger.error('An error occurred while calculating pricing: %s', str(e))
            raise ValueError("[calculate_pricing] Failed to calculate pricing. Upload a Valid PDF")

    def structure_document(self, request_id=None, stream=False, max_tokens=4096):
        """
        Structures the document based on a given prompt ID. This method
        loads the PDF, extracts information using a specified prompt, calculates
        pricing based on token usage, and logs the entire process.

        Parameters:
            request_id (str): The ID of the prompt to use for structuring.
                            Default is 'simple_prompt'.

        Returns:
            tuple: A tuple containing the structured document response, the price
                for the operation, token usage, and execution time. In case of an
                error, returns None for the response and zeros for all numerical values.
        """
        self.logger.info('[PDFLoader] structure_document')
        try:
            complete_text = self.load_pdf()
            if complete_text is None:
                self.logger.error("[structure_document] Failed to load the PDF. Upload a Valid PDF")
                raise ValueError("[structure_document] Failed to load the PDF. Upload a Valid PDF")
            self.logger.debug('complete_text: %s', complete_text)
            response, price, token_usage, execution_time = self.extract_information(complete_text, request_id, stream=stream, max_tokens=max_tokens)
            #print('response:', response)
            price = self.calculate_pricing(token_usage)
            return response, price, token_usage, execution_time
        except Exception as e:
            self.logger.error('An error occurred while structuring the document: %s', str(e))
            raise ValueError("[structure_document] Failed to structure the document. Upload a Valid PDF")

    def extract_json_from_text(self, text):
        """
        Extracts a JSON object from the given text. This method searches the text
        for a JSON structure, parses it, and returns the JSON object as a string
        with proper formatting. Logs the process and errors if any.

        Parameters:
            text (str): The text from which to extract a JSON object.

        Returns:
            str: A string representation of the JSON object if found, otherwise None.
        """
        self.logger.info('[PDFLoader] extract_json_from_text')
        try:
            start_index = text.index('{')
            end_index = text.rindex('}')
            json_str = text[start_index:end_index + 1]
            json_object = json.loads(json_str)
            json_string = json.dumps(json_object, indent=4)
            self.logger.debug('json_string: %s', json_string)
            return json_string
        except (ValueError, json.JSONDecodeError) as e:
            self.logger.error('An error occurred while extracting JSON from text: %s', str(e))
            raise ValueError("[extract_json_from_text] Failed to extract JSON from text. Upload a Valid PDF")



############################################################################################################
### CV Extractor: Extracts information from CVs using a specific extraction prompt. ########################
############################################################################################################

class CVExtractor(PDFLoader):
    """
    A class derived from PDFLoader to specialize in extracting information
    from CVs. It adds functionality to handle different types of CVs by
    setting a specific extraction prompt based on the CV type.

    Attributes:
        cv_type (str): The type of CV for which the class will extract information.
        extraction_prompt (str): The system prompt used for extraction, derived from the CV type.
    """

    def __init__(self, pdf_path, cv_type: str, model_name="gpt-4-turbo-preview", loader_type = "pdfplumber"):
        """
        Initializes the CVExtractor with a path to the CV, the CV type, and an
        optional model name.

        Parameters:
            pdf_path (str): Path to the PDF file (CV) to be loaded.
            cv_type (str): Type of CV to set the specific extraction prompt.
            model_name (str): Optional; name of the model for extraction. Default is 'gpt-4-turbo-preview'.
        """
        super().__init__(pdf_path, model_name ,loader_type=loader_type)
        self.set_cv_type(cv_type)
        self.request_id = cv_type
        self.logger.debug('TEMPLATES: %s',self.PROMPT_TEMPLATES)
        #self.logger.debug("System Prompt:\n%s", self.PROMPT_TEMPLATES[cv_type])
        self.logger.info('[CVExtractor] Initialized with CV type: %s', cv_type)

    def set_cv_type(self, cv_type):
        """
        Sets the CV type and adjusts the system prompt for extraction based on the CV type.

        Parameters:
            cv_type (str): The type of CV for which information will be extracted.
        
        Raises:
            ValueError: If an invalid CV type is provided.
        """
        self.logger.info('[CVExtractor] set_cv_type to %s', cv_type)
        try:
            self.cv_type = cv_type
            self.extraction_prompt = self.PROMPT_TEMPLATES.get(
                self.cv_type, "GENERAL_CV_DATA_EXTRACTION"
            )
        except Exception as e:
            self.logger.error('An error occurred while setting the CV type: %s', str(e))
            raise ValueError("Failed to set CV type. Upload a Valid PDF")

    def extract_cv_information(self, text=None, request_id=None, stream=False, max_tokens=4096):
        """
        Extracts information from the CV using the specified extraction prompt.

        Returns:
            tuple: A tuple containing the extracted CV information, the price
                   for the operation, token usage, and execution time. In case of an
                   error, returns None for the response and zeros for all numerical values.
        """
        
        self.logger.info('[extract_cv_information] extract_cv_information')
        try:
            
            if request_id is None:
                request_id = self.request_id
            logger.info(f"[extract_cv_information] extract CV information request_id: {request_id}")
            
            if text is None:
                text = self.text
            
            return super().extract_information(text, request_id, max_tokens=max_tokens, stream=stream)

        except Exception as e:
            self.logger.error('[extract_cv_information] An error occurred while extracting CV information: %s', str(e))
            #raise ValueError("[extract_cv_information] Failed to extract CV information. Upload a Valid PDF")



############################################################################################################
### Job Offer Extractor: Extracts information from job offer PDFs using a specific extraction prompt. ######
############################################################################################################


class JobOfferExtractor(PDFLoader):
    def __init__(self, pdf_path, offer_type, model_name="gpt-4-turbo-preview"):
        super().__init__(pdf_path,model_name)
        self.set_offer_type(offer_type)
        self.request_id = offer_type
        #print(self.PROMPT_TEMPLATES[offer_type])
        
        self.system_prompt = self.PROMPT_TEMPLATES.get(self.offer_type, "ELLOUZE_JOB_OFFER_EXTRACTION")
        self.logger.info('[JobOfferExtractor] Initialized with offer type: %s', offer_type)

    def set_offer_type(self, offer_type):
        self.logger.info('[JobOfferExtractor] set_offer_type to %s', offer_type)    
        try:
            #valid_types = ["GENERAL_JOB_OFFER_EXTRACTION", "ELLOUZE_JOB_OFFER_EXTRACTION", "ELLOUZE_JOB_OFFER_EXTRACTION_MIN"]
            #if offer_type not in valid_types:
            #    raise ValueError(f"Invalid job offer type. Must be one of {valid_types}.")
            self.offer_type = offer_type
            self.extraction_prompt = self.PROMPT_TEMPLATES.get(self.offer_type, "ELLOUZE_JOB_OFFER_EXTRACTION")
        except Exception as e:
            self.logger.error('An error occurred while setting the job offer type: %s', str(e))
            

    def extract_job_offer_information(self, text=None, request_id=None, stream=False, max_tokens=4096):
        try:
            self.logger.info('[JobOfferExtractor] extract_job_offer_information')
                        
            if request_id is None:
                request_id = self.request_id
            logger.info(f"[extract_cv_information] extract Job information request_id: {request_id}")
            
            if text is None:
                text = self.text
           
            return super().extract_information(text, request_id, max_tokens=max_tokens, stream=stream)
        
        except Exception as e:
            self.logger.error('An error occurred while extracting job offer information: %s', str(e))
            raise ValueError("Failed to extract job offer information. Upload a Valid PDF")

    def extract_information(self, complete_text, request_id):
        #prompt = json.dumps(self.extraction_prompt)
        print('request_id:',request_id)
        return super().extract_information(complete_text, request_id)
















# Assuming the necessary imports and class definitions are already in place
def test_cv_extraction():
    # Define the path to the CV PDF file
    pdf_path = "cv1.pdf"
    # Initialize the JobOfferExtractor with the specified job offer type
    #model_name="gpt-4-turbo-preview"
    #model_name="gemini-1.0-pro"
    #model_name="command"
    model_name="gpt-3.5-turbo"
    #model_name="gpt-4"
    
    # Initialize the CVExtractor with the specified CV type
    cv_extractor = CVExtractor(pdf_path, "ELLOUZE_CV_EXTRACTION_TYPESCRIPT", model_name=model_name)
    
    # Extract CV information
    try:
        structured_data, price, token_usage, execution_time = cv_extractor.extract_cv_information()
        print("Structured Document:", remove_code_blocks(structured_data))
        print("Cost of Extraction:", price)
        print("Token Usage:", token_usage)
        print("Execution Time:", execution_time)
    except Exception as e:
        print("An error occurred during CV extraction:", str(e))

def test_job_offer_extraction():
    # Define the path to the job offer PDF file
    pdf_path = "job1.pdf"
    
    # Initialize the JobOfferExtractor with the specified job offer type
    #model_name="gpt-4-turbo-preview"
    #model_name="gemini-1.0-pro"
    #model_name="command"
    model_name="gpt-3.5-turbo"
    #model_name="gpt-4"
    job_offer_extractor = JobOfferExtractor(pdf_path, "ELLOUZE_JOB_OFFER_EXTRACTION", model_name=model_name)
    
    # Extract job offer information
    try:
        structured_data, cost = job_offer_extractor.extract_job_offer_information()
        # Assuming remove_code_blocks is a method to clean or process the structured data
        print(remove_code_block_markers(DataFormatter().json_to_yaml(structured_data)))  # Note: .remove_code_blocks() is not defined here
        print("Cost of Extraction:", cost)
    except Exception as e:
        print("An error occurred during job offer extraction:", str(e))
import time
# Call the test functions
if __name__ == "__main__":
    #t0 = time.time()  # Capture the start time
    test_cv_extraction()
    #test_job_offer_extraction()  # Call the function you want to time
    #t1 = time.time()  # Capture the end time after the function execution
    #execution_time = t1 - t0  # Calculate the difference in time
    #print('Execution time:', execution_time, 'seconds')  # Print the execution time


   



