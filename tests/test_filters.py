
from app.filters import filter_jobs


def test_filter_accepts_junior_python_backend_job():
    jobs = [
        {
            "title": "Junior Python Backend Developer",
            "description": "Experience with Python, FastAPI and REST API.",
        }
    ]

    result = filter_jobs(jobs)

    assert len(result) == 1
    assert result[0]["title"] == "Junior Python Backend Developer"


def test_filter_rejects_customer_support_job():
    jobs = [
        {
            "title": "Junior Technical Support Specialist",
            "description": "Python and API knowledge is useful.",
        }
    ]

    result = filter_jobs(jobs)

    assert result == []
