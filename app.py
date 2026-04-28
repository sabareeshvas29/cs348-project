from flask import Flask, render_template, request, redirect
from models import db, Team, Player, Game, PlayerGameStats
from datetime import date


app =  Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///basketball.db'
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/stats', methods=['GET', 'POST'])
def stats():
    if request.method == 'POST':

        numeric_fields = ['points', 'rebounds', 'assists', 'steals', 'blocks', 'fouls', 'mins_played']
        for field in numeric_fields:
            if not request.form[field].isdigit():
                return f"Invalid input for {field}", 400

        player_id = request.form['player_id']
        game_id = request.form['game_id']
        points = request.form['points']
        rebounds = request.form['rebounds']
        assists = request.form['assists']
        steals = request.form['steals']
        blocks = request.form['blocks']
        fouls = request.form['fouls']
        mins_played = request.form['mins_played']

        new_stat = PlayerGameStats(player_id = player_id, game_id = game_id, points = points, rebounds = rebounds, 
                                   assists = assists, steals = steals, blocks = blocks, fouls = fouls, 
                                   mins_played = mins_played )
        
        db.session.add(new_stat)
        db.session.execute(db.text('PRAGMA read_uncommitted = OFF'))
        db.session.commit()
        return redirect('/stats')

    games = Game.query.all()
    players = Player.query.all()
    stats = PlayerGameStats.query.all()
        
    return render_template('stats.html', players=players, games=games, stats=stats)



@app.route("/report", methods= ['GET', 'POST'])
def report():
    results = []
    if request.method == 'POST':

        player_id = request.form['player_id']
        min_points = request.form['min_points']

        query = PlayerGameStats.query
        if player_id:
            query = query.filter(PlayerGameStats.player_id == player_id)

        if min_points:
            query = query.filter(PlayerGameStats.points >= min_points)

        results = query.all()

    games = Game.query.all()
    players = Player.query.all()
    stats = PlayerGameStats.query.all()

    return render_template('report.html', players=players, games=games, results=results)














@app.route('/delete/<int:stat_id>')
def delete_stat(stat_id):
    stat = PlayerGameStats.query.get(stat_id)

    db.session.delete(stat)
    db.session.commit()
    return redirect('/stats')


@app.route('/edit/<int:stat_id>', methods=['GET', 'POST'])
def edit_stat(stat_id):
    stat = PlayerGameStats.query.get(stat_id)

    if request.method == 'POST':
        numeric_fields = ['points', 'rebounds', 'assists', 'steals', 'blocks', 'fouls', 'mins_played']
        for field in numeric_fields:
            if not request.form[field].isdigit():
                return f"Invalid input for {field}", 400
        stat.player_id = request.form['player_id']
        stat.game_id = request.form['game_id']
        stat.points = request.form['points']
        stat.rebounds = request.form['rebounds']
        stat.assists = request.form['assists']
        stat.steals = request.form['steals']
        stat.blocks = request.form['blocks']
        stat.fouls = request.form['fouls']
        stat.mins_played = request.form['mins_played']

        db.session.execute(db.text('PRAGMA read_uncommitted = OFF'))
        db.session.commit()
        return redirect('/stats')

    players = Player.query.all()
    games = Game.query.all()
    return render_template('edit.html', stat=stat, players=players, games=games)


@app.route('/seed')
def seed():
    # Clear existing data
    PlayerGameStats.query.delete()
    Game.query.delete()
    Player.query.delete()
    Team.query.delete()
    db.session.commit()

    # Teams
    warriors = Team(team_name='Warriors', city='Golden State')
    celtics = Team(team_name='Celtics', city='Boston')
    lakers = Team(team_name='Lakers', city='Los Angeles')
    db.session.add_all([warriors, celtics, lakers])
    db.session.commit()

    # Players
    curry = Player(player_name='Stephen Curry', team_id=warriors.team_id, jersey_num=30, position='Guard')
    klay = Player(player_name='Klay Thompson', team_id=warriors.team_id, jersey_num=11, position='Guard')
    tatum = Player(player_name='Jayson Tatum', team_id=celtics.team_id, jersey_num=0, position='Forward')
    lebron = Player(player_name='LeBron James', team_id=lakers.team_id, jersey_num=23, position='Forward')
    db.session.add_all([curry, klay, tatum, lebron])
    db.session.commit()

    # Games
    game1 = Game(game_date=date(2022, 6, 10), location='TD Garden', home_team_id=celtics.team_id, away_team_id=warriors.team_id)
    game2 = Game(game_date=date(2022, 6, 13), location='Chase Center', home_team_id=warriors.team_id, away_team_id=celtics.team_id)
    game3 = Game(game_date=date(2023, 1, 28), location='Crypto.com Arena', home_team_id=lakers.team_id, away_team_id=warriors.team_id)
    db.session.add_all([game1, game2, game3])
    db.session.commit()

    # Stats
    db.session.add_all([
        PlayerGameStats(player_id=curry.player_id, game_id=game1.game_id, points=43, rebounds=10, assists=4, steals=0, blocks=0, fouls=3, mins_played=41),
        PlayerGameStats(player_id=klay.player_id, game_id=game1.game_id, points=18, rebounds=3, assists=2, steals=1, blocks=0, fouls=2, mins_played=36),
        PlayerGameStats(player_id=tatum.player_id, game_id=game1.game_id, points=23, rebounds=6, assists=3, steals=1, blocks=1, fouls=4, mins_played=38),
        PlayerGameStats(player_id=curry.player_id, game_id=game2.game_id, points=34, rebounds=7, assists=7, steals=2, blocks=0, fouls=2, mins_played=40),
        PlayerGameStats(player_id=klay.player_id, game_id=game2.game_id, points=25, rebounds=4, assists=1, steals=0, blocks=1, fouls=3, mins_played=37),
        PlayerGameStats(player_id=lebron.player_id, game_id=game3.game_id, points=38, rebounds=8, assists=9, steals=1, blocks=1, fouls=2, mins_played=39),
        PlayerGameStats(player_id=curry.player_id, game_id=game3.game_id, points=27, rebounds=5, assists=6, steals=3, blocks=0, fouls=1, mins_played=38),
    ])
    db.session.commit()

    return 'Seeded with fresh data!'


if __name__ == "__main__":
    app.run(debug=True)
    

