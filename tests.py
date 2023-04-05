from unittest import TestCase
from app import app
import json
from flask import session
from boggle import Boggle

app.config['TESTING'] = True

class FlaskTests(TestCase):   

    def test_boggle_form(self):
        """Test if table and form appears""" 
        with app.test_client() as client:
            res = client.get("/")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<p>Your words</p>', html)

    def test_valid_submission(self):
        """Test if submitted word is valid on the board""" 
        with app.test_client() as client:
            with client.session_transaction() as board:
                board["board"] = [['S', 'P', 'Y', 'S', 'P'],['S', 'P', 'Y', 'S', 'P'],['S', 'P', 'Y', 'S', 'P'],['S', 'P', 'Y', 'S', 'P'],['S', 'P', 'Y', 'S', 'P']]
            res = client.post('/submitted', data=json.dumps(dict(word='spy')),
                       content_type='application/json')
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.json['result'], "ok")

    def test_not_word(self):
        """Test if word submitted is not a word"""
        with app.test_client() as client:
            with client.session_transaction() as board:
                board["board"] = [['S', 'P', 'Y', 'S', 'P'],['S', 'P', 'Y', 'S', 'P'],['S', 'P', 'Y', 'S', 'P'],['S', 'P', 'Y', 'S', 'P'],['S', 'P', 'Y', 'S', 'P']]
            res = client.post('/submitted', data=json.dumps(dict(word='rezzz')),content_type='application/json')
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.json['result'], "not-word")

    
    def test_post_game_result(self):
        """Test if play count incremented and highest_score updated"""
        with app.test_client() as client:
            with client.session_transaction() as stats:
                stats["highest_score"] = 12
                stats["times_played"] = 4
        res = client.post('/end', data=json.dumps(dict(score= 20)), content_type='application/json')
        self.assertEqual(res.json["highest_score"], 20)
        self.assertEqual(res.json["times_played"], 5)




    