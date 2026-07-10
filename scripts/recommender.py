import pandas as pd
import argparse

def get_recommendations(risk_appetite, n=3):
    """
    Given a risk appetite ('Low', 'Moderate', 'High'), returns the top n funds
    by sharpe ratio within that risk grade.
    """
    try:
        perf_df = pd.read_csv('data/processed/07_scheme_performance.csv')
    except FileNotFoundError:
        print("Error: Could not find 'data/processed/07_scheme_performance.csv'. Make sure you run this from the project root.")
        return

    # Standardize input
    risk_appetite = risk_appetite.capitalize()
    valid_grades = ['Low', 'Low to Moderate', 'Moderate', 'Moderately High', 'High', 'Very High']
    
    # Map input to risk grades
    if risk_appetite == 'Low':
        match_grades = ['Low', 'Low to Moderate']
    elif risk_appetite == 'Moderate':
        match_grades = ['Moderate', 'Moderately High']
    elif risk_appetite == 'High':
        match_grades = ['High', 'Very High']
    else:
        print(f"Error: '{risk_appetite}' is not a valid risk appetite. Please choose from: Low, Moderate, High.")
        return
        
    filtered = perf_df[perf_df['risk_grade'].isin(match_grades)].copy()
    
    if filtered.empty:
        print(f"No funds found for risk appetite '{risk_appetite}'.")
        return
        
    # Sort by sharpe_ratio descending
    top_funds = filtered.sort_values('sharpe_ratio', ascending=False).head(n)
    
    print("="*60)
    print(f"   TOP {n} FUND RECOMMENDATIONS (Risk: {risk_appetite.upper()})")
    print("="*60)
    
    table_data = top_funds[['scheme_name', 'category', 'risk_grade', 'sharpe_ratio', 'return_3yr_pct']]
    # Format the table for printing
    print(table_data.to_string(index=False, justify='left'))
    print("="*60)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple Mutual Fund Recommender')
    parser.add_argument('risk', type=str, nargs='?', default='Moderate', 
                        help="Risk appetite: Low, Moderate, or High (default: Moderate)")
    args = parser.parse_args()
    
    get_recommendations(args.risk)
