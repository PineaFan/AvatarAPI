{
  description = "Licenced under the Fork Your Code Public Licence";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = nixpkgs.legacyPackages.${system};
    in {
      devShells.default = pkgs.mkShell {
        packages = [ pkgs.bashInteractive (pkgs.python3.withPackages (pyPkgs: with pyPkgs; [ opencv4 numpy cairosvg aiohttp ])) ];
      };
    });
}
