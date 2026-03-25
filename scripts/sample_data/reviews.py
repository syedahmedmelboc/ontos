"""
Review data generator for restaurant sample data.

Generates realistic customer reviews including:
- Ratings (1-5 stars with realistic distribution)
- Review text
- Customer and order references
- Timestamps
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

from faker import Faker

from config import FAKER_SEED, EntityCounts, REVIEW_RATING_DISTRIBUTION
from utils import (
    generate_short_id,
    weighted_choice_int,
    write_json,
    write_csv
)

# Initialize Faker with fixed seed
fake = Faker()
Faker.seed(FAKER_SEED)
random.seed(FAKER_SEED)


# Review text templates by rating
REVIEW_TEMPLATES = {
    5: [
        "Absolutely fantastic experience! The food was incredible and the service was impeccable.",
        "Best restaurant in town! Every dish was perfectly prepared.",
        "Outstanding! From the moment we walked in, everything was perfect.",
        "A truly memorable dining experience. Will definitely be back!",
        "Five stars isn't enough! This place exceeded all expectations.",
        "The chef clearly knows what they're doing. Every bite was divine.",
        "Perfect for our anniversary dinner. Romantic ambiance and amazing food.",
        "We've been coming here for years and it never disappoints!",
    ],
    4: [
        "Really good food and service. Minor issues but overall great.",
        "Enjoyed our meal very much. Will recommend to friends.",
        "Solid choice for dinner. Good portion sizes and fair prices.",
        "Very satisfied with our experience. A few small improvements could be made.",
        "Good food, friendly staff. A bit of a wait but worth it.",
        "Consistently good. This is our go-to spot for Italian.",
        "Pleasantly surprised by the quality. Will return.",
        "Great food, reasonable prices. Service was a bit slow.",
    ],
    3: [
        "Decent food, nothing special but not bad either.",
        "Average experience. Some dishes were good, others just okay.",
        "It was fine. Probably wouldn't go out of my way to come back.",
        "Middle of the road. Not bad, not great.",
        "The food was alright but the service could use some improvement.",
        "Mixed feelings. Great appetizers but main courses were underwhelming.",
        "Acceptable for a quick meal but not for a special occasion.",
        "Just okay. Expected more based on the reviews.",
    ],
    2: [
        "Disappointing experience. Food was cold and service was slow.",
        "Not worth the price. Many better options in the area.",
        "Had high hopes but left disappointed. Won't be returning.",
        "Service was poor and the food was mediocre at best.",
        "Waited too long for average food. Not impressed.",
        "Several issues with our order. Management didn't seem to care.",
        "The quality has gone downhill. Used to be much better.",
        "Overpriced for what you get. Better options nearby.",
    ],
    1: [
        "Terrible experience from start to finish. Avoid this place.",
        "Food was inedible. Sent it back and left hungry.",
        "Worst restaurant experience I've had in years.",
        "Completely unacceptable. Health department should investigate.",
        "Rude staff, cold food, overpriced. Stay away!",
        "Got sick after eating here. Never again.",
        "Absolutely horrible. How is this place still in business?",
        "Zero stars if I could. Total waste of money.",
    ],
}


def generate_review(
    review_id: str,
    customers: List[Dict[str, Any]],
    orders: List[Dict[str, Any]],
    orders_by_id: Dict[str, Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Generate a single review record.
    
    Args:
        review_id: Unique identifier
        customers: List of customers to select from
        orders: List of orders to select from
        orders_by_id: Order lookup dictionary
        
    Returns:
        Dictionary containing review data
    """
    # Select a completed order (reviews come from completed orders)
    completed_orders = [o for o in orders if o["status"] == "completed"]
    
    if not completed_orders:
        return None
    
    order = random.choice(completed_orders)
    order_id = order["order_id"]
    customer_id = order.get("customer_id")
    
    # If order has no customer, sometimes assign anonymous review
    if not customer_id:
        if random.random() < 0.5 and customers:
            customer_id = random.choice(customers)["customer_id"]
        else:
            customer_id = None
    
    # Generate rating (weighted distribution)
    rating = weighted_choice_int(REVIEW_RATING_DISTRIBUTION)
    
    # Generate review text based on rating
    base_text = random.choice(REVIEW_TEMPLATES[rating])
    
    # Sometimes add additional comments
    if random.random() < 0.4:
        additional = fake.sentence(nb_words=random.randint(5, 15))
        base_text = f"{base_text} {additional}"
    
    # Review date is after order date
    order_date = datetime.fromisoformat(order["created_at"])
    review_date = order_date + timedelta(
        days=random.randint(0, 14),
        hours=random.randint(0, 12)
    )
    
    # Generate review aspects (what they're reviewing)
    aspects = []
    if random.random() < 0.6:
        aspects.append("food_quality")
    if random.random() < 0.4:
        aspects.append("service")
    if random.random() < 0.3:
        aspects.append("ambiance")
    if random.random() < 0.2:
        aspects.append("value")
    
    return {
        "review_id": review_id,
        "order_id": order_id,
        "customer_id": customer_id,
        "rating": rating,
        "review_text": base_text,
        "aspects": aspects,
        "is_verified": True,  # Verified because linked to actual order
        "helpful_count": random.randint(0, 50) if rating in [1, 5] else random.randint(0, 10),
        "response_text": generate_response(rating) if random.random() < 0.3 else None,
        "response_date": (review_date + timedelta(days=random.randint(1, 3))).isoformat() if random.random() < 0.3 else None,
        "created_at": review_date.isoformat(),
        "source": random.choice(["website", "mobile_app", "google", "yelp", "internal"]),
    }


