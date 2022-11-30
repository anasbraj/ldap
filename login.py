import ldap
import sys

# https://www.forumsys.com/2022/05/10/online-ldap-test-server/
#
# LDAP Server Information (read-only access):
# Server: ldap.forumsys.com
# Port: 389
# Bind DN: cn=read-only-admin,dc=example,dc=com
# Bind Password: password

SERVER_HOST = "ldap.forumsys.com"
SERVER_PORT = 389
USER_DC = "dc=example,dc=com"

def login_user(username, password):
    try:
        conn = ldap.initialize(f"ldap://{SERVER_HOST}:{SERVER_PORT}")
        conn.protocol_version = ldap.VERSION3
        conn.simple_bind_s(f"uid={username},{USER_DC}", password)
        return True

    except Exception as error:
        print(error, file=sys.stderr)
        return False

if __name__ == "__main__":
    success = login_user("euler", "password")
    print(f"success = {success}")
