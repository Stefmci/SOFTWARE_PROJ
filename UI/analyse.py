import streamlit as st
import classes as cl
import matplotlib.pyplot as plt
import numpy as np
import classes as cl



def analyse():
    st.header("Analyse")
    
    st.divider()
    
    st.metric(label="Test", value="123.45", delta="5.67")