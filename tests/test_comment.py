from app.models import Comment,Blogs
import unittest
from app import db

class TestComment(unittest.TestCase):
    def setUp(self):
        self.new_blog=Blogs(blog='i love life')
        self.new_comment=Comment(comment='live life',blogs=self.new_blog)

    def tearDown(self):
        self.new_comment.query.delete()
        self.new_blog.query.delete()

        

    def test_comment_saved(self):
        self.new_comment.save_comment()
        self.assertTrue(len(Comment.query.all())>0)

    def test_get_comments(self):
        self.new_comment.save_comment()
        get=Comment.get_comment(self.new_blog.id)
        self.assertTrue(len(get)==1)
