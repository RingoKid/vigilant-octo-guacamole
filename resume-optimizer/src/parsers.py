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
        description="A rewritten professional summary optimized for keywords, minimum 500 characters, maximum 550 characters."
    )

    liberty_mutual_group: List[str] = Field(
        default_factory=list,
        description="Exactly 3 rewritten bullet points for Liberty Mutual Group experience, each minimum 230 characters, maximum 250 characters."
    )

    inovace_technologies: List[str] = Field(
        default_factory=list,
        description="Exactly 3 rewritten bullet points for Inovace Technologies experience, each minimum 230 characters, maximum 250 characters."
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
                "updated_summary": "Experienced Software Engineer with 5+ years of expertise in full-stack development, cloud architecture, and machine learning. Proven track record of delivering scalable solutions using Python, AWS, React, and modern frameworks. Strong background in API development, microservices, CI/CD pipelines, and data optimization. Skilled in Docker, Kubernetes, PostgreSQL, and agile methodologies with demonstrated ability to improve system performance and reduce operational costs.",
                "liberty_mutual_group": [
                    "Led development of cloud-native applications using Python, AWS Lambda, and DynamoDB, serving 50K+ daily users with 99.9% uptime while implementing comprehensive automated testing and monitoring solutions that reduced incident response time by 60% and improved overall system reliability",
                    "Implemented comprehensive CI/CD pipelines using Jenkins, Docker, and Kubernetes, reducing deployment time by 40% and establishing automated quality gates that decreased production bugs by 35% through rigorous testing protocols and code review processes",
                    "Optimized database queries and implemented advanced caching strategies using Redis and ElasticSearch, resulting in 30% improved application performance and 25% reduction in infrastructure costs while maintaining strict data integrity and compliance standards"
                ],
                "inovace_technologies": [
                    "Developed scalable RESTful APIs using Flask, SQLAlchemy, and PostgreSQL serving 10K+ daily users with sub-200ms response times, implementing comprehensive error handling, logging, and monitoring solutions for production reliability and performance optimization",
                    "Architected microservices infrastructure with Docker and Kubernetes on AWS EKS, enabling horizontal scaling and fault tolerance while reducing system complexity and improving deployment efficiency by 45% across multiple development teams and environments",
                    "Implemented OAuth 2.0 and JWT authentication with role-based access control, enhancing system security and user management capabilities while ensuring GDPR compliance and establishing comprehensive audit trails for security monitoring and compliance reporting"
                ],
                "spider_digital_commerce": [
                    "Designed responsive web interfaces using React.js and Material UI for e-commerce platform, improving user experience and conversion rates by 20% through intuitive design and performance optimization"
                ],
                "echo_project": [
                    "Built voice-enabled assistant with natural language processing capabilities using Python, TensorFlow, and speech recognition APIs, achieving 95% accuracy in voice command interpretation",
                    "Implemented real-time WebSocket communication between client and server components, enabling instant voice feedback and seamless user interactions with sub-100ms latency for enhanced user experience"
                ]
            }
        }
