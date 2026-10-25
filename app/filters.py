def filter_jobs(jobs):
    results = []

    for job in jobs:
        title = job.get("title", "").lower()
        description = job.get("description", "").lower()
        text = f"{title} {description}"

        # Identify Python as a relevant technology
        python_keywords = [
            "python",
            "django",
            "fastapi",
            "flask",
        ]

        python_related = any(
            word in text for word in python_keywords
        )

        # Identify software development roles
        software_keywords = [
            "developer",
            "software engineer",
            "software developer",
            "backend",
            "back-end",
            "back end",
            "api developer",
            "programista",
            "inżynier oprogramowania",
        ]

        software_role = any(
            word in title for word in software_keywords
        )

        # Identify junior and entry-level positions
        junior_keywords = [
            "junior",
            "entry level",
            "entry-level",
            "graduate",
            "trainee",
            "intern",
            "internship",
            "associate",
            "młodszy",
            "staż",
            "stażysta",
        ]

        junior_level = any(
            word in title for word in junior_keywords
        )

        # Exclude unrelated job categories
        excluded_keywords = [
            "electronics",
            "robot autonomy",
            "sales",
            "account executive",
            "customer support",
            "technical support",
            "data scientist",
            "data analyst",
            "project manager",
            "product manager",
            "recruiter",
            "obsługa klienta",
            "kierownik projektu",
        ]

        excluded_role = any(
            word in title for word in excluded_keywords
        )

        # Require evidence of backend or API work
        backend_keywords = [
            "backend",
            "back-end",
            "back end",
            "api",
            "server-side",
            "server side",
            "rest",
            "restful",
            "web services",
            "programowanie serwerowe",
        ]

        backend_related = any(
            word in text for word in backend_keywords
        )

        if (
            python_related
            and software_role
            and junior_level
            and backend_related
            and not excluded_role
        ):
            results.append(job)

    return results
