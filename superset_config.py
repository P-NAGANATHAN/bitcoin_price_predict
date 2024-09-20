ENABLE_CORS = True

# Remove or modify the 'X-Frame-Options' header to allow embedding
HTTP_HEADERS = {
    'X-Frame-Options': 'ALLOWALL',  # This allows embedding from any domain
}
