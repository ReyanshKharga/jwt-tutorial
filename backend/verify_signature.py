import base64
import hmac
import hashlib

SECRET_KEY = "myjwtsecret" # DEMO ONLY! Use a strong 256/512-bit secret key in production.

def verify_jwt(token: str) -> bool:
    try:
        # Split the token into header, payload, and signature
        header_enc, payload_enc, signature_enc = token.split(".")
        
        # Recompute the signature
        message = f"{header_enc}.{payload_enc}".encode() # This converts the string representation of header_enc.payload_enc into bytes before passing it to the HMAC-SHA256 hashing function.
        expected_signature = hmac.new(SECRET_KEY.encode(), message, hashlib.sha256).digest()
        expected_signature_enc = base64.urlsafe_b64encode(expected_signature).rstrip(b"=").decode()

        # Compare computed signature with the provided one
        return hmac.compare_digest(expected_signature_enc, signature_enc)
    
    except Exception as e:
        print("Error:", e)
        return False

# Example JWT Token
jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc0MjkyNzQ3NX0.sYMSMto3Grk2e_U0TUS1S5afEY_BXRNfgLQxesYDufM"

# Verify token
is_valid = verify_jwt(jwt_token)
print("Is JWT valid?", is_valid)
