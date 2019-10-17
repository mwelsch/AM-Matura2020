OVERLEAF_BASE_URL = "https://www.overleaf.com"
OVERLEAF_LOGIN = OVERLEAF_BASE_URL + "/login"
OVERLEAF_CSRF_REGEX = "window\.csrfToken = \"(.+)\""


def get_download_url(project_id):
    return OVERLEAF_BASE_URL + ("/project/%s/download/zip" % str(project_id))
