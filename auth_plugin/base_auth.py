class BaseAuth:
    def authenticate(self, *args, **kwargs):
        raise NotImplementedError("Subclasses should implement this!")

    def generate_token(self, *args, **kwargs):
        raise NotImplementedError("Subclasses should implement this!")

    def validate_token(self, *args, **kwargs):
        raise NotImplementedError("Subclasses should implement this!")
