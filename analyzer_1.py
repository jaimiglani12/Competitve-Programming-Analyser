import pandas as pd
from datetime import datetime
from fetch_data import fetch_codeforces_submissions
from fetch_info import fetch_user_info
import requests


def tags(handle):
    submissions = fetch_codeforces_submissions(handle)
    topic_count = {}
    for sub in submissions:
        tag_list = sub["problem"]["tags"]
        verdict = sub["verdict"]
        if verdict != "OK":
            continue
        for tag in tag_list:
            topic_count[tag] = topic_count.get(tag, 0) + 1
    topic_count = dict(sorted(topic_count.items(), key=lambda x: x[1], reverse=True))
    return topic_count


def analyze_tags(handle):
    submissions = fetch_codeforces_submissions(handle)
    topic_count = {}
    total_solved = 0
    top_topics = {}
    weak_topics = {}

    for sub in submissions:
        tag_list = sub["problem"]["tags"]
        verdict = sub["verdict"]
        if verdict != "OK":
            continue
        total_solved += 1
        for tag in tag_list:
            topic_count[tag] = topic_count.get(tag, 0) + 1
        topic_count = dict(sorted(topic_count.items(), key=lambda x: x[1], reverse=True))
        top_topics = dict(list(topic_count.items())[0:3])
        weak_topics = dict(list(topic_count.items())[-2:])

    return {
        "user": handle,
        "total submissions": len(submissions),
        "total_solved": total_solved,
        "top topics": top_topics,
        "weak topics": weak_topics
    }


def dif_analysis(handle):
    submissions = fetch_codeforces_submissions(handle)
    harder = 0
    rating_sum = 0
    problem_count = 0
    easy = 0
    hard = 0
    medium = 0

    for sub in submissions:
        verdict = sub.get("verdict", {})
        if verdict != "OK":
            continue
        problem = sub.get("problem", {})
        rating = problem.get("rating")
        if rating is None:
            continue
        if rating > harder:
            harder = rating
        rating_sum += rating
        problem_count += 1
        if rating <= 1200:
            easy += 1
        elif rating <= 1800:
            medium += 1
        else:
            hard += 1

    # Guard against zero division
    if problem_count == 0:
        return {
            "handle": handle,
            "average_rating": 0,
            "hardest_problem": 0,
            "easy_problems": 0,
            "medium_problems": 0,
            "hard_problems": 0
        }

    average_rating = rating_sum / problem_count
    return {
        "handle": handle,
        "average_rating": round(average_rating, 2),
        "hardest_problem": harder,
        "easy_problems": easy,
        "medium_problems": medium,
        "hard_problems": hard
    }


def analysis(handle):
    info = fetch_user_info(handle)
    if not info:
        return {"error": "User not found"}

    user = info[0]
    reg_time = user.get("registrationTimeSeconds")
    registration_year = None
    if reg_time:
        registration_year = datetime.fromtimestamp(reg_time).year

    return {
        "handle": user.get("handle"),
        "current_rating": user.get("rating", "Unrated"),
        "max_rating": user.get("maxRating", "Unrated"),
        "rank": user.get("rank", "Unrated"),
        "max_rank": user.get("maxRank", "Unrated"),
        "contribution": user.get("contribution", 0),
        "friends_of_count": user.get("friendOfCount", 0),
        "registration_year": registration_year
    }


def dash(handle):
    profile = analysis(handle)
    skills = analyze_tags(handle)
    difficulty = dif_analysis(handle)
    topics = tags(handle)

    if "error" in profile:
        return profile

    return {
        "handle": handle,
        "profile": profile,
        "skills": skills,
        "difficulty": difficulty,
        "topics": topics
    }


