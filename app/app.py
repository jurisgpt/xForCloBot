import streamlit as st
import pandas as pd
import numpy as np
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
from pathlib import Path
import os
from dotenv import load_dotenv
import openai
import json

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(
    page_title="Legal Document Analyzer",
    page_icon="⚖️",
    layout="wide"
)

# Initialize session state
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []

class LegalAnalyzer:
    def __init__(self):
        self.risk_categories = {
            'notice_requirements': {
                'high_risk': [
                    'Multiple authority changes',
                    'Complex modification history',
                    'Servicer transitions',
                    'Incomplete contact information'
                ],
                'medium_risk': [
                    'Timing close to requirements',
                    'Minor information discrepancies',
                    'Supplemental verbal communications',
                    'Authority delegation'
                ],
                'low_risk': [
                    'Clear single authority',
                    'Complete documentation',
                    'Consistent communication',
                    'Proper delegation paper trail'
                ]
            }
        }
        
    def analyze_text(self, text):
        # Placeholder for actual analysis
        # This would be replaced with real model inference
        analysis = {
            'risk_level': 'medium',
            'key_issues': [
                'Notice requirements compliance',
                'Authority documentation',
                'Communication records'
            ],
            'recommendations': [
                'Verify authority documentation',
                'Ensure proper notice delivery',
                'Maintain communication records'
            ]
        }
        return analysis

def main():
    st.title("⚖️ Legal Document Analysis System")
    st.subheader("Foreclosure Document Risk Assessment")
    
    # Sidebar
    with st.sidebar:
        st.header("Settings")
        analysis_type = st.selectbox(
            "Analysis Type",
            ["Notice Requirements", "Authority Verification", "Document Compliance"]
        )
        
        st.header("Analysis History")
        for idx, analysis in enumerate(st.session_state.analysis_history[-5:]):
            with st.expander(f"Analysis {len(st.session_state.analysis_history) - idx}"):
                st.write(analysis)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Document Input")
        doc_text = st.text_area(
            "Enter legal document text here:",
            height=300
        )
        
        if st.button("Analyze Document"):
            if doc_text:
                analyzer = LegalAnalyzer()
                analysis = analyzer.analyze_text(doc_text)
                
                # Store in history
                st.session_state.analysis_history.append({
                    'text': doc_text[:100] + "...",
                    'analysis': analysis
                })
                
                # Display results
                with col2:
                    st.subheader("Analysis Results")
                    
                    # Risk Level
                    risk_color = {
                        'high': 'red',
                        'medium': 'yellow',
                        'low': 'green'
                    }
                    st.markdown(f"**Risk Level:** :{risk_color[analysis['risk_level']}[{analysis['risk_level'].upper()}]")
                    
                    # Key Issues
                    st.subheader("Key Issues")
                    for issue in analysis['key_issues']:
                        st.markdown(f"- {issue}")
                    
                    # Recommendations
                    st.subheader("Recommendations")
                    for rec in analysis['recommendations']:
                        st.markdown(f"- {rec}")
            else:
                st.error("Please enter document text for analysis")

if __name__ == "__main__":
    main()
