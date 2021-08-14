class ApiError(Exception):
    def __init__(self, status_code, error, description):
        self.status_code = status_code
        self.error = error
        self.description = description
    
    def to_dict(self):
        return {
            "status_code": self.status_code,
            "error": self.error,
            "description": self.description
        }

class CheckResult(Exception):
    def __init__(self, status_code, success, gh_user, message):
        self.status_code = status_code
        self.success = success
        self.gh_user = gh_user
        self.message = message
    
    def to_dict(self):
        return {
            "status_code": self.status_code,
            "success": self.success,
            "github_user": self.gh_user,
            "message": self.message
        }

not_enough_permissions = ApiError(
    403,
    "not_enough_permissions", 
    "The code passed doesn't grant enough permissions, 'user:email' scope is required"
    )

code_not_provided = ApiError(
    400,
    "code_not_provided",
    "No code was passed in the query string"
)

esi_email_not_found = CheckResult(
    401,
    False,
    "",
    "ESI email not found, to join ESIHub org you must add your @esi.dz email \
to your Github account"
)

esi_email_not_verified = CheckResult(
    401,
    False,
    "",
    "ESI email not verified, to join ESIHub org you must verify your @esi.dz email \
in your Github account"
)
