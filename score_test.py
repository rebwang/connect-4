"""
This score_test.py tests all the methods in Score class
"""
from score import Score


def test_score_constructor():
    score_file = "score_test.txt"
    score = Score(score_file)
    assert score.score_file == score_file
    assert score.scores == {}


def test_read_score_file():
    """Test read file and save data into a dictionary"""
    score_file = "score_test.txt"
    score = Score(score_file)
    score.read_score_file()
    assert score.scores == {
        'iago': 7,
        'emilia': 7,
        'desdemona': 2,
        'cassio': 1
    }


def test_record_score():
    """Test record_score: write data into file"""
    score_file = "score_test.txt"
    score = Score(score_file)
    score.read_score_file()

    # test space between name
    name = "EMI LIA"
    score.record_score(name)
    assert score.scores == {
        'emilia': 7,
        'iago': 7,
        'desdemona': 2,
        'cassio': 1,
        'emi lia': 1
    }

    # test sorting by score
    name = "Emilia"
    score.record_score(name)
    assert score.scores == {
        'emilia': 8,
        'iago': 7,
        'desdemona': 2,
        'cassio': 1,
        'emi lia': 1
    }
    reset_score_test_file()


def reset_score_test_file():
    """Reset score_test file back to original status"""
    score_file = "score_test.txt"
    score = Score(score_file)
    score.scores = {
        'iago': 7,
        'emilia': 7,
        'desdemona': 2,
        'cassio': 1
    }

    f = open(score_file, 'w')
    for key, value in score.scores.items():
        name = key.capitalize()
        score = str(value)
        f.write(f"{name} {score}\n")

    f.close()
