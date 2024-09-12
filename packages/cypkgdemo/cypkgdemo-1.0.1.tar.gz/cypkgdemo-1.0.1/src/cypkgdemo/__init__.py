import cypkgdemo.sa  # support `import cypkgdemo; cypkgdemo.sa.sa(0)`

if locals().get("cypkgdemo", None):
    del cypkgdemo  # avoid infinite level of cypkgdemo.cypkgdemo.cypkgdemo...
