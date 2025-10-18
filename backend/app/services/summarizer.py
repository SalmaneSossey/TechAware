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
    
    async def summarize(
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
    
    async def suggest_impact(self, title: str, abstract: str) -> List[str]:
        """
        Generate impact suggestions based on paper content (async version)
        
        Args:
            title: Paper title
            abstract: Paper abstract
            
        Returns:
            List of impact suggestion strings
        """
        # Extract keywords to determine category
        text_lower = (title + " " + abstract).lower()
        
        # Determine category based on keywords
        if any(kw in text_lower for kw in ["privacy", "security", "federated", "differential privacy"]):
            category = "Privacy & Security"
        elif any(kw in text_lower for kw in ["vision", "image", "video", "detection", "segmentation"]):
            category = "Computer Vision"
        elif any(kw in text_lower for kw in ["nlp", "language", "text", "translation", "chatbot"]):
            category = "Natural Language Processing"
        elif any(kw in text_lower for kw in ["robot", "autonomous", "navigation"]):
            category = "Robotics"
        else:
            category = "Machine Learning"
        
        return self.generate_impact_suggestions(title, abstract, category)
    
    async def extract_tags(self, title: str, abstract: str) -> List[str]:
        """
        Extract relevant tags from paper title and abstract
        
        Args:
            title: Paper title
            abstract: Paper abstract
            
        Returns:
            List of tag strings
        """
        text_lower = (title + " " + abstract).lower()
        tags = []
        
        # Common ML/AI tags
        tag_keywords = {
            "LLM": ["large language model", "llm", "gpt", "bert", "transformer language"],
            "Computer Vision": ["computer vision", "image", "video", "visual", "detection", "segmentation"],
            "NLP": ["natural language", "nlp", "text processing", "language model"],
            "Deep Learning": ["deep learning", "neural network", "deep neural"],
            "Reinforcement Learning": ["reinforcement learning", "rl", "policy gradient", "q-learning"],
            "Federated Learning": ["federated learning", "federated"],
            "Privacy": ["privacy", "differential privacy", "secure"],
            "Security": ["security", "adversarial", "attack"],
            "Attention": ["attention mechanism", "self-attention", "attention"],
            "Transformer": ["transformer", "bert", "gpt"],
            "Efficiency": ["efficient", "optimization", "faster", "speedup"],
            "Edge Computing": ["edge", "mobile", "embedded"],
            "Real-Time": ["real-time", "realtime", "latency"],
            "Generative AI": ["generative", "generation", "gan", "diffusion"],
            "Robotics": ["robot", "autonomous", "navigation"],
            "Healthcare": ["medical", "healthcare", "diagnosis", "clinical"],
            "Multimodal": ["multimodal", "multi-modal", "vision-language"]
        }
        
        for tag, keywords in tag_keywords.items():
            if any(kw in text_lower for kw in keywords):
                tags.append(tag)
        
        # Limit to 5 most relevant tags
        return tags[:5] if tags else ["Machine Learning"]
