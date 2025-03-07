import argparse
from get_papers.fetch_papers import fetch_papers
import pandas as pd

def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed.")
    parser.add_argument("query", type=str, help="Search query for PubMed.")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode.")
    parser.add_argument("-f", "--file", type=str, help="Save results to a CSV file.")
    args = parser.parse_args()

    if args.debug:
        print("Debug mode enabled.")

    papers = fetch_papers(args.query)
    df = pd.DataFrame(papers)

    if args.file:
        df.to_csv(args.file, index=False)
        print(f"Results saved to {args.file}.")
    else:
        print(df.to_string(index=False))

if __name__ == "__main__":
    main()