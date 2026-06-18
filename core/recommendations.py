from abc import ABC, abstractmethod
from core.models import Rating

class RecStrat(ABC):
    @abstractmethod
    def calculate_score(self, rating):
        pass

class NotEnoughRatingsError(Exception):
    pass

class RepeatInterestStrategy(RecStrat):
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

        return round(score, 2)

class RecEngine:

    minimum_ratings = 3

    def __init__(self, strategy=None):
        if strategy is None:
            strategy = RepeatInterestStrategy()
        self.strategy = strategy

    def get_user_ratings(self, user):
        
        return list(
            Rating.objects
            .filter(user=user)
            .select_related("experience", "experience__restaurant")
        )

    def get_top_restaurants(self, user, limit=5):
        ratings = self.get_user_ratings(user)

        if len(ratings) < self.minimum_ratings:
            raise NotEnoughRatingsError(
                f"At least {self.minimum_ratings} ratings are needed to generate recommendations"
            )

        restaurant_scores = dict()

        for rating in ratings:
            restaurant = rating.experience.restaurant
            score = self.strategy.calculate_score(rating)

            if restaurant.id not in restaurant_scores:
                restaurant_scores[restaurant.id] = {
                    "restaurant": restaurant,
                    "scores": [],
                }

            restaurant_scores[restaurant.id]["scores"].append(score)

        recommendations = list()

        for restaurant_data in restaurant_scores.values():
            scores = restaurant_data["scores"]
            avg_score = sum(scores) / len(scores)

            recommendations.append(
                {
                    "restaurant": restaurant_data["restaurant"],
                    "score": round(avg_score, 2),
                    "ratings_count": len(scores),
                }
            )

        def get_score(recommendation):
            return recommendation["score"]

        recommendations.sort(key=get_score, reverse=True)

        return recommendations[:limit]
