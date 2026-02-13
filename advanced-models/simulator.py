"""
Portfolio Performance Simulator
Ads Optimization Framework – Advanced Models

This simulator models:
- Blended ROAS
- Marginal ROAS
- Budget scaling impact
- Diminishing returns detection
"""

import numpy as np


class Campaign:
    def __init__(self, name, base_roas, saturation_point):
        """
        name: Campaign name
        base_roas: Initial ROAS at low spend
        saturation_point: Spend level where efficiency starts declining
        """
        self.name = name
        self.base_roas = base_roas
        self.saturation_point = saturation_point

    def simulate_roas(self, spend):
        """
        Simulates diminishing returns as spend increases.
        """
        if spend <= self.saturation_point:
            return self.base_roas
        else:
            decay_factor = (spend - self.saturation_point) / self.saturation_point
            return max(self.base_roas * (1 - 0.2 * decay_factor), 0.5)


def simulate_portfolio(campaigns, spend_allocation):
    total_spend = 0
    total_revenue = 0

    for campaign, spend in zip(campaigns, spend_allocation):
        roas = campaign.simulate_roas(spend)
        revenue = spend * roas

        total_spend += spend
        total_revenue += revenue

        print(f"{campaign.name}")
        print(f"  Spend: ${spend}")
        print(f"  Simulated ROAS: {round(roas,2)}")
        print(f"  Revenue: ${round(revenue,2)}\n")

    blended_roas = total_revenue / total_spend

    print("------ Portfolio Summary ------")
    print(f"Total Spend: ${total_spend}")
    print(f"Total Revenue: ${round(total_revenue,2)}")
    print(f"Blended ROAS: {round(blended_roas,2)}")

    return blended_roas


if __name__ == "__main__":

    # Define campaigns
    campaign_a = Campaign("Growth Campaign", base_roas=3.5, saturation_point=20000)
    campaign_b = Campaign("Profitability Campaign", base_roas=4.2, saturation_point=15000)
    campaign_c = Campaign("Testing Campaign", base_roas=2.5, saturation_point=8000)

    campaigns = [campaign_a, campaign_b, campaign_c]

    # Define spend allocation
    spend_allocation = [25000, 18000, 10000]

    simulate_portfolio(campaigns, spend_allocation)
