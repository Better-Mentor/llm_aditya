# Running the necessary functions:
## How to use it:
```python

from mcq_analyzer import MCQAnalyzer  # Your existing analyzer class
# Initialize analyzer
analyzer = MCQAnalyzer()
# Prepare data for analysis
analysis_data = []
for q in mcq_questions['questions']:
    analysis_data.append({
        'question': q['question'],
        'correct_answer': q['correct_answer'],
        'student_answer': q['id'],
        'options': q['options']
    })

# get analysis results
results = analyzer.analyze_test_performance(analysis_data)
```
`Analyze test performance` -
Return values:  
'raw_score' - correct answers  
'weighted_score'  
'average_answer_similarity'  
'concept_consistency'  
'concept_mastery'  
'weighted_score'  
'question_metrics'- Expert OR Advanced OR Proficient OR Developing OR Basic  
'concept_metrics'  
'answer_distribution'  



### MCQ Analyzer Formulas

### Complexity
Average semantic similarity between options in a question:

Complexity_i = (1 / C(n, 2)) * Σ_{j=1}^{n-1} Σ_{k=j+1}^n cosine_similarity(option_j, option_k)


where `n` is the number of options in question `i`, and `C(n, 2)` represents the combination formula for choosing 2 items from `n`.

### Subject Alignment
Similarity between the question text and the correct answer:

Subject_Alignment_i = cosine_similarity(question_i, correct_answer_i)



### Average Option Similarity
Average similarity between all pairs of options in a question:

Avg_Option_Similarity_i = Complexity_i



### Answer Similarity
Similarity between the student's answer and the correct answer:

Answer_Similarity_i = cosine_similarity(student_answer_i, correct_answer_i)



### Answer Distribution
Distribution of answers across correct, partially correct, and incorrect:

Answer_Distribution_i =
Correct if student_answer_i == correct_answer_i
Partially Correct if Answer_Similarity_i > 0.7 and student_answer_i ≠ correct_answer_i
Incorrect otherwise



### Raw Score
Fraction of correctly answered questions:

Raw_Score = (Σ_{i=1}^N Correct_i) / N


where `N` is the total number of questions.

### Weighted Score
Average similarity across all questions:

Weighted_Score = (1 / N) * Σ_{i=1}^N Answer_Similarity_i



### Average Answer Similarity
Mean similarity across all questions:

Average_Answer_Similarity = Weighted_Score



### Concept Consistency
Standard deviation of answer similarities across questions:

Concept_Consistency = sqrt((1 / N) * Σ_{i=1}^N (Answer_Similarity_i - Weighted_Score)^2)



### Concept Mastery
Weighted score for mastery level:

Concept_Mastery_Score = 0.4 * Weighted_Score + 0.4 * Average_Answer_Similarity + 0.2 * (1 - Concept_Consistency)


Mastery Levels:

Concept_Mastery =
Expert if Concept_Mastery_Score >= 0.9
Advanced if 0.8 <= Concept_Mastery_Score < 0.9
Proficient if 0.7 <= Concept_Mastery_Score < 0.8
Developing if 0.6 <= Concept_Mastery_Score < 0.7
Basic if Concept_Mastery_Score < 0.6

