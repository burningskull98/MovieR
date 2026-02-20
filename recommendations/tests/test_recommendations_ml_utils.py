from unittest.mock import MagicMock
import pytest
from recommendations.ml_utils import ContentBasedRecommender, random_recommendations


@pytest.fixture
def recommender():
    """Fixture for initializing ContentBasedRecommender."""
    return ContentBasedRecommender()



def test_load_model(mocker, recommender):
    mocker.patch('os.path.exists', return_value=True)
    mock_load = mocker.patch('joblib.load')
    mock_load.return_value = {
        'vectorizer': MagicMock(),
        'vectors': MagicMock(),
        'ids': [1, 2, 3]
    }

    assert recommender._load_model() is True
    assert recommender.vectorizer is not None
    assert recommender.content_vectors is not None
    assert recommender.content_ids == [1, 2, 3]

def test_save_model(mocker, recommender):
    mock_dump = mocker.patch('joblib.dump')

    recommender.content_vectors = MagicMock()
    recommender.content_ids = [1, 2, 3]

    recommender._save_model()

    assert mock_dump.called is True
    assert mock_dump.call_args[0][0]['ids'] == [1, 2, 3]


def test_fit_model(mocker, recommender):
    mock_genre1 = MagicMock(name='Genre', spec=str)
    mock_genre1.name = 'Drama'
    mock_genre2 = MagicMock(name='Genre', spec=str)
    mock_genre2.name = 'Action'

    mock_actor = MagicMock(name='Actor', spec=str)
    mock_actor.name = 'John Doe'

    mock_director = MagicMock(name='Director', spec=str)
    mock_director.name = 'Jane Doe'

    mock_content = [
        MagicMock(tmdb_id=i,
                  genres=MagicMock(all=lambda: [mock_genre1, mock_genre2]),
                  actors=MagicMock(all=lambda: [mock_actor]),
                  director=MagicMock(all=lambda: [mock_director]))
        for i in range(5)
    ]

    mock_load = mocker.patch('Movie_app.models.Content.objects.all', return_value=mock_content)
    mock_save = mocker.patch.object(recommender, '_save_model')

    recommender.fit()

    assert recommender.content_vectors is not None
    mock_save.assert_called_once()


def test_random_recommendations(mocker):
    mock_content = [MagicMock(tmdb_id=i) for i in range(1, 11)]
    mocker.patch('Movie_app.models.Content.objects.all', return_value=mock_content)

    recommendations = random_recommendations(top_n=5)

    assert len(recommendations) == 5
