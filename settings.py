import requests
import sys
import util
from urlparse import urljoin, urlparse

# Change ERROR to DEBUG if you'd like more information.
import logging
logging.basicConfig(level=logging.ERROR, format="%(levelname)s\t%(module)s\t\t%(message)s")

# Set this to the network interface that provides DHCP leases.
public_interface="br0"
# Should we wait for the VMs to receive DHCP leases.
wait_for_addresses=True
# This is the size you want to use when creating a VM.  A value of None causes the demo to select a size arbitrarily.
size_id = None
# This is the profile you want to use when creating a VM.  A value of None causes the demo to select a profile arbitrarily.
profile_id = None
# This is the hypervisor to launch VM instances on.
hypervisor_uri = "v0/hypervisor/instance/kvm1"

# Native Kahu Authentication
if True:
    role="zfierstadt"
    password="testing31337"

    api_url = "https://dashboard.lightcrest.com/kahu/test/"

    session = requests.Session()
    r = session.post(urljoin(api_url, "v0/auth/login"), data={ 'role': role,
                                                               'password': password })
    util.check_response(r, [200])

    # Use an arbitrary tenancy.
    tenant_url = urljoin(api_url, "v0/")

# or directly against the Kahu APIs
else:
    # Note: if basic HTTP auth is required for your Kahu installation, include it in the api_url.
    api_url = "https://<YOUR KAHU HOSTNAME HERE>"
    tenant_url = urljoin(api_url, "/v0/tenant/<YOUR KAHU TENANT ID HERE>/")
    session = requests.Session()

    # Only necessary if your kahu endpoint doesn't have a valid SSL cert.
    session.verify = False
    util.disable_ssl_warnings()

    # Add any additional authentication information here, e.g.
    session.cookies.set("<COOKIE NAME>", "<COOKIE VALUE>")

# Extract just the path information, to make it an external key.
hypervisor_id = urlparse(urljoin(api_url, hypervisor_uri))[2]
