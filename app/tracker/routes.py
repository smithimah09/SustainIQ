from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.tracker.forms import EcoActionForm, GoalForm
from app import mongo
from datetime import datetime, time
from bson.objectid import ObjectId

tracker = Blueprint('tracker', __name__)

@tracker.route('/log-action', methods=['GET', 'POST'])
@login_required
def log_action():
    form = EcoActionForm()
    if form.validate_on_submit():
        action_data = {
            'user_id': current_user.get_id(),
            'action_text': form.action_text.data,
            'category': form.category.data,
            'timestamp': datetime.utcnow()
        }
        mongo.db.eco_actions.insert_one(action_data)
        flash('Action logged successfully!', 'success')
        return redirect(url_for('dashboard.home'))
    
    return render_template('tracker/log_action.html', 
                          title='Log Eco-Action',
                          form=form)

@tracker.route('/set-goal', methods=['GET', 'POST'])
@login_required
def set_goal():
    form = GoalForm()

    if form.validate_on_submit():
        # Convert date to datetime.datetime
        target_date = form.target_date.data
        if target_date:
            target_date = datetime.combine(target_date, time.min)

        goal_data = {
            'user_id': current_user.get_id(),
            'title': form.title.data,
            'description': form.description.data,
            'status': 'in progress',
            'created_at': datetime.utcnow(),
            'target_date': target_date  # safe for MongoDB now
        }

        mongo.db.sustainability_goals.insert_one(goal_data)
        flash('Goal set successfully!', 'success')
        return redirect(url_for('dashboard.home'))

    return render_template('tracker/set_goal.html',
                           title='Set Sustainability Goal',
                           form=form)
@tracker.route('/update-goal/<goal_id>/<status>')
@login_required
def update_goal_status(goal_id, status):
    if status not in ['in progress', 'completed', 'abandoned']:
        flash('Invalid status!', 'danger')
        return redirect(url_for('dashboard.home'))
    
    mongo.db.sustainability_goals.update_one(
        {'_id': ObjectId(goal_id), 'user_id': current_user.get_id()},
        {'$set': {'status': status}}
    )
    flash('Goal status updated!', 'success')
    return redirect(url_for('dashboard.home'))

@tracker.route('/actions-history')
@login_required
def actions_history():
    actions = mongo.db.eco_actions.find(
        {'user_id': current_user.get_id()}
    ).sort('timestamp', -1)
    
    return render_template('tracker/actions_history.html', 
                          title='Eco-Actions History',
                          actions=list(actions))

@tracker.route('/goals')
@login_required
def goals():
    goals = mongo.db.sustainability_goals.find(
        {'user_id': current_user.get_id()}
    ).sort('created_at', -1)
    
    return render_template('tracker/goals.html', 
                          title='Sustainability Goals',
                          goals=list(goals))