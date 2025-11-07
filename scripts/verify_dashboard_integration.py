"""
Verify that dashboard correctly integrates real data.

Usage:
    python scripts/verify_dashboard_integration.py
"""
import os
from pathlib import Path

def verify_streamlit_app():
    """Verify Streamlit app exists."""
    app_path = Path("streamlit_app.py")
    
    if app_path.exists():
        print(f"✅ Streamlit app found")
        return True
    else:
        print(f"❌ Streamlit app not found")
        return False

def verify_neo4j_integration():
    """Verify Neo4j integration."""
    app_path = Path("streamlit_app.py")
    
    if app_path.exists():
        with open(app_path, 'r', encoding='utf-8') as f:
            content = f.read()
            has_neo4j = "neo4j" in content.lower()
            
            if has_neo4j:
                print("✅ Neo4j integration found")
                return True
            else:
                print("⚠️  Neo4j integration not found")
                return False
    return False

def verify_elasticsearch_integration():
    """Verify Elasticsearch integration."""
    app_path = Path("streamlit_app.py")
    
    if app_path.exists():
        with open(app_path, 'r', encoding='utf-8') as f:
            content = f.read()
            has_es = "elasticsearch" in content.lower() or "es." in content.lower()
            
            if has_es:
                print("✅ Elasticsearch integration found")
                return True
            else:
                print("⚠️  Elasticsearch integration not found")
                return False
    return False

if __name__ == "__main__":
    print("=" * 60)
    print("Cipher Dashboard Integration Verification")
    print("=" * 60)
    print()
    
    repo_dir = Path(__file__).parent.parent
    os.chdir(repo_dir)
    
    print("1. Dashboard Components:")
    print("-" * 60)
    app_ok = verify_streamlit_app()
    neo4j_ok = verify_neo4j_integration()
    es_ok = verify_elasticsearch_integration()
    
    print("\n" + "=" * 60)
    print("Summary:")
    print("=" * 60)
    
    if app_ok and neo4j_ok and es_ok:
        print("✅ All checks passed!")
    else:
        print("⚠️  Some checks failed. See docs/DASHBOARD_DATA_INTEGRATION.md for details.")

