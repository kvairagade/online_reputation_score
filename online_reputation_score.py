def get_listing_score(platform_presence: int, profile_completeness: float, total_platform: int = 20) -> float:
    platform_presence_percent = platform_presence / total_platform if total_platform != 0 else 0
    profile_completeness_percent = profile_completeness / platform_presence if platform_presence != 0 else 0
    listing_score = (0.3 * platform_presence_percent) + (0.7 * profile_completeness_percent)
    return round(listing_score * 10, 2) if listing_score > 0 else 0


def get_review_score(no_of_reviews_increased: int, last_reviews: int, overall_rating: float, text_reviews: int) -> float:
    total_reviews = last_reviews + no_of_reviews_increased
    increased_in_reviews_percent = no_of_reviews_increased / last_reviews if last_reviews != 0 else 0
    rating_percent = overall_rating / 5
    text_reviews_percent = text_reviews / total_reviews if total_reviews != 0 else 0
    reviews_score = (0.3 * increased_in_reviews_percent) + (0.4 * rating_percent) + (0.3 * text_reviews_percent)
    return reviews_score


def get_social_media_presence_score(platform_presence: int, profile_completeness: float, increased_in_post: int, last_posts: int, increased_in_engagement: float, last_engagement: float, total_platform: int = 20) -> float:
    platform_presence_percent = platform_presence / total_platform if total_platform != 0 else 0
    profile_completeness_percent = profile_completeness / platform_presence if platform_presence != 0 else 0
    increased_in_post_percent = increased_in_post / last_posts if last_posts != 0 else 0
    increased_in_engagement_percent = increased_in_engagement / last_engagement if last_engagement != 0 else 0
    social_media_presence_score = (0.2 * platform_presence_percent) + (0.2 * profile_completeness_percent) + (0.2 * increased_in_post_percent) + (0.4 * increased_in_engagement_percent)
    return round(social_media_presence_score * 10, 2) if social_media_presence_score > 0 else 0


def get_accessibility_score(no_of_working_days: int, no_of_working_hours: int, available_contact_channels: int, total_contact_channels: int = 6) -> float:
    operations_hours = no_of_working_hours * no_of_working_days
    operations_hour_percent = operations_hours / (24 * 7) if (24 * 7) != 0 else 0
    available_contact_channels_percent = available_contact_channels / total_contact_channels if total_contact_channels != 0 else 0
    phone_score = ((0.4 * operations_hour_percent) + (0.6 * available_contact_channels_percent)) / 10
    accessibility_score = (0.2 * phone_score) + (0.3 * operations_hour_percent) + (0.5 * available_contact_channels_percent)
    return round(accessibility_score * 10, 2)


def get_promotion_score(ad_reach_percent: float, ctr_percent: float, conversion_rate_percent: float, redemption_rate_percent: float, engagement_rate_percent: float, promotion_rate_percent: float, sales_lift_percent: float) -> float:
    ad_score = 0.3 * ad_reach_percent + 0.3 * ctr_percent + 0.4 * conversion_rate_percent
    promotion_score = 0.25 * redemption_rate_percent + 0.25 * engagement_rate_percent + 0.25 * promotion_rate_percent + 0.25 * sales_lift_percent
    final_promotion_score = 0.5 * ad_score + 0.5 * promotion_score
    return round(final_promotion_score * 10, 2)


def get_overall_score(listing_score: float, reviews_score: float, social_media_presence_score: float, accessibility_score: float, promotion_score: float) -> float:
    overall_score = (
        (0.20 * listing_score) + 
        (0.25 * reviews_score) + 
        (0.20 * social_media_presence_score) + 
        (0.25 * accessibility_score) + 
        (0.10 * promotion_score)
    )
    return round(overall_score, 2)


def get_final_score(overall_score,k,last_final_score,decay_factor):
    normalized_overall_score = 0.6 + (overall_score/10 * 6.5)
    print(f"overall_score- {overall_score}")
    print(f"normalized_overall_score- {normalized_overall_score}")
    sigmoid_adjustment = 3.5/(1 + 2.71828**(k*(normalized_overall_score-6.5)))
        
    if normalized_overall_score >= 7:
        final_score = (6.5 + sigmoid_adjustment)
    else:
        final_score = normalized_overall_score

    final_score = round(final_score,3)
    if last_final_score == final_score:
        t = 1
    else:
        t = 0

    decay_weight = (1-decay_factor)**t

    final_score = final_score * decay_weight
    final_score = min(round(final_score, 3), 9.89)
    return final_score


listing_score = get_listing_score(platform_presence = 20,
                                  profile_completeness = 1.0,
                                  total_platform = 20)

reviews_score = get_review_score(no_of_reviews_increased = 400,
                                 last_reviews = 255,
                                 overall_rating = 4.3,
                                 text_reviews = 300)

social_media_presence_score = get_social_media_presence_score(platform_presence = 10,
                                                              profile_completeness = 1.0,
                                                              increased_in_post = 1200,
                                                              last_posts = 1500,
                                                              increased_in_engagement = 0.8,
                                                              last_engagement = 0.1,
                                                              total_platform = 20)

accessibility_score = get_accessibility_score(no_of_working_days = 7,
                                              no_of_working_hours = 24,
                                              available_contact_channels = 6,
                                              total_contact_channels = 6)

promotion_score = get_promotion_score(ad_reach_percent = 0.8,
                                        ctr_percent = 0.8,
                                        conversion_rate_percent = 0.8,
                                        redemption_rate_percent = 0.8,
                                        engagement_rate_percent = 0.8,
                                        promotion_rate_percent = 0.8,
                                        sales_lift_percent = 0.8)

overall_score = get_overall_score(listing_score,
                                  reviews_score,
                                  social_media_presence_score,
                                  accessibility_score,
                                  promotion_score)

final_score = get_final_score(overall_score = overall_score,
                              k = -0.5,
                              last_final_score = 9.89,
                              decay_factor = 0.1)

print(f"final_score - {final_score}")
