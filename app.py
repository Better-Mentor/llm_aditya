import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from mcq_data import mcq_questions
from mcq_analyzer import MCQAnalyzer  # Your existing analyzer class

def create_radar_chart(metrics):
    """Create radar chart for overall performance"""
    categories = ['Raw Score', 'Weighted Score', 'Answer Similarity', 'Concept Consistency']
    values = [
        metrics['raw_score'],
        metrics['weighted_score'],
        metrics['average_answer_similarity'],
        1 - metrics['concept_consistency']  # Convert std to consistency measure
    ]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Performance Metrics'
    ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=False
    )
    return fig

def create_complexity_chart(question_metrics):
    """Create line chart for question complexity analysis"""
    df = pd.DataFrame(question_metrics)
    fig = px.line(df, x='question_number', y=['complexity', 'subject_alignment', 'avg_option_similarity'],
                  title='Question Complexity Analysis',
                  labels={'value': 'Score', 'question_number': 'Question Number'})
    return fig

def create_concept_mastery_chart(concept_metrics):
    """Create bar chart for concept mastery"""
    df = pd.DataFrame(concept_metrics)
    fig = px.bar(df, x='concept', y=['mastery', 'confidence'],
                 title='Concept Mastery Breakdown',
                 barmode='group')
    return fig

def create_answer_distribution_chart(answer_dist):
    """Create stacked bar chart for answer distribution"""
    df = pd.DataFrame(answer_dist)
    fig = px.bar(df, x='question', y=['correct', 'partially_correct', 'incorrect'],
                 title='Answer Distribution by Question',
                 barmode='stack')
    return fig

def main():
    st.title("MCQ Quiz and Analysis Dashboard")
    
    # Initialize session state
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    if 'quiz_completed' not in st.session_state:
        st.session_state.quiz_completed = False
    
    # Quiz section
    if not st.session_state.quiz_completed:
        questions = mcq_questions['questions']
        current_q = questions[st.session_state.current_question]
        
        # Display progress
        st.progress((st.session_state.current_question + 1) / len(questions))
        st.write(f"Question {st.session_state.current_question + 1} of {len(questions)}")
        
        # Display question
        st.markdown(f"### {current_q['question']}")
        answer = st.radio("Select your answer:", current_q['options'], key=f"q_{current_q['id']}")
        
        # Navigation buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.session_state.current_question > 0:
                if st.button("Previous"):
                    st.session_state.current_question -= 1
                    st.rerun()
        
        with col2:
            if st.session_state.current_question < len(questions) - 1:
                if st.button("Next"):
                    st.session_state.answers[current_q['id']] = answer
                    st.session_state.current_question += 1
                    st.rerun()
            else:
                if st.button("Submit Quiz"):
                    st.session_state.answers[current_q['id']] = answer
                    st.session_state.quiz_completed = True
                    st.rerun()
    
    # Analysis section
    if st.session_state.quiz_completed:
        st.markdown("## Quiz Analysis")
        
        # Initialize analyzer
        analyzer = MCQAnalyzer()
        
        # Prepare data for analysis
        analysis_data = []
        for q in mcq_questions['questions']:
            analysis_data.append({
                'question': q['question'],
                'correct_answer': q['correct_answer'],
                'student_answer': st.session_state.answers[q['id']],
                'options': q['options']
            })
        
        # Get analysis results
        results = analyzer.analyze_test_performance(analysis_data)
        
        # Display metrics and visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Overall Score", f"{results['raw_score']*100:.1f}%")
            st.metric("Concept Mastery Level", results['concept_mastery'])
        
        with col2:
            st.metric("Weighted Score", f"{results['weighted_score']*100:.1f}%")
            st.metric("Concept Consistency", f"{(1-results['concept_consistency'])*100:.1f}%")
        
        # Visualizations
        st.plotly_chart(create_radar_chart(results))
        
        tabs = st.tabs(["Complexity Analysis", "Concept Mastery", "Answer Distribution"])
        
        with tabs[0]:
            st.plotly_chart(create_complexity_chart(results['question_metrics']))
        
        with tabs[1]:
            st.plotly_chart(create_concept_mastery_chart(results['concept_metrics']))
        
        with tabs[2]:
            st.plotly_chart(create_answer_distribution_chart(results['answer_distribution']))
        
        # Detailed feedback
        st.markdown("### Question-wise Feedback")
        for i, q in enumerate(analysis_data):
            with st.expander(f"Question {i+1}"):
                st.write(f"**Question:** {q['question']}")
                st.write(f"**Your Answer:** {q['student_answer']}")
                st.write(f"**Correct Answer:** {q['correct_answer']}")
                st.write(f"**Similarity Score:** {results['question_metrics'][i]['answer_similarity']:.2f}")
                
        # Reset button
        if st.button("Take Quiz Again"):
            st.session_state.current_question = 0
            st.session_state.answers = {}
            st.session_state.quiz_completed = False
            st.rerun()

if __name__ == "__main__":
    main()
