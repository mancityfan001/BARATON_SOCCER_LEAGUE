from django.shortcuts import render
from players.models import Player
from teams.models import Team


def awards_page(request):

    # =========================
    # MEN'S AWARDS
    # =========================

    men_golden_boot = (
        Player.objects.filter(team_category="Men")
        .order_by("-goals")
        .first()
    )

    men_top_playmaker = (
        Player.objects.filter(team_category="Men")
        .order_by("-assists")
        .first()
    )

    men_golden_glove = (
        Player.objects.filter(
            team_category="Men",
            position="Goalkeeper"
        )
        .order_by("-clean_sheets", "goal_conceded")
        .first()
    )

    men_champion = (
        Team.objects.filter(category="Men")
        .order_by(
            "-points",
            "-goal_difference",
            "-goals_scored"
        )
        .first()
    )


    # =========================
    # LADIES' AWARDS
    # =========================

    ladies_golden_boot = (
        Player.objects.filter(team_category="Ladies")
        .order_by("-goals")
        .first()
    )

    ladies_top_playmaker = (
        Player.objects.filter(team_category="Ladies")
        .order_by("-assists")
        .first()
    )

    ladies_golden_glove = (
        Player.objects.filter(
            team_category="Ladies",
            position="Goalkeeper"
        )
        .order_by("-clean_sheets", "goal_conceded")
        .first()
    )

    ladies_champion = (
        Team.objects.filter(category="Ladies")
        .order_by(
            "-points",
            "-goal_difference",
            "-goals_scored"
        )
        .first()
    )


    context = {

        "men_golden_boot": men_golden_boot,
        "men_top_playmaker": men_top_playmaker,
        "men_golden_glove": men_golden_glove,
        "men_champion": men_champion,

        "ladies_golden_boot": ladies_golden_boot,
        "ladies_top_playmaker": ladies_top_playmaker,
        "ladies_golden_glove": ladies_golden_glove,
        "ladies_champion": ladies_champion,

    }

    return render(request, "awards/awards.html", context)