def generate_response(rating: int) -> str:
    """Generate a management response based on rating."""
    if rating >= 4:
        responses = [
            "Thank you so much for your kind words! We're thrilled you enjoyed your experience.",
            "We appreciate you taking the time to share your feedback. Hope to see you again soon!",
            "Thank you for the wonderful review! Our team will be delighted to hear this.",
        ]
    elif rating == 3:
        responses = [
            "Thank you for your feedback. We're always looking to improve and appreciate your input.",
            "We appreciate you sharing your experience. We'll work on the areas you mentioned.",
            "Thanks for the honest review. We hope to exceed your expectations next time.",
        ]
    else:
        responses = [
            "We're sorry to hear about your experience. Please contact us directly so we can make it right.",
            "We apologize for falling short. Your feedback helps us improve.",
            "Thank you for bringing this to our attention. We'd like to make this right for you.",
        ]
    return random.choice(responses)


def generate_reviews(
    customers: List[Dict[str, Any]],
    orders: List[Dict[str, Any]],
    count: int = None
) -> List[Dict[str, Any]]:
    """
    Generate multiple reviews.
    
    Args:
        customers: List of customers
        orders: List of orders
        count: Number of reviews to generate
        
    Returns:
        List of review dictionaries
    """
    if count is None:
        count = EntityCounts.reviews
    
    reviews = []
    used_ids = set()
    
    # Create order lookup
    orders_by_id = {o["order_id"]: o for o in orders}
    
    # Track which orders have been reviewed
    reviewed_orders = set()
    
    attempts = 0
    while len(reviews) < count and attempts < count * 2:
        review_id = f"REV-{generate_short_id(length=6)}"
        while review_id in used_ids:
            review_id = f"REV-{generate_short_id(length=6)}"
        
        review = generate_review(review_id, customers, orders, orders_by_id)
        
        if review and review["order_id"] not in reviewed_orders:
            used_ids.add(review_id)
            reviewed_orders.add(review["order_id"])
            reviews.append(review)
        
        attempts += 1
    
    return reviews


def main(
    customers: List[Dict[str, Any]],
    orders: List[Dict[str, Any]],
    output_dir: str = "output"
) -> List[Dict[str, Any]]:
    """
    Main function to generate and save review data.
    
    Args:
        customers: List of customers
        orders: List of orders
        output_dir: Directory to save output files
        
    Returns:
        List of generated reviews
    """
    print("\n⭐ Generating review data...")
    
    reviews = generate_reviews(customers, orders)
    
    # Save to files
    write_json(reviews, "reviews.json", output_dir)
    write_csv(reviews, "reviews.csv", output_dir)
    
    # Print summary stats
    print(f"  📊 Generated {len(reviews)} reviews")
    
    # Rating distribution
    rating_counts = {}
    for review in reviews:
        rating = review["rating"]
        rating_counts[rating] = rating_counts.get(rating, 0) + 1
    
    print("  📊 Rating distribution:")
    for rating in [5, 4, 3, 2, 1]:
        count = rating_counts.get(rating, 0)
        pct = (count / len(reviews)) * 100
        stars = "⭐" * rating
        print(f"     {stars} ({rating} stars): {count} ({pct:.1f}%)")
    
    # Average rating
    avg_rating = sum(r["rating"] for r in reviews) / len(reviews)
    print(f"  📊 Average rating: {avg_rating:.2f}")
    
    # Response rate
    responded = sum(1 for r in reviews if r["response_text"])
    response_rate = (responded / len(reviews)) * 100
    print(f"  📊 Management response rate: {response_rate:.1f}%")
    
    return reviews


if __name__ == "__main__":
    print("This module requires customers and orders data.")
    print("Run generate_all.py instead.")
