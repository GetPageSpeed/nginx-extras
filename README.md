# nginx-extras

The nginx-extras project is your freeware Nginx Plus!

It allows you to:

* install prebuilt CentOS/RHEL packages for virtually any NGINX module, without compilation
* submit *your* NGINX module for build in GetPageSpeed extras RPM repository


## Module Requirements (for authors)

The module requirements are pretty straightforward and most of module repositories already follow it:

* Hosted on GitHub
* File releases with sane version numbers
* `config` file in the root of repository

### Submit your module for build

* Fork the repository
* Create `modules/<handle>.yml` file and specify parameters like the example below. The handle should be unique. The resulting package will have name `nginx-module-<handle>`, e.g. `nginx-module-foo`
* Submit pull request. That's it! Your module will be automatically built against both stable and mainline NGINX

### Sample module.yml

```yml
repo: openresty/srcache-nginx-module
summary: Transparent subrequest-based caching layout for arbitrary NGINX locations
description: |
  This module provides a transparent caching layer for arbitrary nginx
  locations (like those use an upstream or even serve static disk files).

  The caching behavior is mostly compatible with RFC 2616.
soname: ngx_http_srcache_filter_module
```

* `repo`: GitHub repository in format `<owner>/<name>`
* `summary`: short (up to 70 characters) summary of the module
* `description`: longer description of the module
* `soname`: basename of dynamic module filename
