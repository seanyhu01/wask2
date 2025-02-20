from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user, logout_user
from ..forms import SearchForm, WeatherReviewForm
from .. import city_client, weather_client
from ..models import Review
from datetime import datetime, timedelta

weather = Blueprint("weather", __name__)


@weather.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for("weather.results", query=form.search_query.data))

    return render_template("index.html", form=form)


# /results/<query>
# Returns a list of locations that matches the user's search query.
@weather.route("/results/<query>", methods=["GET"])
def results(query):
    try:
        locations = city_client.search_cities(query)
    except ValueError as e:
        return render_template("results.html", error=e)

    return render_template("results.html", locations=locations)


# /forecast/<location>
# Returns details of the forecast of the chosen location
@weather.route("/forecast/<location>", methods=["GET", "POST"])
def forecast(location):
    try:
        forecast = weather_client.get_forecast(location)
    except ValueError as e:
        return render_template("forecast.html", error=e)

    form = WeatherReviewForm()
    if form.validate_on_submit():
        review = Review(
            commenter=current_user._get_current_object(),
            content=form.text.data,
            location=f'{forecast["location"]["name"]},{forecast["location"]["region"]},{forecast["location"]["country"]}',
        )

        review.save()

        return redirect(request.path)

    reviews = Review.objects(
        location=f'{forecast["location"]["name"]},{forecast["location"]["region"]},{forecast["location"]["country"]}'
    )

    # location_query is the original query to get the forecast, so we can reuse for history
    return render_template(
        "forecast.html",
        forecast=forecast,
        location_query=location,
        form=form,
        reviews=reviews,
    )


# /history/<location>/<date>
# Returns details of the forecast history of the chosen location
@weather.route("/history/<location>", methods=["GET"])
def history(location):
    # start_date and end_date are date strings of the format YYYY/MM/DD
    # we use this to get the starting date of the weather history
    start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    # we use this to get the ending date of the weather history
    end_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    try:
        history = weather_client.get_history(location, start_date, end_date)
    except ValueError as e:
        return render_template("history.html", error=e)

    # location_query is the original query to get the forecast, so we can reuse for forecast
    return render_template("history.html", history=history, location_query=location)
