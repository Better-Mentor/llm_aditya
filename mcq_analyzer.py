from typing import List, Dict, Tuple
import numpy as np
from scipy.spatial.distance import cosine
import torch
from transformers import BertTokenizer, BertModel

class MCQAnalyzer:
    def __init__(self, model_name: str = "bert-base-uncased"):
        """Initialize BERT model and tokenizer"""
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = BertModel.from_pretrained(model_name)
        self.model.eval()
        
    def get_bert_embedding(self, text: str) -> np.ndarray:
        """Get BERT embedding for a piece of text"""
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        with torch.no_grad():
            outputs = self.model(**inputs)
            embeddings = outputs.last_hidden_state[:, 0, :].numpy()
        return embeddings[0]
    
    def get_semantic_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity between two texts"""
        embedding1 = self.get_bert_embedding(text1)
        embedding2 = self.get_bert_embedding(text2)
        return 1 - cosine(embedding1, embedding2)
    
    def analyze_test_performance(self, questions: List[Dict]) -> Dict:
        """Analyze overall test performance"""
        question_metrics = []
        concept_metrics = []
        answer_distribution = []
        
        # Analyze each question
        for i, q in enumerate(questions):
            # Question complexity analysis
            option_similarities = [
                self.get_semantic_similarity(opt1, opt2)
                for i, opt1 in enumerate(q['options'])
                for opt2 in q['options'][i+1:]
            ]
            
            # Calculate metrics for each question
            answer_similarity = self.get_semantic_similarity(
                q['student_answer'], 
                q['correct_answer']
            )
            
            subject_alignment = self.get_semantic_similarity(
                q['question'], 
                q['correct_answer']
            )
            
            question_metrics.append({
                'question_number': i + 1,
                'complexity': np.mean(option_similarities),
                'subject_alignment': subject_alignment,
                'avg_option_similarity': np.mean(option_similarities),
                'answer_similarity': answer_similarity
            })
            
            # Determine answer correctness
            is_correct = q['student_answer'] == q['correct_answer']
            is_partially_correct = answer_similarity > 0.7 if not is_correct else False
            
            answer_distribution.append({
                'question': i + 1,
                'correct': float(is_correct),
                'partially_correct': float(is_partially_correct),
                'incorrect': float(not (is_correct or is_partially_correct))
            })
        
        # Calculate concept metrics (simplified example)
        concept_metrics = [
            {
                'concept': f'Concept {i+1}',
                'mastery': np.mean([m['answer_similarity'] for m in question_metrics]),
                'confidence': 1 - np.std([m['answer_similarity'] for m in question_metrics])
            }
            for i in range(3)  # Assuming 3 concepts for demonstration
        ]
        
        # Calculate overall metrics
        raw_score = np.mean([q['student_answer'] == q['correct_answer'] for q in questions])
        answer_similarities = [m['answer_similarity'] for m in question_metrics]
        
        return {
            'raw_score': raw_score,
            'weighted_score': np.mean(answer_similarities),
            'average_answer_similarity': np.mean(answer_similarities),
            'concept_consistency': np.std(answer_similarities),
            'concept_mastery': self._calculate_mastery_level({
                'weighted_score': np.mean(answer_similarities),
                'average_answer_similarity': np.mean(answer_similarities),
                'concept_consistency': np.std(answer_similarities)
            }),
            'question_metrics': question_metrics,
            'concept_metrics': concept_metrics,
            'answer_distribution': answer_distribution
        }
    
    def _calculate_mastery_level(self, metrics: Dict) -> str:
        """Determine concept mastery level based on metrics"""
        score = (
            metrics['weighted_score'] * 0.4 +
            metrics['average_answer_similarity'] * 0.4 +
            (1 - metrics['concept_consistency']) * 0.2
        )
        
        if score >= 0.9: return "Expert"
        elif score >= 0.8: return "Advanced"
        elif score >= 0.7: return "Proficient"
        elif score >= 0.6: return "Developing"
        else: return "Basic"
