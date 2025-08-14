import json
import os
import uuid
from datetime import datetime
from typing import Dict, Any, List


def save_job_analysis_result(job_description: str, analysis_result: Dict[str, Any]) -> str:
    """
    Save job analysis result to a JSON file with metadata.

    Args:
        job_description: The original job description text
        analysis_result: The analysis result from the analyzer chain

    Returns:
        str: The file path where the result was saved
    """
    # Generate unique identifier
    unique_id = str(uuid.uuid4())[:8]
    timestamp = datetime.now()

    # Create filename with timestamp and unique ID
    filename = f"job_analysis_{timestamp.strftime('%Y%m%d_%H%M%S')}_{unique_id}.json"
    file_path = f"resume-optimizer/outputs/job_analysis/{filename}"

    # Prepare data to save
    data_to_save = {
        "metadata": {
            "type": "job_analysis",
            "unique_id": unique_id,
            "timestamp": timestamp.isoformat(),
            "generated_at": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "filename": filename
        },
        "input": {
            "job_description": job_description,
            "job_description_preview": job_description[:200] + "..." if len(job_description) > 200 else job_description
        },
        "output": {
            "analysis_result": analysis_result,
            "total_keywords_extracted": sum(len(keywords) for keywords in analysis_result.values() if isinstance(keywords, list))
        }
    }

    # Save to file
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data_to_save, f, indent=2, ensure_ascii=False)

    return file_path


def save_resume_optimization_result(keywords: List[str], original_resume: str, optimization_result: Dict[str, Any], source_type: str = "job_analysis") -> str:
    """
    Save resume optimization result to a JSON file with metadata.

    Args:
        keywords: List of keywords used for optimization
        original_resume: The original resume text
        optimization_result: The optimization result from the rewriter chain
        source_type: Type of keywords source ("job_analysis", "example")

    Returns:
        str: The file path where the result was saved
    """
    # Generate unique identifier
    unique_id = str(uuid.uuid4())[:8]
    timestamp = datetime.now()

    # Create filename with timestamp and unique ID
    filename = f"resume_optimization_{timestamp.strftime('%Y%m%d_%H%M%S')}_{unique_id}.json"
    file_path = f"resume-optimizer/outputs/resume_optimization/{filename}"

    # Prepare data to save
    data_to_save = {
        "metadata": {
            "type": "resume_optimization",
            "unique_id": unique_id,
            "timestamp": timestamp.isoformat(),
            "generated_at": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "filename": filename,
            "keywords_source": source_type
        },
        "input": {
            "keywords_used": keywords,
            "keywords_count": len(keywords),
            "original_resume_preview": original_resume[:300] + "..." if len(original_resume) > 300 else original_resume
        },
        "output": {
            "optimization_result": optimization_result,
            "sections_optimized": list(optimization_result.keys()) if isinstance(optimization_result, dict) else []
        }
    }

    # Save to file
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data_to_save, f, indent=2, ensure_ascii=False)

    return file_path


def list_saved_files(output_type: str = "all") -> Dict[str, List[str]]:
    """
    List all saved files in the outputs directory.

    Args:
        output_type: "all", "job_analysis", or "resume_optimization"

    Returns:
        Dict with file lists for each type
    """
    base_path = "resume-optimizer/outputs"

    result = {}

    if output_type in ["all", "job_analysis"]:
        job_analysis_path = f"{base_path}/job_analysis"
        if os.path.exists(job_analysis_path):
            result["job_analysis"] = [f for f in os.listdir(
                job_analysis_path) if f.endswith('.json')]
        else:
            result["job_analysis"] = []

    if output_type in ["all", "resume_optimization"]:
        resume_opt_path = f"{base_path}/resume_optimization"
        if os.path.exists(resume_opt_path):
            result["resume_optimization"] = [f for f in os.listdir(
                resume_opt_path) if f.endswith('.json')]
        else:
            result["resume_optimization"] = []

    return result


def load_saved_file(file_type: str, filename: str) -> Dict[str, Any]:
    """
    Load a saved JSON file.

    Args:
        file_type: "job_analysis" or "resume_optimization"
        filename: The filename to load

    Returns:
        Dict containing the saved data
    """
    base_path = "resume-optimizer/outputs"
    file_path = f"{base_path}/{file_type}/{filename}"

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)
