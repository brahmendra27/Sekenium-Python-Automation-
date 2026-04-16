#!/usr/bin/env python3
"""
Script to create a new test automation project from template.

Usage:
    python scripts/create_new_project.py <project_name>

Example:
    python scripts/create_new_project.py my_ecommerce_site
"""

import os
import shutil
import sys
from pathlib import Path


def create_new_project(project_name):
    """
    Create a new project from template.
    
    Args:
        project_name: Name of the new project (kebab-case recommended)
    """
    
    # Validate project name
    if not project_name:
        print("❌ Error: Project name cannot be empty")
        return False
    
    if " " in project_name:
        print("❌ Error: Project name cannot contain spaces. Use kebab-case (e.g., my-project)")
        return False
    
    # Define paths
    template_dir = Path("projects/_template")
    project_dir = Path(f"projects/{project_name}")
    
    # Check if template exists
    if not template_dir.exists():
        print(f"❌ Error: Template directory not found at {template_dir}")
        return False
    
    # Check if project already exists
    if project_dir.exists():
        print(f"❌ Error: Project '{project_name}' already exists at {project_dir}")
        print(f"   Please choose a different name or delete the existing project.")
        return False
    
    print(f"📦 Creating new project: {project_name}")
    print(f"📁 Location: {project_dir}")
    print()
    
    try:
        # Copy template to new project directory
        print("📋 Copying template files...")
        shutil.copytree(template_dir, project_dir)
        
        # Rename template files
        print("✏️  Renaming template files...")
        config_template = project_dir / "config.yaml.template"
        config_file = project_dir / "config.yaml"
        if config_template.exists():
            config_template.rename(config_file)
        
        conftest_template = project_dir / "tests" / "conftest.py.template"
        conftest_file = project_dir / "tests" / "conftest.py"
        if conftest_template.exists():
            conftest_template.rename(conftest_file)
        
        # Update config.yaml with project name
        print("🔧 Updating configuration...")
        if config_file.exists():
            content = config_file.read_text()
            content = content.replace("PROJECT_NAME", project_name)
            config_file.write_text(content)
        
        # Create __init__.py files
        print("📝 Creating __init__.py files...")
        init_files = [
            project_dir / "__init__.py",
            project_dir / "pages" / "__init__.py",
            project_dir / "tests" / "__init__.py",
            project_dir / "tests" / "selenium" / "__init__.py",
            project_dir / "tests" / "playwright" / "__init__.py",
        ]
        
        for init_file in init_files:
            if not init_file.exists():
                init_file.write_text('"""Package initialization."""\n')
        
        # Success message
        print()
        print("=" * 70)
        print(f"✅ Project '{project_name}' created successfully!")
        print("=" * 70)
        print()
        print("📚 Next steps:")
        print(f"   1. Update configuration: {config_file}")
        print(f"   2. Create page objects: {project_dir / 'pages'}")
        print(f"   3. Write tests: {project_dir / 'tests'}")
        print()
        print("🚀 Quick start:")
        print(f"   # Navigate to project")
        print(f"   cd {project_dir}")
        print()
        print(f"   # Create your first page object")
        print(f"   # Edit pages/home_page.py")
        print()
        print(f"   # Write your first test")
        print(f"   # Edit tests/selenium/test_homepage.py")
        print()
        print(f"   # Run tests")
        print(f"   pytest {project_dir}/tests/")
        print()
        print("📖 Documentation:")
        print(f"   - Project README: {project_dir / 'README.md'}")
        print(f"   - Page Objects Guide: {project_dir / 'pages' / 'README.md'}")
        print(f"   - Test Data Guide: {project_dir / 'test_data' / 'README.md'}")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating project: {str(e)}")
        # Clean up partial project if error occurred
        if project_dir.exists():
            print(f"🧹 Cleaning up partial project...")
            shutil.rmtree(project_dir)
        return False


def main():
    """Main entry point."""
    
    print()
    print("=" * 70)
    print("  Test Automation Framework - New Project Creator")
    print("=" * 70)
    print()
    
    # Check command line arguments
    if len(sys.argv) < 2:
        print("❌ Error: Project name is required")
        print()
        print("Usage:")
        print("   python scripts/create_new_project.py <project_name>")
        print()
        print("Example:")
        print("   python scripts/create_new_project.py my_ecommerce_site")
        print("   python scripts/create_new_project.py internal_portal")
        print("   python scripts/create_new_project.py api_tests")
        print()
        sys.exit(1)
    
    project_name = sys.argv[1]
    
    # Create project
    success = create_new_project(project_name)
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
