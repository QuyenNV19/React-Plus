import sys
import os

project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

from search_service.search_engine import SearchEngine

def main():
    engine = SearchEngine()
    print("Testing search engine...")
    results = engine.search_by_name("Canxi", size=2)
    print("Results:")
    for res in results:
        print(f"- {res['name']}")

if __name__ == "__main__":
    main()
