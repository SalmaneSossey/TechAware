"""
Summarization service using HuggingFace transformers
"""
from typing import List, Dict
import os

class Summarizer:
    def __init__(self, model_name: str = "facebook/bart-large-cnn"):
        """
        Initialize the summarizer with a HuggingFace model
        
        Args:
            model_name: HuggingFace model identifier
        """
        self.model_name = model_name
        # Lazy loading - only load model when needed
        self._model = None
        self._tokenizer = None
    
    def _load_model(self):
        """Lazy load the model and tokenizer"""
        if self._model is None:
            from transformers import pipeline
            self._model = pipeline("summarization", model=self.model_name)
    
    def summarize(
        self,
        text: str,
        max_length: int = 220,
        min_length: int = 50
    ) -> str:
        """
        Generate a short summary of the input text
        
        Args:
            text: Input text to summarize
            max_length: Maximum length of summary
            min_length: Minimum length of summary
            
        Returns:
            Summary string
        """
        self._load_model()
        
        # Truncate input if too long
        max_input_length = 1024
        if len(text) > max_input_length:
            text = text[:max_input_length]
        
        result = self._model(
            text,
            max_length=max_length,
            min_length=min_length,
            do_sample=False
        )
        
        return result[0]['summary_text']
    
    def generate_impact_suggestions(
        self,
        title: str,
        abstract: str,
        category: str
    ) -> List[str]:
        """
        Generate impact suggestions based on paper content
        
        This is a placeholder implementation. In production, this could use:
        - A fine-tuned model for impact analysis
        - Rule-based heuristics
        - LLM-based generation
        
        Args:
            title: Paper title
            abstract: Paper abstract
            category: Paper category
            
        Returns:
            List of impact suggestion strings
        """
        # Placeholder implementation with rule-based suggestions
        suggestions = []
        
        # Category-based suggestions
        category_impacts = {
            "Machine Learning": [
                "MLOps: Improved model training and deployment workflows",
                "Research: New benchmarks for model performance"
            ],
            "Computer Vision": [
                "Robotics: Enhanced visual perception systems",
                "Healthcare: Improved medical image analysis"
            ],
            "Natural Language Processing": [
                "Customer Service: Better chatbot interactions",
                "Content Creation: Enhanced text generation tools"
            ],
            "Privacy & Security": [
                "Enterprise: Stronger data protection measures",
                "Compliance: Meeting regulatory requirements"
            ]
        }
        
        suggestions = category_impacts.get(category, [
            "Industry: Practical applications in production systems",
            "Research: Foundation for future investigations"
        ])
        
        return suggestions[:2]  # Return max 2 suggestions
