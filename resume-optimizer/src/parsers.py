from typing import List
from pydantic import BaseModel, Field


class JobDescriptionKeywords(BaseModel):
    """
    Pydantic model representing the key skills and requirements extracted from a job description.
    """
    technical_skills: List[str]
    technologies_and_tools: List[str]
    soft_skills: List[str]
    certifications: List[str]
    other_requirements: List[str]


class OptimizedResumeContent(BaseModel):
    """
    Pydantic model representing the optimized resume content with specific sections.
    This model is designed to be used with LangChain's JsonOutputParser.
    """
    updated_summary: str = Field(
        description="A rewritten professional summary optimized for keywords, maximum 450 characters."
    )

    liberty_mutual_group: List[str] = Field(
        default_factory=list,
        description="Exactly 3 rewritten bullet points for Liberty Mutual Group experience, each maximum 140 characters."
    )

    inovace_technologies: List[str] = Field(
        default_factory=list,
        description="Exactly 3 rewritten bullet points for Inovace Technologies experience, each maximum 140 characters."
    )

    spider_digital_commerce: List[str] = Field(
        default_factory=list,
        description="1-2 rewritten bullet points for Spider Digital Commerce internship."
    )

    echo_project: List[str] = Field(
        default_factory=list,
        description="Exactly 2 rewritten bullet points for the Echo project."
    )

    class Config:
        json_schema_extra = {
            "example": {
                "updated_summary": "Experienced Software Engineer with expertise in...",
                "liberty_mutual_group": [
                    "Led development of cloud-native applications using Python and AWS...",
                    "Implemented CI/CD pipelines reducing deployment time by 40%...",
                    "Optimized database queries resulting in 30% improved application performance..."
                ],
                "inovace_technologies": [
                    "Developed RESTful APIs using Flask and SQLAlchemy serving 10K+ daily users...",
                    "Architected microservices infrastructure with Docker and Kubernetes...",
                    "Implemented OAuth 2.0 and JWT authentication enhancing system security..."
                ],
                "spider_digital_commerce": [
                    "Designed responsive web interfaces using React.js and Material UI..."
                ],
                "echo_project": [
                    "Built voice-enabled assistant with NLP capabilities using Python and TensorFlow...",
                    "Implemented WebSocket for real-time communication between client and server..."
                ]
            }
        }
