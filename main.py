#!/usr/bin/env python
import asyncio
import os
from dotenv import load_dotenv
from learning_types import LearningProfile
from crews.TheoryExpertCrew.TheoryExpertCrew import TheoryExpertCrew

def get_user_input() -> LearningProfile:
    print("\n=== Create Your Learning Profile ===\n")
    
    # Skill level input
    print("What's your current skill level in music theory?")
    print("Options: beginner, intermediate, advanced")
    skill_level = input("Your skill level: ").lower()
    
    # Learning style input
    print("\nWhat's your preferred learning style?")
    print("Options: visual, auditory, practical, reading")
    learning_style = input("Your learning style: ").lower()
    
    # Goals input
    print("\nWhat are your learning goals? (Enter empty line to finish)")
    goals = []
    while True:
        goal = input("Goal (or press Enter to finish): ")
        if not goal:
            break
        goals.append(goal)
    
    # Previous knowledge input
    print("\nLet's assess your previous knowledge")
    previous_knowledge = {}
    areas = ["Reading music", "Instrument experience", "Music theory", "Other skills"]
    for area in areas:
        knowledge = input(f"Your level in {area} (none/basic/intermediate/advanced): ")
        previous_knowledge[area] = knowledge
    
    # Learning pace
    print("\nWhat's your preferred learning pace?")
    print("Options: slow, moderate, fast")
    preferred_pace = input("Your preferred pace: ").lower()
    
    return LearningProfile(
        skill_level=skill_level,
        learning_style=learning_style,
        goals=goals,
        previous_knowledge=previous_knowledge,
        preferred_pace=preferred_pace
    )

async def main():
    try:
        # Get user input
        user_profile = get_user_input()
        
        print("\nInitializing Theory Expert Crew...")
        crew = TheoryExpertCrew(learning_profile=user_profile)
        
        print("Starting analysis and plan creation...")
        result = await crew.crew().kickoff()
        print("\n=== Results ===")
        print(result)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    load_dotenv()
    if not os.getenv("GROQ_API_KEY"):
        print("Error: GROQ_API_KEY not found in .env file")
    else:
        asyncio.run(main())
