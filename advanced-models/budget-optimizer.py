"""
Portfolio Budget Optimizer
Ads Optimization Framework – Advanced Models

Objective:
Automatically allocate budget across campaigns
to maximize blended ROAS under constraints.

Constraints:
- Total budget fixed
- Maintain minimum ROAS threshold
"""

import numpy as np


class Campaign:
    def __init__(self, name, base_roas, saturation_point):
        self.name = name
        self.base_roas = base_roas
        self.saturation_point = saturation_point

    def simulate_roas(self, spend):
        """
        Diminishing returns model.
        """
        if spend <= self.saturation_point:
            return self.base_roas
        else:
            decay_factor = (spend - self.saturation_point) / self.saturation_point
            return max(self.base_roas * (1 - 0.2 * decay_factor), 0.5)


def optimize_budget(campaigns, total_budget, min_roas=2.5, step=1000):

    allocation = np.zeros(len(campaigns))
    remaining_budget = total_budget

    while remaining_budget > 0:

        best_index = None
        best_marginal_roas = 0

        for i, campaign in enumerate(campaigns):

            current_spend = allocation[i]
            current_roas = campaign.simulate_roas(current_spend)
            new_roas = campaign.simulate_roas(current_spend + step)

            marginal_revenue = (current_spend + step) * new_roas - \
                               current_spend * current_roas

            marginal_roas = marginal_revenue / step

            if marginal_roas > best_marginal_roas and marginal_roas >= min_roas:
                best_marginal_roas = marginal_roas
                best_index = i

        if best_index is None:
            break

        allocation[best_index] += step
        remaining_budget -= step

    return allocation


def portfolio_summary(campaigns, allocation):
    total_spend = sum(allocation)
    total_revenue = 0

    for campaign, spend in zip(campaigns, allocation):
        roas = campaign.simulate_roas(spend)
        revenue = spend * roas
        total_revenue += revenue

        print(f"{campaign.name}")
        print(f"  Spend: ${spend}")
        print(f"  ROAS: {round(roas,2)}")
        print(f"  Revenue: ${round(revenue,2)}\n")

    blended_roas = total_revenue / total_spend if total_spend > 0 else 0

    print("------ Optimized Portfolio ------")
    print(f"Total Spend: ${total_spend}")
    print(f"Total Revenue: ${round(total_revenue,2)}")
    print(f"Blended ROAS: {round(blended_roas,2)}")


if __name__ == "__main__":

    campaign_a = Campaign("Growth Campaign", 3.5, 20000)
    campaign_b = Campaign("Profitability Campaign", 4.2, 15000)
    campaign_c = Campaign("Testing Campaign", 2.5, 8000)

    campaigns = [campaign_a, campaign_b, campaign_c]

    total_budget = 50000
    min_roas_constraint = 3.0

    optimal_allocation = optimize_budget(
        campaigns,
        total_budget,
        min_roas=min_roas_constraint
    )

    portfolio_summary(campaigns, optimal_allocation)
