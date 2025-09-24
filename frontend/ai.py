import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
import json

load_dotenv()

openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

if not openrouter_api_key:
    raise ValueError("OPENROUTER_API_KEY not found in .env file")

llm = ChatOpenAI(
    model_name="x-ai/grok-4-fast:free",
    openai_api_key=openrouter_api_key,
    openai_api_base="https://openrouter.ai/api/v1",
)

def get_resume_analysis(resume_text: str, job_description_text: str) -> dict:
    """
    Analyzes a resume against a job description and returns a score, a summary, and guidance.
    """
    prompt = f"""
    Analyze the following resume and job description.
    Provide a relevance score from 0 to 100, where 100 is a perfect match.
    Also, provide a brief summary of why the candidate is a good or bad fit.
    Finally, provide personalized guidance on how to improve the resume to better match the job description.

    Resume: {resume_text}

    Job Description: {job_description_text}

    Output the result in a JSON format with three keys: 'score', 'summary', and 'guidance'.
    """

    try:
        response = llm.invoke(prompt).content
    except Exception as e:
        return {"score": 0, "summary": f"Could not get analysis from the model: {e}", "guidance": "Please check the connection to the language model."}

    try:
        if response.startswith("```json"):
            response = response[7:-4]
        result = json.loads(response)
    except json.JSONDecodeError:
        score_line = [line for line in response.split('\n') if '"score"' in line]
        summary_line = [line for line in response.split('\n') if '"summary"' in line]
        guidance_line = [line for line in response.split('\n') if '"guidance"' in line]
        if score_line and summary_line and guidance_line:
            score = int(score_line[0].split(':')[1].replace('",', '').strip())
            summary = summary_line[0].split(':')[1].replace('"', '').strip()
            guidance = guidance_line[0].split(':')[1].replace('"', '').strip()
            result = {"score": score, "summary": summary, "guidance": guidance}
        else:
            result = {"score": 0, "summary": "Could not parse the model's response.", "guidance": "Could not parse the model's response."}
    return result

def generate_challenge(resume_text: str) -> str:
    """
    Generates a short technical challenge with 3 questions based on the skills mentioned in the resume.
    """
    prompt = f"""
    Based on the following resume, generate a short technical challenge with 3 questions.
    The questions should be designed to test the candidate's practical skills.
    The questions should be in a numbered list.

    Resume: {resume_text}
    """

    try:
        response = llm.invoke(prompt).content
    except Exception as e:
        response = f"Could not generate challenge: {e}"
    return response

def score_challenge(questions: str, answers: str) -> int:
    """
    Scores a technical challenge based on the questions and answers.
    Returns a score from 0 to 100.
    """
    prompt = f"""
    The following is a technical challenge and the candidate's answers.
    Please score the challenge from 0 to 100, where 100 is a perfect score.
    Provide only the score as an integer.

    Challenge Questions:
    {questions}

    Candidate's Answers:
    {answers}
    """

    try:
        response = llm.invoke(prompt).content
    except Exception as e:
        print(f"Error scoring challenge: {e}")
        return 0

    try:
        score = int(response)
    except ValueError:
        score = 0
    return score

def get_skill_gaps(resume_text: str, job_description_text: str) -> list[str]:
    """
    Identifies the skill gaps between a resume and a job description.
    Returns a list of skill gaps.
    """
    prompt = f"""
    Identify the skill gaps between the following resume and job description.
    List the skills that are mentioned in the job description but not in the resume.
    Return the result as a JSON list of strings.

    Resume: {resume_text}

    Job Description: {job_description_text}
    """

    try:
        response = llm.invoke(prompt).content
    except Exception as e:
        print(f"Error getting skill gaps: {e}")
        return []

    try:
        if response.startswith("```json"):
            response = response[7:-4]
        result = json.loads(response)
    except json.JSONDecodeError:
        result = []

    return result

def get_challenge_feedback(questions: str, answers: str, score: int) -> str:
    """
    Provides detailed feedback on a technical challenge.
    """
    prompt = f"""
    The following is a technical challenge, the candidate's answers, and the final score.
    Please provide a detailed, question-by-question feedback for the candidate.
    Explain what was right, what was wrong, and how they can improve.

    Challenge Questions:
    {questions}

    Candidate's Answers:
    {answers}

    Final Score: {score}/100

    Provide the feedback in a markdown format.
    """

    try:
        response = llm.invoke(prompt).content
    except Exception as e:
        response = f"Could not generate feedback: {e}"
    return response