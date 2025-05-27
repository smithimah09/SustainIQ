from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app import mongo
from datetime import datetime, timedelta
from bson.objectid import ObjectId

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
@dashboard.route('/home')
@login_required
def home():
    # Get recent actions
    recent_actions = list(mongo.db.eco_actions.find(
        {'user_id': current_user.get_id()}
    ).sort('timestamp', -1).limit(5))

    # Get active goals
    active_goals = list(mongo.db.sustainability_goals.find({
        'user_id': current_user.get_id(),
        'status': 'in progress'
    }))

    # Get saved AI suggestions
    saved_suggestions = list(mongo.db.ai_suggestions.find({
        'user_id': current_user.get_id(),
        'saved': True
    }).sort('timestamp', -1).limit(5))

    # Calculate statistics
    total_actions = mongo.db.eco_actions.count_documents({'user_id': current_user.get_id()})
    completed_goals = mongo.db.sustainability_goals.count_documents({
        'user_id': current_user.get_id(),
        'status': 'completed'
    })

    # Get actions by category for chart
    categories = ['energy', 'waste', 'transport', 'food', 'water', 'other']
    category_counts = {}
    for category in categories:
        count = mongo.db.eco_actions.count_documents({
            'user_id': current_user.get_id(),
            'category': category
        })
        category_counts[category] = count

    # Get recent progress (past 7 days)
    today = datetime.utcnow().date()
    daily_actions = []

    for i in range(6, -1, -1):  # 7 days, from oldest to newest
        day = today - timedelta(days=i)
        start = datetime.combine(day, datetime.min.time())
        end = datetime.combine(day + timedelta(days=1), datetime.min.time())
        
        count = mongo.db.eco_actions.count_documents({
            'user_id': current_user.get_id(),
            'timestamp': {'$gte': start, '$lt': end}
        })

        daily_actions.append({
            'date': day.strftime('%b %d'),  # e.g., May 08
            'count': count
        })

    return render_template('dashboard/home.html',
                           title='Dashboard',
                           recent_actions=recent_actions,
                           active_goals=active_goals,
                           saved_suggestions=saved_suggestions,
                           total_actions=total_actions,
                           completed_goals=completed_goals,
                           category_counts=category_counts,
                           daily_actions=daily_actions)
