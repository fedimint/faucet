{pkgs, lib}:
let
  mach-nix = import (builtins.fetchGit {
    url = "https://github.com/DavHau/mach-nix/";
    ref = "refs/tags/3.5.0";
  }) {};
  python = mach-nix.mkPython {
    requirements = builtins.readFile ./requirements.txt;
  };
in
pkgs.python3Packages.buildPythonApplication {
  name = "faucet";
  src = ./.;

  propagatedBuildInputs = [ python pkgs.python3Packages.setuptools ];

  installPhase = ''
    runHook preInstall
    python setup.py install --prefix=$out
    cp -r templates $out/lib/python3.9/site-packages/fedimint_helper-1.0-py3.9.egg/EGG-INFO/scripts/templates
    cp -r static $out/lib/python3.9/site-packages/fedimint_helper-1.0-py3.9.egg/EGG-INFO/scripts/static
    wrapProgram $out/bin/faucet.py --prefix PYTHONPATH : "$(toPythonPath $out)"
    runHook postInstall
  '';

  shellHook = "export FLASK_APP=faucet.py";

  format = "other";
}