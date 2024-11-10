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



# MCQ Analysis Metrics
### 1. **Complexity**
   - Average semantic similarity between options in a question:
   \[
   \text{Complexity}_i = \frac{1}{\binom{n}{2}} \sum_{j=1}^{n-1} \sum_{k=j+1}^{n} \text{cosine\_similarity}(\text{option}_j, \text{option}_k)
   \]
   where \( n \) is the number of options in question \( i \).

### 2. **Subject Alignment**
   - Similarity between the question text and the correct answer:
   \[
   \text{Subject Alignment}_i = \text{cosine\_similarity}(\text{question}_i, \text{correct\_answer}_i)
   \]

### 3. **Average Option Similarity**
   - Average similarity between all pairs of options in a question:
   \[
   \text{Avg Option Similarity}_i = \text{Complexity}_i
   \]

### 4. **Answer Similarity**
   - Similarity between the student's answer and the correct answer:
   \[
   \text{Answer Similarity}_i = \text{cosine\_similarity}(\text{student\_answer}_i, \text{correct\_answer}_i)
   \]

### 5. **Answer Distribution**
   - Distribution of answers across correct, partially correct, and incorrect:
   \[
   \text{Answer Distribution}_i = 
   \begin{cases} 
      \text{Correct} & \text{if } \text{student\_answer}_i = \text{correct\_answer}_i \\
      \text{Partially Correct} & \text{if } \text{Answer Similarity}_i > 0.7 \text{ and not correct} \\
      \text{Incorrect} & \text{otherwise} 
   \end{cases}
   \]

### 6. **Raw Score**
   - Fraction of correctly answered questions:
   \[
   \text{Raw Score} = \frac{\sum_{i=1}^{N} \text{Correct}_i}{N}
   \]
   where \( N \) is the total number of questions.

### 7. **Weighted Score**
   - Average similarity across all questions:
   \[
   \text{Weighted Score} = \frac{1}{N} \sum_{i=1}^{N} \text{Answer Similarity}_i
   \]

### 8. **Average Answer Similarity**
   - Mean similarity across all questions:
   \[
   \text{Average Answer Similarity} = \text{Weighted Score}
   \]

### 9. **Concept Consistency**
   - Standard deviation of answer similarities across questions:
   \[
   \text{Concept Consistency} = \sqrt{\frac{1}{N} \sum_{i=1}^{N} (\text{Answer Similarity}_i - \text{Weighted Score})^2}
   \]

### 10. **Concept Mastery**
   - Weighted score for mastery level:
   \[
   \text{Concept Mastery Score} = 0.4 \times \text{Weighted Score} + 0.4 \times \text{Average Answer Similarity} + 0.2 \times (1 - \text{Concept Consistency})
   \]
   - Mastery Levels:
   \[
   \text{Concept Mastery} = 
   \begin{cases} 
      \text{Expert} & \text{if } \text{Concept Mastery Score} \geq 0.9 \\
      \text{Advanced} & \text{if } 0.8 \leq \text{Concept Mastery Score} < 0.9 \\
      \text{Proficient} & \text{if } 0.7 \leq \text{Concept Mastery Score} < 0.8 \\
      \text{Developing} & \text{if } 0.6 \leq \text{Concept Mastery Score} < 0.7 \\
      \text{Basic} & \text{if } \text{Concept Mastery Score} < 0.6 \\
   \end{cases}
