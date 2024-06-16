from itertools import product

# Constants
total_team_members = 20
monthly_price_per_customer = 100
monthly_growth_rate = 25
base_customers = 1000
monthly_churn_rate = 0.10
new_business_acquisition_per_member = 5
account_manager_customer_limit = 25
revenue_increase_rate = 0.20
csat_increase_per_support = 0.01
churn_rate_reduction_per_csat = 0.15

# Function to calculate Customer Lifetime Value (CLTV)
def calculate_cltv(arpu, churn_rate):
    lt = 1 / churn_rate if churn_rate else float('inf')
    return arpu * lt

# Function to calculate monthly revenue
def calculate_monthly_revenue(N, A, S, current_customers):
    # Revenue from New Business Acquisition
    revenue_acquisition = N * new_business_acquisition_per_member * monthly_price_per_customer

    # Revenue from Account Management
    revenue_account = A * account_manager_customer_limit * monthly_price_per_customer * ((1 + revenue_increase_rate)**6)

    # Adjusting for Churn
    churn_reduction = S * csat_increase_per_support * churn_rate_reduction_per_csat
    adjusted_churn_rate = monthly_churn_rate - churn_reduction

    # Revenue from existing customers after churn
    adjusted_customers = current_customers * (1 - adjusted_churn_rate)
    revenue_existing = adjusted_customers * monthly_price_per_customer

    # Calculate ARPU
    arpu = monthly_price_per_customer # As ARPU is constant per user

    return revenue_acquisition + revenue_account + revenue_existing, adjusted_churn_rate, arpu

# Function to find optimal distribution for a given number of months
def find_optimal_distribution(months):
    optimal_distributions = []
    total_revenue = 0
    total_cltv = 0
    current_customers = base_customers

    for months in range(months):
        max_revenue = 0
        max_cltv = 0
        optimal_distribution = (0, 0, 0)

        for N, A, S in product(range(total_team_members + 1), repeat=3):
            if N + A + S == total_team_members:
                monthly_revenue, adjusted_churn_rate, arpu = calculate_monthly_revenue(N, A, S, current_customers)
                monthly_cltv = calculate_cltv(arpu, adjusted_churn_rate) * current_customers
                if monthly_cltv > max_cltv:  # Optimize for CLTV
                    max_revenue = monthly_revenue
                    max_cltv = monthly_cltv
                    optimal_distribution = (N, A, S)

        total_revenue += max_revenue
        total_cltv += max_cltv
        optimal_distributions.append(optimal_distribution)
        # Update customer base for next month
        current_customers = (current_customers - (current_customers * adjusted_churn_rate) + (optimal_distribution[0] * new_business_acquisition_per_member) + monthly_growth_rate)

    return optimal_distributions, total_revenue, total_cltv

# Assume user input for months is 24 for the simulation to run
months = 24
optimal_distributions, total_revenue, total_cltv = find_optimal_distribution(months)

for i, dist in enumerate(optimal_distributions):
    print(f"Month {i+1}: Optimal distribution (New Business Acquisition, Account Management, Support): {dist}")
print(f"Total Maximum Revenue for {months} months: ${total_revenue:,.2f}")
print(f"Total Maximum CLTV for {months} months: ${total_cltv:,.2f}")
