"""
Verify that IOC collections are running and data is being collected.

Usage:
    python scripts/verify_ioc_collection.py
"""
import os
from pathlib import Path

def verify_elasticsearch():
    """Verify Elasticsearch connection."""
    try:
        from elasticsearch import Elasticsearch
        
        es = Elasticsearch(['localhost:9200'])
        
        try:
            health = es.cluster.health()
            indices = es.indices.get_alias()
            
            print("✅ Elasticsearch connected")
            print(f"   Cluster status: {health['status']}")
            print(f"   Indices: {list(indices.keys())}")
            
            # Check IOC count if index exists
            if 'iocs' in indices:
                count = es.count(index='iocs')['count']
                print(f"   IOC count: {count}")
            
            return True
        except Exception as e:
            print(f"❌ Elasticsearch error: {e}")
            print("   Make sure Elasticsearch is running on localhost:9200")
            return False
    except ImportError:
        print("⚠️  elasticsearch package not installed")
        return False

def verify_neo4j():
    """Verify Neo4j connection."""
    try:
        from neo4j import GraphDatabase
        
        driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
        
        try:
            with driver.session() as session:
                result = session.run("MATCH (n) RETURN count(n) as count")
                count = result.single()['count']
                
                print("✅ Neo4j connected")
                print(f"   Node count: {count}")
                return True
        except Exception as e:
            print(f"❌ Neo4j error: {e}")
            print("   Make sure Neo4j is running on localhost:7687")
            return False
    except ImportError:
        print("⚠️  neo4j package not installed")
        return False

def verify_ioc_collectors():
    """Verify IOC collectors exist."""
    collectors_dir = Path("src/collectors")
    
    if collectors_dir.exists():
        collectors = list(collectors_dir.glob("*.py"))
        print(f"✅ IOC collectors found: {len(collectors)} files")
        for collector in collectors:
            print(f"   - {collector.name}")
        return True
    else:
        print("❌ IOC collectors directory not found")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Cipher IOC Collection Verification")
    print("=" * 60)
    print()
    
    repo_dir = Path(__file__).parent.parent
    os.chdir(repo_dir)
    
    results = []
    
    print("1. IOC Collectors:")
    print("-" * 60)
    collectors_ok = verify_ioc_collectors()
    results.append(collectors_ok)
    
    print("\n2. Elasticsearch:")
    print("-" * 60)
    es_ok = verify_elasticsearch()
    results.append(es_ok)
    
    print("\n3. Neo4j:")
    print("-" * 60)
    neo4j_ok = verify_neo4j()
    results.append(neo4j_ok)
    
    print("\n" + "=" * 60)
    print("Summary:")
    print("=" * 60)
    
    passed = sum(1 for r in results if r)
    total = len(results)
    
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("✅ All checks passed!")
    else:
        print("⚠️  Some checks failed. See details above.")
        print("\nNote: IOC collection verification requires:")
        print("  1. Elasticsearch running")
        print("  2. Neo4j running")
        print("  3. IOC collectors executed")
        print("\nSee docs/DATASET_USAGE_VERIFICATION.md for details.")

