"""
Recommendation algorithm.
"""

from abc import ABC, abstractmethod
from core.models import Rating

class RecStrat(ABC):
    """
    All strategies need to define a `calculate_score` method.
    """
    @abstractmethod
    def calculate_score(self, rating):
        raise NotImplementedError("Please implement a `calculate_score` method for the strategy")

class NotEnoughRatedRestaurantsError(Exception):
    """
    Error for a user not having enough ratings of unique restaurants.
    """
    pass

class RepeatInterestWeightStrategy(RecStrat):
    """
    Calculates score based on weights,
    would_eat_again being the most important factor.
    """
    weight_dict = {
            "would_eat_again":0.3,
            "taste":0.25,
            "quality":0.2,
            "price":0.15,
            "wait":0.1
    }

    def calculate_score(self, rating):
        score = (
            rating.would_eat_again * self.weight_dict["would_eat_again"]
            + rating.taste * self.weight_dict["taste"]
            + rating.quality * self.weight_dict["quality"]
            + rating.price * self.weight_dict["price"]
            + rating.wait * self.weight_dict["wait"]
        )

        return score

class TopXEngine:
    """
    Ranking engine, which builds a top 'X' list.

    The engine retrieves a user's ratings, scores each visit using the declared strategy,
    averages the scores in repeated-visit cases, returns the highest-ranked restaurants.
    
    Args:

        `min_restaurants`: decide the required minimum ratings of unique restaurants before ranking generation is possible.
        `limit`: decides how many restaurants are displayed, i.e. limit=3 -> top 3.
        `strategy`: decides the strategy used for calculation. All strategies should inherit from RecStrat.
    """
    def __init__(self, min_restaurants, limit, strategy):

        self.min_restaurants = min_restaurants
        self.limit = limit
        self.strategy = strategy

    def get_top_restaurants(self, user):

        # Extraction and aggregation of Ratings.
        ratings = list(
            Rating.objects
            .filter(user=user)
            .select_related("experience", "experience__restaurant")
        )

        # Validation of user having a minimum of [min_restaurants] rated visits to unique restaurants.
        unique_rated_restaurants = {rating.experience.restaurant_id for rating in ratings}

        if len(unique_rated_restaurants) < self.min_restaurants:
            raise NotEnoughRatedRestaurantsError(
                    f"Rate at least {self.min_restaurants} restaurants to generate the ranking"
                    )
               
        # Building the ranking and calculating using Strategy class's calculation method.
        ranking = dict()

        for rating in ratings:
            restaurant = rating.experience.restaurant
            score = self.strategy.calculate_score(rating)

            if restaurant.id not in ranking:
                ranking[restaurant.id] = {
                    "restaurant": restaurant,
                    "scores": [],
                }

            ranking[restaurant.id]["scores"].append(score)

        # Handling many ratings for one restaurant cases and building output.
        recommendations = list()

        for restaurant_data in ranking.values():
            scores = restaurant_data["scores"]
            avg_score = sum(scores) / len(scores)

            recommendations.append(
                {
                    "restaurant": restaurant_data["restaurant"],
                    "score": round(avg_score, 2),
                    "ratings_count": len(scores),
                }
            )

        recommendations.sort(key=lambda recommendation: recommendation["score"], reverse=True)

        return recommendations[:self.limit]
