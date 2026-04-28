from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Team(db.Model):
        __tablename__ = 'teams'
        team_id = db.Column(db.Integer, primary_key=True)
        team_name = db.Column(db.String(100), nullable=False)
        city = db.Column(db.String(100))

class Player(db.Model):
        __tablename__ = 'players'
        player_id = db.Column(db.Integer, primary_key=True)
        player_name = db.Column(db.String(100), nullable=False)
        team_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'))
        jersey_num = db.Column(db.Integer, nullable=False)
        position = db.Column(db.String(100), nullable=False)

class Game(db.Model):
         __tablename__ = 'games'
         game_id = db.Column(db.Integer, primary_key=True)
         game_date = db.Column(db.Date,  nullable=False)
         location = db.Column(db.String(100), nullable=False)
         home_team_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'))
         away_team_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'))

class PlayerGameStats(db.Model):
        __tablename__ = 'player_game_stats'
        stat_id = db.Column(db.Integer, primary_key=True)
        player_id = db.Column(db.Integer, db.ForeignKey('players.player_id'))
        game_id = db.Column(db.Integer, db.ForeignKey('games.game_id'))
        points = db.Column(db.Integer, nullable=False)
        rebounds = db.Column(db.Integer, nullable=False)
        assists = db.Column(db.Integer, nullable=False)
        steals = db.Column(db.Integer, nullable=False)
        blocks = db.Column(db.Integer, nullable=False)
        fouls = db.Column(db.Integer, nullable=False)
        mins_played = db.Column(db.Integer, nullable=False)
        player = db.relationship('Player', foreign_keys=[player_id])
        game = db.relationship('Game', foreign_keys=[game_id])





