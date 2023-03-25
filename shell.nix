with import <nixpkgs> {};

mkShell {

  buildInputs = [
    python310
    python310Packages.poetry
  ];
}

