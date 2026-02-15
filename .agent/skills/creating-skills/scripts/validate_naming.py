import sys
import re

def validate(name):
    if not re.match(r'^[a-z0-9-]+$', name):
        return False, "Name must be lowercase, numbers, and hyphens only."
    if len(name) > 64:
        return False, "Name must be under 64 characters."
    if not name.endswith('ing'):
        return False, "Name should ideally be in gerund form (ending in -ing)."
    return True, "Valid"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_naming.py <name>")
        sys.exit(1)
    
    success, msg = validate(sys.argv[1])
    print(msg)
    sys.exit(0 if success else 1)
