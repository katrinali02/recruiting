from itertools import product

# Constants
total_team_members = 20
monthly_price_per_customer = 100 #p
monthly_growth_rate = 25 #o
base_customers = 1000
monthly_churn_rate = 0.10 #d
new_business_acquisition_per_member = 5
account_manager_customer_limit = 25 
revenue_increase_rate = 0.20 #r
csat_increase_per_support = 0.01 #csat
churn_rate_reduction_per_csat = 0.15

# Function to calculate monthly revenue
def calculate_monthly_revenue(N, A, S, current_customers):
    # Revenue from New Business Acquisition
    revenue_acquisition = N * new_business_acquisition_per_member * monthly_price_per_customer

    # Revenue from Account Management (assuming an even distribution of customer management duration)
    revenue_account = A * account_manager_customer_limit * monthly_price_per_customer * ((1 + revenue_increase_rate)**6)

    # Adjusting for Churn
    churn_reduction = monthly_churn_rate - (monthly_churn_rate * S * csat_increase_per_support * churn_rate_reduction_per_csat)
    adjusted_customers = current_customers * (1 - churn_reduction)

    # Revenue from existing customers after churn
    revenue_existing = adjusted_customers * monthly_price_per_customer

    return revenue_acquisition + revenue_account + revenue_existing

# Function to find optimal distribution for a given number of months
def find_optimal_distribution(months):
    optimal_distributions = []
    total_revenue = 0
    current_customers = base_customers

    for month in range(months):
        max_revenue = 0
        optimal_distribution = (0, 0, 0)

        for N, A, S in product(range(total_team_members + 1), repeat=3):
            if N + A + S == total_team_members:
                monthly_revenue = calculate_monthly_revenue(N, A, S, current_customers)
                if monthly_revenue > max_revenue:
                    max_revenue = monthly_revenue
                    optimal_distribution = (N, A, S)

        total_revenue += max_revenue
        optimal_distributions.append(optimal_distribution)
        # Update customer base for next month
        current_customers = (current_customers - (current_customers * monthly_churn_rate) + (optimal_distribution[0] * new_business_acquisition_per_member) + monthly_growth_rate)

    return optimal_distributions, total_revenue

# User input for the number of months
months = int(input("Enter the number of months for the analysis (1-24): "))
optimal_distributions, total_revenue = find_optimal_distribution(months)

for i, dist in enumerate(optimal_distributions):
    print(f"Month {i+1}: Optimal distribution (New Business Acquisition, Account Management, Support): {dist}")
print(f"Total Maximum Revenue for {months} months: ${total_revenue:,.2f}")