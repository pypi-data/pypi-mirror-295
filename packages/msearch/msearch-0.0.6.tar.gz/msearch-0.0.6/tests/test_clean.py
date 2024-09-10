import re
import pytest
from msearch.main import clean, run_search


def test_run_search():
    search_string = "novnc"
    results = run_search(search_string, "web", False)
  

    assert """{"props":{"initialPayload":{"allShortcutsEnabled":false,"path":"/","repo":{"id":
598164,"defaultBranch":"master","name":"noVNC","ownerLogin":"novnc","currentUser
CanPush":false,"isFork":false,"isEmpty":false,"createdAt":"2010-04-07T01:55:44.0
00Z","ownerAvatar":"https://avatars.githubusercontent.com/u/24572588?v=4","publi
c":true,"private":false,"isOrgOwned":true},"currentUser":null,"refInfo":{"name":""" not in results

    assert """{"props""" not in results
    assert """
### Quick Start

* Use the `novnc_proxy` script to automatically download and start websockify, which
  includes a mini-webserver and the WebSockets proxy. The `--vnc` option is
  used to specify the location of a running VNC server:

    `./utils/novnc_proxy --vnc localhost:5901`
    
* If you don't need to expose the web server to public internet, you can
  bind to localhost:
  
    `./utils/novnc_proxy --vnc localhost:5901 --listen localhost:6081`

* Point your browser to the cut-and-paste URL that is output by the `novnc_proxy`
  script. Hit the Connect button, enter a password if the VNC server has one
  configured, and enjoy!
""" in results, f"found {results[results.find('### Quick Start'):results.rfind('Enjoy!') + len('Enjoy!')]}"
    assert """
### Installation from Snap Package
Running the command below will install the latest release of noVNC from Snap:

`sudo snap install novnc`

#### Running noVNC from Snap Directly

You can run the Snap-package installed novnc directly with, for example:

`novnc --listen 6081 --vnc localhost:5901 # /snap/bin/novnc if /snap/bin is not in your PATH`

If you want to use certificate files, due to standard Snap confinement restrictions you need to have them in the /home/<user>/snap/novnc/current/ directory. If your username is jsmith an example command would be:
  
  `novnc --listen 8443 --cert ~jsmith/snap/novnc/current/self.crt --key ~jsmith/snap/novnc/current/self.key --vnc ubuntu.example.com:5901`
""" in results, f"found {results[results.find('### Installation from Snap Package'):results.rfind('ubuntu.example.com:5901') + len('ubuntu.example.com:5901')]}"
    assert """
#### Running noVNC from Snap as a Service (Daemon)
The Snap package also has the capability to run a 'novnc' service which can be 
configured to listen on multiple ports connecting to multiple VNC servers 
(effectively a service runing multiple instances of novnc).
Instructions (with example values):

List current services (out-of-box this will be blank):

```
sudo snap get novnc services
Key             Value
services.n6080  {...}
services.n6081  {...}
```

Create a new service that listens on port 6082 and connects to the VNC server 
running on port 5902 on localhost:

`sudo snap set novnc services.n6082.listen=6082 services.n6082.vnc=localhost:5902`

(Any services you define with 'snap set' will be automatically started)
Note that the name of the service, 'n6082' in this example, can be anything 
as long as it doesn't start with a number or contain spaces/special characters.

View the configuration of the service just created:

```
sudo snap get novnc services.n6082
Key                    Value
services.n6082.listen  6082
services.n6082.vnc     localhost:5902
```

Disable a service (note that because of a limitation in  Snap it's currently not 
possible to unset config variables, setting them to blank values is the way 
to disable a service):

`sudo snap set novnc services.n6082.listen='' services.n6082.vnc=''`

(Any services you set to blank with 'snap set' like this will be automatically stopped)

Verify that the service is disabled (blank values):

```
sudo snap get novnc services.n6082
Key                    Value
services.n6082.listen  
services.n6082.vnc
```""" in results, f"found {results[results.find('#### Running noVNC from Snap as a Service (Daemon)') - 20:results.rfind('services.n6082.vnc') + len('services.n6082.vnc')]}"
    assert """
### Integration and Deployment

Please see our other documents for how to integrate noVNC in your own software,
or deploying the noVNC application in production environments:

* [Embedding](docs/EMBEDDING.md) - For the noVNC application
* [Library](docs/LIBRARY.md) - For the noVNC JavaScript library""" in results, f"found {results[results.find('### Integration and Deployment') -20:results.rfind('Library.md') + len('Library.md')]}"

    assert """\n### Features

* Supports all modern browsers including mobile (iOS, Android)
* Supported authentication methods: none, classical VNC, RealVNC's
  RSA-AES, Tight, VeNCrypt Plain, XVP, Apple's Diffie-Hellman,
  UltraVNC's MSLogonII
* Supported VNC encodings: raw, copyrect, rre, hextile, tight, tightPNG,
  ZRLE, JPEG, Zlib
* Supports scaling, clipping and resizing the desktop
* Local cursor rendering
* Clipboard copy/paste with full Unicode support
* Translations
* Touch gestures for emulating common mouse actions
* Licensed mainly under the [MPL 2.0](http://www.mozilla.org/MPL/2.0/), see
  [the license document](LICENSE.txt) for details

### Screenshots""" in results
if __name__ == "__main__":
    pytest.main()
