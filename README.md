# Project: Progressive Automated Screening System (PASS)

## 1. Problem Statement

Based on the Innomatics Research Labs "Code4Edtech Challenge," the current manual resume evaluation process is slow, inconsistent, and unable to scale for the thousands of applications received weekly. This leads to delays in shortlisting, inconsistent judgments, and a high workload for the placement team. There is a pressing need for an automated, scalable system that can provide fast, high-quality shortlists and give actionable feedback to students.

## 2. Our Solution: The PASS Platform

The Progressive Automated Screening System (PASS) is a comprehensive platform that streamlines the initial stages of technical recruitment. It features two distinct portals for HR and Students and employs a two-stage screening process to not only score candidates but also validate their practical skills.

### Stage 1: Automated Resume & JD Matching
This stage provides an instant, data-driven first pass on every application, fulfilling the core requirements of the hackathon.

### Stage 2: Dynamic Skills-Based Challenge
This stage incorporates our unique, innovative feature. The most promising candidates are automatically sent a personalized technical challenge to validate the skills listed on their resume, providing a much stronger signal to recruiters.

## 3. Key Features

### Student Portal
- **Job Discovery:** View a list of open positions uploaded by the HR team.
- **Instant Feedback Loop:** Upload a CV and instantly see a detailed analysis and relevance score *before* final submission.
- **Automated Technical Assessment:** Top candidates are automatically presented with a short, timed, skills-based challenge (max 3 questions).
- **Personalized Guidance:** Receive AI-generated feedback on how to improve their resume.

### HR Portal
- **Job Management:** Upload and manage job descriptions.
- **Ranked Candidate Dashboard:** View all applicants for a job, ranked by their resume relevance score.
- **In-Depth Profiles:** Click on any candidate to see a detailed report including skill gaps, the AI-generated "fit verdict," and the results of their technical challenge.
- **Proctoring Flags:** The technical assessment results will include "red flags" if the candidate switched tabs or pasted content, giving insight into their behavior.

## 4. User Workflow

1.  **Upload & Preview:** A student uploads their CV for a job. The system analyzes it and shows the score and feedback only to the student.
2.  **Final Submission:** The student reviews their score and clicks "Finalize and Submit Application." Their application now appears on the HR dashboard.
3.  **Challenge Trigger:** If the student's score exceeds a set threshold, the system immediately generates and presents a unique, 3-question technical challenge.
4.  **HR Review:** The HR team reviews the ranked list of candidates, using the resume score and the technical challenge results to create a high-quality shortlist.

## 5. Tech Stack

- **Backend & Database:** Appwrite (replaces FastAPI and PostgreSQL/SQLite for backend services, database, and storage).
- **Frontend:** Python with Streamlit.
- **Core AI Libraries:** Python, LangChain/LangGraph, and a powerful LLM (e.g., Gemini) for analysis and generation.
