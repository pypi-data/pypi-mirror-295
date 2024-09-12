{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    pre-commit-hooks.url = "github:cachix/git-hooks.nix";
    pre-commit-hooks.inputs.nixpkgs.follows = "nixpkgs";
  };
  outputs =
    {
      self,
      nixpkgs,
      pre-commit-hooks,
      ...
    }:
    let
      eachSystem = nixpkgs.lib.genAttrs [ "x86_64-linux" ];
    in
    {
      devShells = eachSystem (
        system:
        let
          pkgs = import nixpkgs { inherit system; };
        in
        {
          default = pkgs.mkShell {
            inherit (self.checks.${system}.pre-commit-check) shellHook;
            buildInputs =
              with pkgs;
              [
                python3
                nixfmt-rfc-style
                pre-commit
                ruff
                uv
              ]
              ++ self.checks.${system}.pre-commit-check.enabledPackages;
          };
        }
      );
      checks = eachSystem (system: {
        pre-commit-check = pre-commit-hooks.lib.${system}.run {
          src = ./.;
          hooks = {
            # pre-defined hooks
            check-added-large-files.enable = true;
            check-executables-have-shebangs.enable = true;
            check-shebang-scripts-are-executable.enable = true;
            check-symlinks.enable = true;
            end-of-file-fixer.enable = true;
            nixfmt-rfc-style.enable = true;
            pyright.enable = true;
            pyright.excludes = [ "^.*migrations/" ];
            ruff-format.enable = true;
            ruff-format.excludes = [ "^.*migrations/" ];
            ruff.enable = true;
          };
        };
      });
    };
}
