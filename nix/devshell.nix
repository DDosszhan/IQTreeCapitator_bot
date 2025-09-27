{
  self,
  pkgs,
}: {
  default = pkgs.mkShell {
    venvDir = "./venv";

    packages = with pkgs; [
      python3Packages.venvShellHook

      (python3.withPackages (
        ps:
          with ps; [
            python
            ruff
          ]
      ))
    ];

    postVenvCreation = ''
      pip install -r requirements.txt
      pip install mypy
      pip install -e .
    '';
  };
}
