#!/usr/bin/env python3
"""
CLI tool for managing saved resume optimizer files.
Usage: python file_cli.py [command] [options]
"""

import argparse
import json
import sys
from datetime import datetime
from src.file_manager import list_saved_files, load_saved_file


def list_files(file_type="all"):
    """List all saved files."""
    files = list_saved_files(file_type)

    if file_type == "all":
        print("📁 All Saved Files:")
        print("=" * 50)

        job_files = files.get("job_analysis", [])
        if job_files:
            print(f"\n📊 Job Analysis Files ({len(job_files)}):")
            for f in sorted(job_files, reverse=True):
                print(f"  • {f}")

        resume_files = files.get("resume_optimization", [])
        if resume_files:
            print(f"\n📝 Resume Optimization Files ({len(resume_files)}):")
            for f in sorted(resume_files, reverse=True):
                print(f"  • {f}")

        total = len(job_files) + len(resume_files)
        print(f"\nTotal files: {total}")

    else:
        file_list = files.get(file_type, [])
        print(f"📁 {file_type.replace('_', ' ').title()} Files ({len(file_list)}):")
        print("=" * 50)
        for f in sorted(file_list, reverse=True):
            print(f"  • {f}")


def show_file_details(file_type, filename):
    """Show details of a specific file."""
    try:
        data = load_saved_file(file_type, filename)

        print(f"📄 File Details: {filename}")
        print("=" * 50)

        print("\n🔍 Metadata:")
        metadata = data["metadata"]
        print(f"  Type: {metadata['type']}")
        print(f"  Generated: {metadata['generated_at']}")
        print(f"  Unique ID: {metadata['unique_id']}")

        if file_type == "job_analysis":
            print(f"\n📊 Analysis Summary:")
            print(
                f"  Keywords extracted: {data['output']['total_keywords_extracted']}")
            print(
                f"  Job description preview: {data['input']['job_description_preview']}")

            print(f"\n📋 Extracted Keywords:")
            result = data['output']['analysis_result']
            for category, keywords in result.items():
                if keywords:
                    print(
                        f"  {category.replace('_', ' ').title()}: {', '.join(keywords)}")

        elif file_type == "resume_optimization":
            print(f"\n📝 Optimization Summary:")
            print(f"  Keywords source: {metadata['keywords_source']}")
            print(f"  Keywords count: {data['input']['keywords_count']}")
            print(
                f"  Keywords used: {', '.join(data['input']['keywords_used'][:5])}{'...' if len(data['input']['keywords_used']) > 5 else ''}")

            print(f"\n📋 Sections optimized:")
            for section in data['output']['sections_optimized']:
                print(f"  • {section.replace('_', ' ').title()}")

    except FileNotFoundError:
        print(f"❌ File not found: {filename}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        sys.exit(1)


def show_stats():
    """Show summary statistics."""
    files = list_saved_files("all")
    job_count = len(files.get("job_analysis", []))
    resume_count = len(files.get("resume_optimization", []))
    total = job_count + resume_count

    print("📈 Summary Statistics")
    print("=" * 30)
    print(f"Job Analysis Files: {job_count}")
    print(f"Resume Optimization Files: {resume_count}")
    print(f"Total Files: {total}")

    if total > 0:
        print(f"\nFile Locations:")
        print(f"  Job Analysis: resume-optimizer/outputs/job_analysis/")
        print(f"  Resume Optimization: resume-optimizer/outputs/resume_optimization/")


def main():
    parser = argparse.ArgumentParser(
        description="Manage resume optimizer saved files")
    subparsers = parser.add_subparsers(
        dest="command", help="Available commands")

    # List command
    list_parser = subparsers.add_parser("list", help="List saved files")
    list_parser.add_argument("--type", choices=["all", "job_analysis", "resume_optimization"],
                             default="all", help="Type of files to list")

    # Show command
    show_parser = subparsers.add_parser("show", help="Show file details")
    show_parser.add_argument("type", choices=["job_analysis", "resume_optimization"],
                             help="Type of file")
    show_parser.add_argument("filename", help="Filename to show")

    # Stats command
    subparsers.add_parser("stats", help="Show summary statistics")

    if len(sys.argv) == 1:
        parser.print_help()
        return

    args = parser.parse_args()

    if args.command == "list":
        list_files(args.type)
    elif args.command == "show":
        show_file_details(args.type, args.filename)
    elif args.command == "stats":
        show_stats()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
