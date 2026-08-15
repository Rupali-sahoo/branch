class RecommendationAgent:

    def generate(
        self,
        fatigue_score,
        risk_level,
        rag_context
    ):
        if risk_level == "High":
            recommendation = (
                "Your fatigue indicators are high. "
                "Please take a break, get adequate rest, "
                "and avoid prolonged activities if you feel drowsy."
            )

        elif risk_level == "Medium":
            recommendation = (
                "Your fatigue indicators are moderate. "
                "Consider taking a short break and getting sufficient rest."
            )

        else:
            recommendation = (
                "Your fatigue indicators are low. "
                "Continue maintaining healthy sleep and rest habits."
            )

        return recommendation