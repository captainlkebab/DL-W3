import streamlit as st
from learning_types import LearningProfile
from crews.TheoryExpertCrew.TheoryExpertCrew import TheoryExpertCrew
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="Music Theory Learning Assistant",
    page_icon="🎵",
    layout="wide"
)

# Helper function for crew execution
def run_crew(user_profile):
    crew = TheoryExpertCrew(learning_profile=user_profile)
    return crew.crew().kickoff()  # Removed async/await

# Title and introduction
st.title("🎵 Music Theory Learning Assistant")
st.write("Create your personalized learning profile and get a customized learning plan.")

# Sidebar for user inputs
with st.sidebar:
    st.header("Your Learning Profile")
    
    # Skill level
    skill_level = st.selectbox(
        "What's your current skill level in music theory?",
        options=["beginner", "intermediate", "advanced"],
        key="skill_level"
    )
    
    # Learning style
    learning_style = st.selectbox(
        "What's your preferred learning style?",
        options=["visual", "auditory", "practical", "reading"],
        key="learning_style"
    )
    
    # Goals
    st.subheader("Learning Goals")
    goals = []
    for i in range(3):  # Allow up to 3 goals
        goal = st.text_input(f"Goal {i+1}", key=f"goal_{i}")
        if goal:
            goals.append(goal)
    
    # Previous knowledge
    st.subheader("Previous Knowledge")
    previous_knowledge = {}
    areas = ["Reading music", "Instrument experience", "Music theory", "Other skills"]
    levels = ["none", "basic", "intermediate", "advanced"]
    
    for area in areas:
        level = st.selectbox(
            f"Your level in {area}",
            options=levels,
            key=f"knowledge_{area}"
        )
        previous_knowledge[area] = level
    
    # Learning pace
    preferred_pace = st.selectbox(
        "What's your preferred learning pace?",
        options=["slow", "moderate", "fast"],
        key="preferred_pace"
    )

# Main content area
if st.button("Generate Learning Plan"):
    if not os.getenv("GROQ_API_KEY"):
        st.error("Error: GROQ_API_KEY not found in environment variables")
    elif not goals:
        st.error("Please add at least one learning goal")
    else:
        try:
            user_profile = LearningProfile(
                skill_level=skill_level,
                learning_style=learning_style,
                goals=goals,
                previous_knowledge=previous_knowledge,
                preferred_pace=preferred_pace
            )
            
            with st.spinner("Creating your personalized learning plan..."):
                try:
                    result = run_crew(user_profile)
                    
                    # Display results
                    st.success("Your learning plan has been created!")
                    
                    tab1, tab2, tab3 = st.tabs(["Learning Plan", "Profile Analysis", "Next Steps"])
                    
                    with tab1:
                        st.markdown("### Your Personalized Learning Plan")
                        
                        # Debug-Ausgabe
                        st.write("Debug - Raw Result Type:", type(result))
                        st.write("Debug - Result Structure:", dir(result))
                        
                        if hasattr(result, 'raw'):
                            st.write("Using result.raw:")
                            st.write(result.raw)
                        elif hasattr(result, 'tasks_output'):
                            st.write("Using tasks_output:")
                            for task in result.tasks_output:
                                st.write("Task Output:", task.raw)
                        else:
                            st.write("Direct result:")
                            st.write(result)
                    
                    with tab2:
                        st.markdown("### Profile Analysis")
                        st.write(f"**Skill Level:** {skill_level.capitalize()}")
                        st.write(f"**Learning Style:** {learning_style.capitalize()}")
                        st.write("**Goals:**")
                        for goal in goals:
                            st.write(f"- {goal}")
                        
                        st.write("\n**Previous Knowledge:**")
                        for area, level in previous_knowledge.items():
                            st.write(f"- {area}: {level.capitalize()}")
                    
                    with tab3:
                        st.markdown("### Next Steps")
                        st.write("1. Review your personalized learning plan")
                        st.write("2. Start with the first module in your timeline")
                        st.write("3. Complete the interactive exercises")
                        st.write("4. Track your progress with each milestone")
                        st.write("5. Return for plan adjustments as needed")
                        
                        # Add a progress tracking section
                        st.subheader("Progress Tracking")
                        st.write("Use this section to track your progress through the learning plan:")
                        for i, goal in enumerate(goals, 1):
                            st.checkbox(f"Goal {i}: {goal}", key=f"progress_goal_{i}")
                
                except Exception as api_error:
                    st.error(f"API Error: {str(api_error)}")
                    st.info("Try again with a different model or wait a few minutes before retrying.")
                
        except Exception as e:
            st.error(f"Application Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("*Powered by AI - Helping you master music theory*") 