def insights_analysis(handle):
    data = dash(handle)

    if "error" in data:
        return data

    insights = []
    topics = data["topics"]
    difficulty = data["difficulty"]

    if not topics:
        insights.append("No solved problems found. Start solving to get insights!")
        return {"handle": handle, "insights": insights}

    strongest_topic = max(topics, key=topics.get)
    insights.append(f"You are strong in {strongest_topic} problems.")

    weak_topics = [t for t, c in topics.items() if c <= 5]
    if weak_topics:
        insights.append(f"You should practice more {', '.join(weak_topics[:3])} problems.")

    avg_rating = difficulty.get("average_rating", 0)

    if avg_rating == 0:
        insights.append("Solve more rated problems to get difficulty insights.")
    elif avg_rating < 1200:
        insights.append("You are solving mostly easy problems. Try harder ones.")
    elif avg_rating < 1600:
        insights.append("Good progress! Start attempting medium-hard problems.")
    else:
        insights.append("Great level! Try advanced and contest-level challenges.")

    if avg_rating:
        next_target = int(avg_rating + 200)
        insights.append(f"Recommended next goal: solve problems around {next_target} rating.")

    return {"handle": handle, "insights": insights}


def user_prog(handle: str):
    url = f"https://codeforces.com/api/user.status?handle={handle}"
    response = requests.get(url)
    data = response.json()

    if data["status"] != "OK":
        return {"error": "Failed to fetch submissions"}

    submissions = data["result"]
    total_submissions = len(submissions)
    monthly_activity = {}
    solved_ratings = []

    for sub in submissions:
        timestamp = sub["creationTimeSeconds"]
        month = datetime.fromtimestamp(timestamp).month
        monthly_activity[month] = monthly_activity.get(month, 0) + 1
        if sub.get("verdict") == "OK":
            rating = sub.get("problem", {}).get("rating")
            if rating:
                solved_ratings.append(rating)

    most_active_month = None
    if monthly_activity:
        most_active_month = max(monthly_activity, key=monthly_activity.get)

    rating_trend = "Not enough data"
    if len(solved_ratings) >= 10:
        mid = len(solved_ratings) // 2
        early = solved_ratings[:mid]
        recent = solved_ratings[mid:]
        early_avg = sum(early) / len(early)
        recent_avg = sum(recent) / len(recent)
        if recent_avg > early_avg:
            rating_trend = "Improving 📈"
        elif abs(recent_avg - early_avg) < 50:
            rating_trend = "Stable ➖"
        else:
            rating_trend = "Declining 📉"

    return {
        "handle": handle,
        "total_submissions": total_submissions,
        "most_active_month": most_active_month,
        "rating_trend": rating_trend,
        "monthly_activity": monthly_activity
    }


def contest_analysis(handle):
    url = f"https://codeforces.com/api/user.rating?handle={handle}"
    response = requests.get(url)
    data = response.json()
    contests = data["result"]

    if not contests:
        return {
            "handle": handle,
            "message": "User has not participated in contests."
        }

    total_contests = len(contests)
    ranking = []
    rating = []

    for contest in contests:
        rank = contest.get("rank")
        new_rating = contest.get("newRating")
        old_rating = contest.get("oldRating")
        if rank:
            ranking.append(rank)
        if old_rating is not None and new_rating is not None:
            delta = new_rating - old_rating
            rating.append(delta)

    # Guard: if not enough contests for trend
    if not ranking:
        return {
            "handle": handle,
            "message": "Not enough contest data."
        }

    best_rank = min(ranking)
    worst_rank = max(ranking)
    avg_rank = sum(ranking) // total_contests
    rating_change = abs(ranking[0] - ranking[total_contests - 1])

    # Default trend values
    early_avg = 0
    recent_avg = 0
    rating_trend = "Not enough data"

    if len(rating) >= 6:
        mid = total_contests // 2
        early_rating = rating[0:mid]
        recent_rating = rating[mid:]
        early_avg = sum(early_rating) / len(early_rating) if early_rating else 0
        recent_avg = sum(recent_rating) / len(recent_rating) if recent_rating else 0

        if recent_avg > early_avg:
            rating_trend = "Improving 📈"
        elif recent_avg == early_avg:
            rating_trend = "Equal"
        else:
            rating_trend = "Declining 📉"

    return {
        "handle": handle,
        "Best Rank": best_rank,
        "Worst Rank": worst_rank,
        "Avg Rank": avg_rank,
        "Rating change": rating_change,
        "Rating Trend": rating_trend
    }
