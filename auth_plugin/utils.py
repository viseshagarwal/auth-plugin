def extract_token_from_header(auth_header):
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header.split(" ")[1]
    return None
