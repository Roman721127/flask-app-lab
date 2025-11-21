import unittest
from app import app, db
from app.models import Post

class PostsBlueprintTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://' 
        
        self.app = app
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        db.create_all()
        
        p1 = Post(
            title='Тестовий Пост 1', 
            content='Тестовий Контент 1', 
            author='Перший Автор'
        )
        db.session.add(p1)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def test_1_posts_list_page(self):
        """Тест: Чи завантажується сторінка зі списком постів."""
        response = self.client.get('/post/')
        self.assertEqual(response.status_code, 200)
        
        self.assertIn('Тестовий Пост 1'.encode('utf-8'), response.data)
        self.assertIn(b'postdefault.png', response.data)
        self.assertIn('Перший Автор'.encode('utf-8'), response.data)

    def test_2_post_detail_page(self):
        """Тест: Чи завантажується сторінка одного поста."""
        response = self.client.get('/post/1')
        self.assertEqual(response.status_code, 200)
        
        self.assertIn('Тестовий Пост 1'.encode('utf-8'), response.data)
        self.assertIn('Тестовий Контент 1'.encode('utf-8'), response.data)
        self.assertIn('Перший Автор'.encode('utf-8'), response.data)

    def test_3_create_post(self):
        """Тест: Створення нового поста (CREATE)."""
        response_get = self.client.get('/post/create')
        self.assertEqual(response_get.status_code, 200)

        response_post = self.client.post('/post/create', data={
            'title': 'Новий Тестовий Пост',
            'content': 'Це пост, створений тестом.',
            'author': 'Тестовий Автор' 
        }, follow_redirects=True) 

        self.assertEqual(response_post.status_code, 200)
        
        self.assertIn('Новий Тестовий Пост'.encode('utf-8'), response_post.data)
        self.assertIn('Тестовий Автор'.encode('utf-8'), response_post.data)
        
        post = db.session.get(Post, 2)
        self.assertIsNotNone(post)
        self.assertEqual(post.author, 'Тестовий Автор')

    def test_4_update_post(self):
        """Тест: Оновлення існуючого поста (UPDATE)."""
        response_get = self.client.get('/post/1/update')
        self.assertEqual(response_get.status_code, 200)

        response_post = self.client.post('/post/1/update', data={
            'title': 'Оновлений Заголовок',
            'content': 'Оновлений контент.',
            'author': 'Оновлений Автор'
        }, follow_redirects=True)

        self.assertEqual(response_post.status_code, 200)
        
        self.assertIn('Оновлений Заголовок'.encode('utf-8'), response_post.data)
        self.assertIn('Оновлений Автор'.encode('utf-8'), response_post.data)

        post = db.session.get(Post, 1)
        self.assertEqual(post.title, 'Оновлений Заголовок')
        self.assertEqual(post.author, 'Оновлений Автор')

    def test_5_delete_post(self):
        """Тест: Видалення поста (DELETE)."""
        response_get = self.client.get('/post/1/delete_confirm')
        self.assertEqual(response_get.status_code, 200)
        
        self.assertIn('Ви впевнені, що хочете видалити'.encode('utf-8'), response_get.data)

        response_post = self.client.post('/post/1/delete', follow_redirects=True)
        self.assertEqual(response_post.status_code, 200)
        
        self.assertNotIn('Тестовий Пост 1'.encode('utf-8'), response_post.data)
        
        post = db.session.get(Post, 1)
        self.assertIsNone(post)

if __name__ == '__main__':
    unittest.main()