import pytest

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


@pytest.mark.parametrize(
    ("title", "description"),
    [
        (
            "Junior Python Backend Developer - Customer Support",
            "Build Python services and REST APIs.",
        ),
        (
            "Senior Python Backend Developer",
            "Build backend services and REST APIs with Python.",
        ),
        (
            "Junior Backend Developer",
            "Build backend services and REST APIs.",
        ),
        (
            "Junior Python Developer",
            "Build desktop applications using Python.",
        ),
        ("Junior Python Accountant", "Python and REST API experience."),
    ],
)
def test_filter_rejects_jobs_that_do_not_match_all_criteria(title, description):
    jobs = [{"title": title, "description": description}]

    result = filter_jobs(jobs)

    assert result == []


def test_filter_handles_missing_title_and_description():
    assert filter_jobs([{}]) == []
