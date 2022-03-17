from django.db import connection


def compare_two_players(player1_first_name, player1_last_name, player2_first_name, player2_last_name):
    with connection.cursor() as cursor:
        cursor.execute("""select p.picture_url , p.first_name, p.last_name, t."name", tp.goals, tp.assists, tp.yellow_cards, tp.red_cards 
                          from "SportWow_app_teamplayer" tp 
                          join "SportWow_app_player" p on p.id =tp.player_id 
                          join "SportWow_app_team" t on t.id = tp.team_id
                          where p.first_name = %s and p.last_name = %s
                          or p.first_name = %s and  p.last_name = %s
                          order by goals desc;""",
                       [player1_first_name, player1_last_name, player2_first_name, player2_last_name])
        rows = cursor.fetchall()
        res_list = [{"picture": row[0], "name": row[1]+' ' + row[2],
                     "team":row[3], 'goals':row[4], 'assists': row[5],
                     "yellow_cards": row[6], "red_cards": row[7]} for row in rows]
        return res_list


def compare_two_teams(team1_name, team2_name, league):
    with connection.cursor() as cursor:
        cursor.execute("""select t.picture_url , t."name" , t.points, t.goals_for , t.goals_against ,sum(t.goals_for - t.goals_against) as GoalsDiff 
                            from "SportWow_app_team" t  join "SportWow_app_league" l on t.league_id = %s
                            where t."name" =%s or t.name= %s
                            group by t.picture_url , t.name, t.points, t.goals_for , t.goals_against 
                            order by points desc, GoalsDiff desc, t.goals_for  desc ;""",
                       [league, team1_name, team2_name])
        rows = cursor.fetchall()
        res_list = [{"picture": row[0], "name": row[1],
                     "points":row[2], 'goals_for': row[3],
                     "goals_against": row[4], "goals_diff": row[5]} for row in rows]
        return res_list


def show_league_table(league):
    with connection.cursor() as cursor:
        cursor.execute("""select t.picture_url , t."name" , t.points, t.goals_for , t.goals_against ,sum(t.goals_for - t.goals_against) as GoalsDiff 
                            from "SportWow_app_team" t  join "SportWow_app_league" l on t.league_id = %s
                            group by t.picture_url , t.name, t.points, t.goals_for , t.goals_against 
                            order by points desc, GoalsDiff desc, t.goals_for  desc ;""",
                       [league])
        rows = cursor.fetchall()
        res_list = [{"picture": row[0], "name": row[1],
                     "points":row[2], 'goals_for': row[3],
                     "goals_against": row[4], "goals_diff": row[5]} for row in rows]
        return res_list


def show_league_assists(league):
    with connection.cursor() as cursor:
        cursor.execute("""select p.picture_url,p.first_name, p.last_name, team."name", t.assists
                            from "SportWow_app_teamplayer" t 
                            join "SportWow_app_player" p on p.id = t.player_id 
                            join "SportWow_app_team" team on team.id = t.team_id 
                            join "SportWow_app_league" l on team.league_id = %s
                            where t.assists > 0
                            order by t.assists desc ;""",
                       [league])
        rows = cursor.fetchall()
        res_list = [{"picture": row[0], "name": row[1] + " " + row[2],
                     "team":row[3], 'assists': row[4]} for row in rows]
        return res_list


def show_league_goals(league):
    with connection.cursor() as cursor:
        cursor.execute("""select p.picture_url,p.first_name, p.last_name, team."name", t.goals
                            from "SportWow_app_teamplayer" t 
                            join "SportWow_app_player" p on p.id = t.player_id 
                            join "SportWow_app_team" team on team.id = t.team_id 
                            join "SportWow_app_league" l on team.league_id = %s
                            where t.goals > 0
                            order by t.goals desc ;""",
                       [league])
        rows = cursor.fetchall()
        res_list = [{"picture": row[0], "name": row[1] + " " + row[2],
                     "team":row[3], 'goals': row[4]} for row in rows]
        return res_list


def show_crowd_avg(team_name):
    with connection.cursor() as cursor:
        cursor.execute("""select avg(match.attendance), team."name" from "SportWow_app_match" match
                            join "SportWow_app_team" team 
                            on (team.id = match.home_team_id or team.id = match.away_team_id)
                            and team.name = %s
                            group by team."name";""",
                       [team_name])
        rows = cursor.fetchall()
        res_list = [{"avg": row[0], "name": row[1]} for row in rows]
        return res_list


def show_players_for_team(team_name):
    with connection.cursor() as cursor:
        cursor.execute("""select p.first_name , p.last_name , tp.appearances , tp.goals ,
                                tp.assists, tp.yellow_cards, tp.red_cards, p.picture_url
                                from "SportWow_app_player" p
                                join "SportWow_app_teamplayer" tp on p.id = tp.player_id
                                join "SportWow_app_team" t on t.id = tp.team_id 
                                where tp.is_active = true and t."name" = %s;""",
                       [team_name])
        rows = cursor.fetchall()
        res_list = [{"name": row[0] + " " + row[1], "appearances": row[2], "goals": row[3], "assists": row[4]
                     , "yellow_cards": row[5], "red_cards":row[6], "picture": row[7]} for row in rows]
        return res_list


def show_players_for_league(league_id):
    with connection.cursor() as cursor:
        cursor.execute("""select p.first_name , p.last_name , tp.appearances , tp.goals ,
                                tp.assists, tp.yellow_cards, tp.red_cards, p.picture_url from "SportWow_app_player" p
                            join "SportWow_app_teamplayer" tp on tp.player_id = p.id 
                            join "SportWow_app_team" t on t.id =tp.team_id 
                            where tp.is_active =true and t.league_id = %s;""",
                       [league_id])
        rows = cursor.fetchall()
        res_list = [{"name": row[0] + " " + row[1], "appearances": row[2], "goals": row[3], "assists": row[4]
                        , "yellow_cards": row[5], "red_cards": row[6], "picture": row[7]} for row in rows]
        return res_list