from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.models import CrewCall, Performance, Production, db

bp = Blueprint("productions", __name__)


@bp.route("/productions")
def list_productions():
    productions = Production.query.order_by(Production.id.desc()).all()
    return render_template("productions/list.html", productions=productions)


@bp.route("/productions/new", methods=["GET", "POST"])
def create_production():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        if not title:
            flash("Title is required.", "error")
            return render_template("productions/form.html"), 400
        production = Production(title=title)
        db.session.add(production)
        db.session.commit()
        return redirect(url_for("productions.list_productions"))
    return render_template("productions/form.html")


@bp.route("/productions/<int:production_id>")
def production_detail(production_id):
    production = db.get_or_404(Production, production_id)
    return render_template("productions/detail.html", production=production)


@bp.route("/productions/<int:production_id>/performances/new", methods=["GET", "POST"])
def create_performance(production_id):
    production = db.get_or_404(Production, production_id)
    if request.method == "POST":
        try:
            date = datetime.strptime(request.form["date"], "%Y-%m-%d").date()
            start_time = datetime.strptime(request.form["start_time"], "%H:%M").time()
        except (KeyError, ValueError):
            flash("Date and start time are required (YYYY-MM-DD, HH:MM).", "error")
            return render_template("productions/performance_form.html", production=production), 400
        performance = Performance(production=production, date=date, start_time=start_time)
        roles = request.form.getlist("role")
        counts = request.form.getlist("count")
        for role, count in zip(roles, counts):
            if role.strip():
                performance.crew_calls.append(
                    CrewCall(role=role.strip(), count=int(count or 1))
                )
        db.session.add(performance)
        db.session.commit()
        return redirect(url_for("productions.production_detail", production_id=production.id))
    return render_template("productions/performance_form.html", production=production)
