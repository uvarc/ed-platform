import unittest
from flask import json
from ed_platform import app, db, data_loader, models


class TestCase(unittest.TestCase):

    def setUp(self):
        app.config.from_pyfile('../config/testing.py')

        self.app = app.test_client()
        db.create_all()
        self.ctx = app.test_request_context()
        self.ctx.push()
        loader = data_loader.DataLoader(db)
        loader.load("example_data.json")

        # Disable sending emails during unit testing
        # mail.init_app(app)
        # self.assertEqual(app.debug, False)

    def tearDown(self):
        self.ctx.pop()
        db.drop_all()
        pass

    def test_base(self):
        rv = self.app.get('/api')
        print(rv.data)
        assert b'ED Platform API' in rv.data

    def add_test_track(self):
        data = {'image_file': 'track_one.jpg',
                'title': 'This is the title',
                'description': 'This is the description'}
        rv = self.app.post('/api/track', data=json.dumps(data), follow_redirects=True,
                           content_type="application/json")
        self.assertSuccess(rv)
        rd = json.loads(rv.get_data(as_text=True))
        return rd

    def add_test_workshop(self):
        data = {'image_file': 'workshop_one.jpg',
                'title': 'This is a test workshop',
                'description': 'This is the test description',
                }
        rv = self.app.post('/api/workshop', data=json.dumps(data), follow_redirects=True,
                           content_type="application/json")
        self.assertSuccess(rv)
        return json.loads(rv.get_data(as_text=True))

    def add_test_session(self, workshop_id):
        data = {
            "workshop": workshop_id,
            "date_time": "2017-11-11T18:30:00.000Z",
            "duration_minutes": "60",
            "instructor_notes": "This is a note from the instructor"
        }
        rv = self.app.post('/api/session', data=json.dumps(data), follow_redirects=True,
                           content_type="application/json")
        self.assertSuccess(rv)
        return json.loads(rv.get_data(as_text=True))

    def assertSuccess(self, rv):
        self.assertTrue(rv.status_code >= 200 and rv.status_code < 300,
                        "BAD Response:" + rv.status + ".")

    def get_workshop(self, id):
        rv = self.app.get('/api/workshop/%i' %id,
                           follow_redirects=True,
                           content_type="application/json")
        return json.loads(rv.get_data(as_text=True))


    def test_add_track(self):
        rd = self.add_test_track()
        assert rd['title'] == "This is the title"
        assert rd['description'] == "This is the description"
        assert rd["id"] is not None

        rv2 = self.app.get('/api/track/' + str(rd["id"]))
        assert b'This is the title' in rv2.data
        assert b'This is the description' in rv2.data

    def test_get_tracks(self):
        response = self.app.get('/api/track')
        all_tracks = json.loads(response.get_data(as_text=True))
        assert len(all_tracks["tracks"]) > 1
        track1 = all_tracks["tracks"][0]
        self.assertTrue("title" in track1.keys())
        self.assertTrue("description" in track1.keys())
        self.assertTrue(len(track1["_links"]["workshops"]) > 0)

    def test_sample_data_load(self):
        track = models.Track.query.filter_by(id=1).first()
        assert track.title == "Learning Python The Hard Way"

    def test_add_workshop(self):
        workshop = self.add_test_workshop()
        self.assertEqual("This is a test workshop", workshop["title"])

    def test_set_workshops_for_track(self):
        track    = self.add_test_track()
        workshop = self.add_test_workshop()
        data = json.dumps({"workshops":[workshop]})
        url = '/api/track/%i/workshops' % track['id']

        response = self.app.patch(url,
                            follow_redirects=True,
                            data = data,
                            content_type="application/json")

        workshops = json.loads(response.get_data(as_text=True))
        self.assertTrue(len(workshops["workshops"]), 1)

    def test_add_session(self):
        workshop = self.add_test_workshop()
        session = self.add_test_session(workshop["id"])
        self.assertEqual("This is a note from the instructor", session["instructor_notes"])
        self.assertEqual(workshop["id"], session["workshop_id"])

    def test_get_sessions(self):
        url = '/api/session'
        print("The url is " + url)
        rv = self.app.get(url, follow_redirects=True)
        self.assertSuccess(rv)

    def test_get_session(self):
        workshop = self.add_test_workshop()
        session = self.add_test_session(workshop["id"])
        url = '/api/session/%i' %session["id"]
        print("The url is " + url)
        rv = self.app.get(url, follow_redirects=True)
        self.assertSuccess(rv)
        session = json.loads(rv.get_data(as_text=True))
        self.assertEqual("This is a note from the instructor", session["instructor_notes"])
        self.assertEqual(workshop["id"], session["workshop_id"])
        self.assertTrue("_links" in session, "Session Has Links.")

    def test_get_workshop_sessions(self):
        workshop = self.add_test_workshop()
        session1 = self.add_test_session(workshop["id"])
        session2 = self.add_test_session(workshop["id"])
        self.assertIsNotNone(workshop["_links"]["sessions"])
        rv = self.app.get(workshop["_links"]["sessions"], follow_redirects=True)
        self.assertSuccess(rv)
        session_list = json.loads(rv.get_data(as_text=True))
        self.assertEqual(2, len(session_list["sessions"]))

    def test_remove_session(self):
        workshop = self.add_test_workshop()
        session = self.add_test_session(workshop["id"])
        rv = self.app.delete(session["_links"]["self"], follow_redirects=True)
        self.assertSuccess(rv)
        rv = self.app.get(session["_links"]["self"], follow_redirects=True)
        self.assertEqual(404, rv.status_code)





if __name__ == '__main__':
    unittest.main()
