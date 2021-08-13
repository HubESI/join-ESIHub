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
