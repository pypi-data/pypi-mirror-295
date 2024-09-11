This is the lib readme

Create uv project
`uv init --lib example-lib`

build the package:
```uvx --from build pyproject-build --installer uv```

Publish to PyPi
`uvx twine upload dist/*`

